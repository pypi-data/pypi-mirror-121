class ClientTimeoutException(Exception):
    pass


class WorkerTimeoutException(Exception):
    pass


class ErrorException(Exception):
    pass


class ResultNotFound(Exception):
    pass
