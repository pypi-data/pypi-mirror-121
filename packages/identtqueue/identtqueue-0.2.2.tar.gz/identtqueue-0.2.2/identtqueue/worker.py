import asyncio
import sys
from typing import Any, Awaitable, Callable, Dict, Optional
from functools import partial

import aioredis
import msgpack # type: ignore
import structlog

from identtqueue.utils import mesure
from identtqueue.job import (
    JobRequest,
    JobResult,
    JobStatus,
    JobResultType,
    JobStatusType,
    Serializable,
)


class Worker:
    def __init__(
        self,
        jobs: Dict[str, Callable],
        redis_address: str = "redis://redis",
        queue_name: str = "default",
        result_ttl: int = 60 * 5,
        status_ttl: int = 60 * 60 * 24,
        job_execution_timeout: float = 60.0,
        on_startup: Optional[Callable[[Dict], Awaitable]] = None,
        on_shutdown: Optional[Callable[[Dict], Awaitable]] = None,
        wait_task_timeout: float = 0,
        health_check_interval: float = 0,
        health_check_max_tries: int = 10,
        health_check_retry_time: int = 5,
        job_serializer=lambda b: msgpack.packb(b, use_bin_type=True),
        job_deserializer=lambda b: msgpack.unpackb(b),
        logger=None,
    ):
        self.redis_address = redis_address
        self.queue_name = queue_name
        self.health_check_interval = health_check_interval
        self.jobs = jobs
        self.result_ttl = result_ttl
        self.status_ttl = status_ttl
        self.job_execution_timeout = job_execution_timeout
        self.job_serializer = job_serializer
        self.job_deserialize = job_deserializer
        self.on_startup = on_startup
        self.on_shutdown = on_shutdown
        self.wait_task_timeout = wait_task_timeout
        self.health_check_max_tries = health_check_max_tries
        self.health_check_retry_time = health_check_retry_time
        self.logger = logger or structlog.get_logger()

        self.redis: Any = None
        self.ctx: Dict = {}

    async def check_health(self) -> bool:
        if not self.redis:
            return False

        try:
            return await self.redis.ping()
        except aioredis.exceptions.ConnectionError:  # pragma: no cover
            return False

    async def health_loop(self, is_error=False) -> None:
        for _ in range(self.health_check_max_tries):
            if await self.check_health():
                return
            self.logger.info("worker", status="unhealthy")
            await asyncio.sleep(self.health_check_retry_time)

        if is_error:
            sys.exit(1)

    async def send_result(self, task_id: str, result: JobResult) -> None:
        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.rpush(f"{task_id}-result", self.serialize(result)).expire(
                task_id, self.result_ttl
            ).execute()
        await self.update_status(task_id, status=JobStatusType.FINISHED)

    async def update_status(
        self, task_id: str, status=JobStatusType.ENQUEUED, **kwargs
    ) -> None:
        await self.redis.set(
            f"{task_id}-status",
            self.serialize(JobStatus(status=status, data=kwargs)),
            ex=self.status_ttl,
        )

    def serialize(self, obj: Serializable):
        return self.job_serializer(obj.to_dict())

    def deserialize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.job_deserialize(data)

    async def connect(self) -> None:
        self.redis = await aioredis.from_url(
            self.redis_address, health_check_interval=self.health_check_interval
        )

        if self.on_startup:
            await self.on_startup(self.ctx)

    async def disconnect(self) -> None:
        if self.on_shutdown:
            await self.on_shutdown(self.ctx)

        if self.redis:
            await self.redis.close()
            self.redis = None

    def run(self) -> None:  # pragma: no cover
        if sys.version_info >= (3, 8):
            asyncio.run(self.loop())
        else:
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.loop())
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.run_until_complete(loop.shutdown_default_executor())
            finally:
                loop.close()

    def loop_forever(self) -> bool:  # pragma: no cover
        """
        Loop forever is used for testing. It's used to mock the number of iterations to only one - to speed up tests.
        """
        return True

    async def get_time(self) -> float:
        (timestamp, microseconds) = await self.redis.time()
        return timestamp + 10 ** -6 * microseconds

    async def perform_loop(self) -> None:
        while self.loop_forever():
            try:
                self.logger.debug(
                    "worker", status="waiting", queue_name=self.queue_name
                )
                task_result = await self.redis.blpop(
                    self.queue_name, timeout=self.wait_task_timeout
                )
                if task_result is None:
                    await self.health_loop()
                    continue

                _, data_raw = task_result
                job_request = JobRequest(**self.deserialize(data_raw))
                queue_time = await self.get_time() - job_request.enqueue_time

                with mesure() as t:
                    try:
                        self.logger.debug(
                            "task",
                            status="new",
                            task_id=job_request.task_id,
                            function_name=job_request.function_name,
                            queue_name=self.queue_name,
                        )
                        if job_request.function_name not in self.jobs.keys():
                            self.logger.warn(
                                "function not found",
                                task_id=job_request.task_id,
                                function_name=job_request.function_name,
                                queue_name=self.queue_name,
                            )
                            await self.send_result(
                                job_request.task_id,
                                JobResult(
                                    JobResultType.EXCEPTION, "function not found"
                                ),
                            )
                            continue

                        await self.update_status(
                            job_request.task_id, status=JobStatusType.PROCESSING
                        )
                        result = await asyncio.wait_for(
                            self.jobs[job_request.function_name](
                                self.ctx,
                                *job_request.args,
                                **job_request.kwargs,
                                update_status=partial(
                                    self.update_status,
                                    status=JobStatusType.PROCESSING,
                                    task_id=job_request.task_id,
                                ),
                            ),
                            timeout=self.job_execution_timeout,
                        )
                        worker_time = t()
                        self.logger.info(
                            "task",
                            status="success",
                            queue_name=self.queue_name,
                            task_id=job_request.task_id,
                            worker_time=worker_time,
                            queue_time=queue_time,
                            total_time=worker_time + queue_time,
                        )
                        await self.send_result(
                            job_request.task_id,
                            JobResult(JobResultType.SUCCESS, result),
                        )
                    except asyncio.TimeoutError:
                        worker_time = t()
                        self.logger.error(
                            "task",
                            status="wroker_timeout",
                            queue_name=self.queue_name,
                            task_id=job_request.task_id,
                            worker_time=worker_time,
                            queue_time=queue_time,
                            total_time=worker_time + queue_time,
                        )
                        await self.send_result(
                            job_request.task_id, JobResult(JobResultType.WORKER_TIMEOUT)
                        )
                    except Exception as e:
                        worker_time = t()
                        self.logger.exception(
                            "task",
                            status="exception",
                            queue_name=self.queue_name,
                            task_id=job_request.task_id,
                            worker_time=worker_time,
                            queue_time=queue_time,
                            total_time=worker_time + queue_time,
                            exc_info=e,
                        )
                        await self.send_result(
                            job_request.task_id,
                            JobResult(JobResultType.EXCEPTION, str(e)),
                        )
            except aioredis.exceptions.ConnectionError:
                await self.health_loop(is_error=True)

    async def loop(self) -> None:
        await self.connect()
        try:
            await self.perform_loop()
        finally:
            await self.disconnect()
