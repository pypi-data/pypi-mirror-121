class DeepError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def error(message):
    return DeepError(message)