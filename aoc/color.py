def purple(text: str) -> str:
    return "\033[35m" + text + "\033[0m"


def blue(text: str) -> str:
    return "\033[34m" + text + "\033[0m"


def red(text: str) -> str:
    return "\033[31m" + text + "\033[0m"


def yellow(text: str) -> str:
    return "\033[33m" + text + "\033[0m"
