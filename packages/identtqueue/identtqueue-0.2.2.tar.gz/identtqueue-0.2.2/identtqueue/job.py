from typing import Any, Dict, Tuple
from enum import Enum, unique


class Serializable:
    def to_dict(self):
        return self.__dict__


@unique
class JobStatusType(int, Enum):
    ENQUEUED = 0
    PROCESSING = 1
    FINISHED = 2


class JobStatus(Serializable):
    def __init__(self, data={}, status=JobStatusType.PROCESSING) -> None:
        self.status = status
        self.data = data


class JobRequest(Serializable):
    def __init__(
        self,
        task_id: str,
        function_name: str,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        enqueue_time: float,
    ) -> None:
        self.task_id = task_id
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.enqueue_time = enqueue_time


@unique
class JobResultType(int, Enum):
    SUCCESS = 0
    EXCEPTION = 1
    WORKER_TIMEOUT = 2


class JobResult(Serializable):
    def __init__(self, type: JobResultType, message: Any = None) -> None:
        self.message = message
        self.type = type
