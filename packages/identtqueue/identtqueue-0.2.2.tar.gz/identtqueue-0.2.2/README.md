# idenTTqueue

Redis based task queue system built for idenTT2check and document-ocr.
In absence of ready to use solution, this project attempts to build limited set of functionality to deliver async queue system.

## Requirments

- redis 6.2.0+
- python 3.6+

## Concept

Package is built on top of aioredis, that covers async communication with Redis.
Current implementation is using list stored at key. Key is used as a message queue.
With `RPUSH [key] [value]` list is adding task to the list (FIFO queue). The `[key]` is equalivent to queue name, while `[value]` is serialized task (task_id, args, kwargs, etc.). The worker (consumer) is 'subscribed' on the `[key]` with `BLPOP [key] [timeout]`, where `[timeout]` defines how long it will wait (default: 0 - waits forever). `BLPOP` is a blocking command, that will resume the coroutine when the message will be delivered with `RPUSH` to the `[key]` that `BLPOP` specified.
First worker that subscribed on the `[key]` will be awaken and will consume the task.
After result is finished, the same mechanism, but in reverse order is used. The client will wait on `BLPOP [task_id] [timeout]` to receive result and worker will push to the `[task_id]` key with `RPUSH [task_id] [value]`. Where `[value]` is serialized value returned by the worker.

## Example usage

Client
```python
client = Client(
    redis_address="redis://redis"
)
await client.connect()

task_id = await client.enqueue_job(
    queue_name="mrz",
    function_name="rnd_magic",
    path="s3://bucket/document.jpg"
)
# wait for task to complete and get result
result = await client.wait_for_result(task_id)

# get result or None
result = await client.get_result(task_id)
```

Worker
```python
async def rnd_magic(ctx, *args, **kwargs):
    return "document not supported"

worker = Worker(
    jobs={"rnd_magic": rnd_magic},
    redis_address="redis://redis",
    queue_name="mrz"
)
worker.run()
```

## Features

- [x] schedule task for any queue with args and kwargs
- [x] worker waits only one one selected queue, asynchronous without pooling
- [x] tasks are perfomed in entry order - FIFO
- [x] serialize input valeues
- [x] serialize output value
- [x] timeout the client if it's waiting too long
- [x] timeout the worker if the task is taking too long
- [x] report exceptions
- [x] prototype project (example)
- [x] test coverage
- [x] test timeouts in tests
- [x] worker is able to consume multiple task in one queue
- [x] time of execution and how long task waited in the queue logged
- [x] worker and client can survice redis disconnect, will auto-reconnect
- [x] monitor task status (initalized, pending, finished)
- [x] retry on worker failure/lost
- [ ] schedule cron tasks (?)
- [ ] worker is able to listen to mutliple queues (?)

## Running tests

```bash
pipenv shell
docker run --rm -p 6379:6379 redis:6.2.4
make test
```

## Run example project

```bash
pipenv shell
make dist
cd example && docker-compose up
```