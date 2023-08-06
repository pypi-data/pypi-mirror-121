import pytest
import os
from identtqueue.worker import Worker
from identtqueue.client import Client


REDIS_ADDRESS = "redis://redis" if os.getenv("CI") else "redis://localhost"


@pytest.fixture
async def worker():
    worker_: Worker = None

    def create(jobs, **kwargs):
        nonlocal worker_
        worker_ = Worker(jobs, redis_address=REDIS_ADDRESS, **kwargs)
        return worker_

    yield create

    if worker_:
        await worker_.disconnect()


@pytest.fixture
async def client():
    client_: client = None

    def create(**kwargs):
        nonlocal client_
        client_ = Client(redis_address=REDIS_ADDRESS, **kwargs)
        return client_

    yield create

    if client_:
        await client_.disconnect()
