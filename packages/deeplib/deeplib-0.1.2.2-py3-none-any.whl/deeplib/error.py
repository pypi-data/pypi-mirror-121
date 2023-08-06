class DeepError(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


def error(message: str) -> DeepError:
    return DeepError(message)
