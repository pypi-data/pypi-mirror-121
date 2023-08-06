#!/usr/bin/env python

from unittest.mock import MagicMock
from identtqueue.job import JobStatusType
import logging
import itertools

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asyncmock import AsyncMock

import asyncio
import pytest
import aioredis

from identtqueue.worker import Worker
from identtqueue.client import Client
from identtqueue.exceptions import (
    ClientTimeoutException,
    ErrorException,
    WorkerTimeoutException,
)


async def sleep_for_two_secons(ctx, *args, **kwargs):
    await asyncio.sleep(2)
    return


async def raise_exception(ctx, *args, **kwargs):
    raise Exception("exception message")


@pytest.mark.asyncio
async def test_check_health(worker, caplog):
    caplog.set_level(logging.INFO)
    worker: Worker = worker({})
    await worker.connect()

    assert await worker.check_health() is True

    await worker.disconnect()


@pytest.mark.asyncio
async def test_check_health_loop(worker, caplog):
    caplog.set_level(logging.INFO)
    worker: Worker = worker({}, health_check_retry_time=0.001, health_check_max_tries=5)
    worker.check_health = AsyncMock(return_value=True)

    await worker.health_loop(is_error=True)
    assert worker.check_health.call_count == 1


@pytest.mark.asyncio
async def test_check_healthcheck_loop(worker, caplog):
    caplog.set_level(logging.INFO)
    worker: Worker = worker(
        {},
        health_check_retry_time=0.001,
        health_check_max_tries=1,
        wait_task_timeout=0.01,
    )
    worker.health_loop = AsyncMock(return_value=True)

    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    assert worker.health_loop.called_once


@pytest.mark.asyncio
async def test_check_health_without_connection(worker, caplog):
    caplog.set_level(logging.INFO)
    worker: Worker = worker({})

    assert await worker.check_health() is False


@pytest.mark.parametrize("health_check_max_tries", [0, 2])
@pytest.mark.asyncio
async def test_check_health_loop_without_connection(
    health_check_max_tries, worker, caplog
):
    caplog.set_level(logging.INFO)
    worker: Worker = worker(
        {}, health_check_retry_time=0.001, health_check_max_tries=health_check_max_tries
    )
    worker.check_health = AsyncMock(return_value=False)
    with pytest.raises(SystemExit):
        await worker.health_loop(is_error=True)

    assert worker.check_health.call_count == health_check_max_tries


@pytest.mark.asyncio
async def test_on_startup_called(worker, caplog):
    caplog.set_level(logging.INFO)
    on_startup = AsyncMock()
    worker: Worker = worker({}, on_startup=on_startup)
    await worker.connect()

    assert worker.redis is not None
    on_startup.assert_called_once_with(worker.ctx)


@pytest.mark.asyncio
async def test_on_shutdown_called(worker, caplog):
    caplog.set_level(logging.INFO)
    on_shutdown = AsyncMock()
    worker: Worker = worker({}, on_shutdown=on_shutdown)
    await worker.connect()
    await asyncio.sleep(0)  # force io cycle
    await worker.disconnect()

    on_shutdown.assert_called_once_with(worker.ctx)


@pytest.mark.asyncio
async def test_task_schedule(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()
    task_result = await client.wait_for_result(task_id, result_timeout=0.01)
    await client.disconnect()

    assert task_result == 42


@pytest.mark.asyncio
async def test_loop_connection_exception(worker, caplog):
    caplog.set_level(logging.ERROR)
    worker: Worker = worker(
        {}, queue_name="default", wait_task_timeout=0.01, health_check_max_tries=1
    )
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)

    worker.connect = AsyncMock()
    worker.redis = AsyncMock()
    worker.health_loop = AsyncMock()
    worker.redis.blpop = AsyncMock(side_effect=aioredis.exceptions.ConnectionError())
    await worker.loop()

    assert worker.health_loop.called_once


@pytest.mark.asyncio
async def test_task_get_result(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)

    task_result_before = await client.get_result(task_id=task_id)
    await worker.loop()
    task_result_after = await client.get_result(task_id=task_id)

    await client.disconnect()

    assert task_result_before is None
    assert task_result_after == 42


@pytest.mark.asyncio
async def test_task_get_result_removed(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    await client.get_result(task_id=task_id, remove=True)
    task_after_removed = await client.get_result(task_id=task_id)

    await client.disconnect()

    assert task_after_removed is None


@pytest.mark.asyncio
async def test_task_get_result_keep_result(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    await client.get_result(task_id=task_id, remove=False)
    task_after_removed = await client.get_result(task_id=task_id)

    await client.disconnect()

    assert task_after_removed == 42


@pytest.mark.asyncio
async def test_task_wait_for_result_keep_result(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    await client.wait_for_result(task_id=task_id, remove=False)
    task_after_removed = await client.wait_for_result(task_id=task_id)

    await client.disconnect()

    assert task_after_removed == 42


@pytest.mark.asyncio
async def test_task_status(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=42)
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)

    task_status_before = await client.get_status(task_id=task_id)
    await worker.loop()
    task_status_after = await client.get_status(task_id=task_id)

    await client.disconnect()

    assert task_status_before is not None
    assert task_status_after is not None

    assert task_status_before.status == JobStatusType.ENQUEUED.value
    assert task_status_after.status == JobStatusType.FINISHED.value


@pytest.mark.asyncio
async def test_task_status_does_not_exist(client, caplog):
    caplog.set_level(logging.ERROR)
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_status = await client.get_status(task_id="does-not-exist")

    await client.disconnect()

    assert task_status is None


@pytest.mark.asyncio
async def test_task_schedule_complex(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    mock_function = AsyncMock(return_value=dict(one=dict(two=dict(three=3))))
    worker: Worker = worker({"mock_function": mock_function}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "mock_function", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()
    task_result = await client.wait_for_result(task_id, result_timeout=0.01)
    await client.disconnect()

    assert task_result["one"]["two"]["three"] == 3


@pytest.mark.asyncio
async def test_task_schedule_invalid_function(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    worker: Worker = worker({}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "does_not_exist")
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()
    with pytest.raises(ErrorException):
        await client.wait_for_result(task_id, result_timeout=0.01)
    await client.disconnect()


@pytest.mark.asyncio
async def test_task_catch_exception(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    worker: Worker = worker({"raise_exception": raise_exception}, queue_name="default")
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "raise_exception", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    with pytest.raises(ErrorException):
        await client.wait_for_result(task_id, result_timeout=0.01)
    await client.disconnect()


@pytest.mark.asyncio
async def test_task_timeout(worker, client, caplog):
    caplog.set_level(logging.ERROR)
    worker: Worker = worker(
        {"sleep": sleep_for_two_secons},
        queue_name="default",
        job_execution_timeout=0.01,
    )
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    task_id = await client.enqueue_job("default", "sleep", 1)
    cycle = itertools.cycle([True, False])
    worker.loop_forever = lambda: next(cycle)
    await worker.loop()

    with pytest.raises(WorkerTimeoutException):
        await client.wait_for_result(task_id, result_timeout=0.01)
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_timeout(client, caplog):
    caplog.set_level(logging.ERROR)
    client: Client = client()
    await client.connect()

    await client.redis.flushdb()
    with pytest.raises(ClientTimeoutException):
        await client.wait_for_result("random-name", result_timeout=0.01)
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_time(client, caplog):
    caplog.set_level(logging.ERROR)
    client: Client = client()
    await client.connect()
    time = await client.get_time()
    time2 = await client.get_time()

    assert type(time) == float
    assert type(time2) == float
    assert time2 > time

    await client.disconnect()


@pytest.mark.asyncio
async def test_worker_time(worker, caplog):
    caplog.set_level(logging.ERROR)
    worker: Worker = worker({}, queue_name="default")
    await worker.connect()

    time = await worker.get_time()
    time2 = await worker.get_time()

    assert type(time) == float
    assert type(time2) == float
    assert time2 > time

    await worker.disconnect()


@pytest.mark.asyncio
async def test_ztask_catch_exception(client, caplog):
    caplog.set_level(logging.ERROR)
    client: Client = client()
    await client.connect()

    await client.enqueue_job("default", "raise_exception", 1)

    await client.disconnect()
