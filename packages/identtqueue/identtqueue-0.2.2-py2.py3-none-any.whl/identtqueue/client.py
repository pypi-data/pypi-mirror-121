from identtqueue.job import (
    JobRequest,
    JobResult,
    JobResultType,
    JobStatus,
    JobStatusType,
    Serializable,
)
import uuid
from typing import Any, Awaitable, Dict, Optional, Tuple, Union

import aioredis
import msgpack # type: ignore
import structlog

from identtqueue.exceptions import (
    ClientTimeoutException,
    ErrorException,
    WorkerTimeoutException,
)


class Client:
    def __init__(
        self,
        redis_address: str = "redis://redis",
        redis_max_connections: Optional[int] = 10,
        job_serializer=lambda b: msgpack.packb(b, use_bin_type=True),
        job_deserializer=lambda b: msgpack.unpackb(b),
        status_ttl: int = 60 * 60 * 24,
        logger=None,
    ):
        self.redis_address = redis_address
        self.redis_max_connections = redis_max_connections
        self.job_serializer = job_serializer
        self.job_deserialize = job_deserializer
        self.status_ttl = status_ttl
        self.logger = logger or structlog.get_logger()

        self.redis: Any = None

    async def connect(self) -> None:
        self.logger.debug("redis", status="connect")
        self.pool = aioredis.BlockingConnectionPool.from_url(
            self.redis_address,
            max_connections=self.redis_max_connections,
            retry_on_timeout=False,
        )
        self.redis = aioredis.Redis(connection_pool=self.pool)

    async def disconnect(self) -> None:
        if self.redis is not None:
            self.logger.debug("redis", status="disconnect")
            await self.redis.close()

    def serialize(self, obj: Serializable):
        return self.job_serializer(obj.to_dict())

    def deserialize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.job_deserialize(data)

    async def get_status(self, task_id: str) -> Optional[JobStatus]:
        async with self.redis.client() as conn:
            raw_data = await conn.get(f"{task_id}-status")

            if raw_data:
                return JobStatus(**self.deserialize(raw_data))

            return None

    async def _parse_result(
        self, task_id: str, value: Union[Tuple, str]
    ) -> Optional[Any]:
        data_raw = value[1] if type(value) is tuple else value
        result = JobResult(**self.deserialize(data_raw))

        if result.type == JobResultType.EXCEPTION:
            self.logger.warning("exception", task_id=task_id)
            raise ErrorException(result.message)

        if result.type == JobResultType.WORKER_TIMEOUT:
            self.logger.warning(
                "wroker_timeout",
                task_id=task_id,
            )
            raise WorkerTimeoutException(task_id)

        return result.message

    async def wait_for_result(
        self, task_id: str, result_timeout=60.0, remove=True
    ) -> Optional[Any]:
        """
        Awaits for results.

        :raises ErrorException: when task returns an error
        :raises ClientTimeoutException: when tasks takes more than result_timeout(s) to send response or worker
                timeout was exceeded. For result_timeout=0 it will wait forever.
        :raises WorkerTimeoutException: when worker took too long to process the task
        """
        async with self.redis.client() as conn:
            if remove:
                value = await conn.blpop(f"{task_id}-result", result_timeout)
            else:
                value = await conn.execute_command(
                    "BLMOVE",
                    f"{task_id}-result",
                    f"{task_id}-result",
                    "LEFT",
                    "RIGHT",
                    result_timeout,
                )

            if value is None:
                self.logger.warning("timeout_no_response", task_id=task_id)
                raise ClientTimeoutException(task_id)

            result = await self._parse_result(task_id=task_id, value=value)

            if remove:
                async with conn.pipeline(transaction=True) as pipe:
                    await pipe.delete(f"{task_id}-result").delete(
                        f"{task_id}-status"
                    ).execute()

            return result

    async def get_result(self, task_id: str, remove=True) -> Union[None, Any]:
        """
        Awaits for results.

        :raises ErrorException: when task returns an error
        :raises WorkerTimeoutException: when worker took too long to process the task
        """
        async with self.redis.client() as conn:
            if remove:
                value = await conn.lpop(f"{task_id}-result")
            else:
                value = await conn.execute_command(
                    "LMOVE", f"{task_id}-result", f"{task_id}-result", "LEFT", "RIGHT"
                )

            if value is None:
                return value

            result = await self._parse_result(task_id=task_id, value=value)

            if remove:
                async with conn.pipeline(transaction=True) as pipe:
                    await pipe.delete(f"{task_id}-result").delete(
                        f"{task_id}-status"
                    ).execute()

            return result

    async def get_time(self) -> float:
        (timestamp, microseconds) = await self.redis.time()
        return timestamp + 10 ** -6 * microseconds

    async def enqueue_job(
        self, queue_name: str, function_name: str, *args, **kwargs
    ) -> str:
        """
        Schedule the job.
        """
        task_id = str(uuid.uuid4())

        jr = JobRequest(
            task_id=task_id,
            function_name=function_name,
            args=args,
            kwargs=kwargs,
            enqueue_time=await self.get_time(),
        )
        self.logger.debug(
            "enqueue_job",
            task_id=task_id,
            queue_name=queue_name,
            function=function_name,
        )
        async with self.redis.client() as conn:
            async with conn.pipeline(transaction=True) as pipe:
                await pipe.rpush(queue_name, self.serialize(jr)).set(
                    f"{task_id}-status",
                    self.serialize(JobStatus(status=JobStatusType.ENQUEUED, data={})),
                    ex=self.status_ttl,
                ).execute()

        return task_id
