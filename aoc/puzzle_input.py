import pathlib
import typing


def read_input_lines(file_path: pathlib.Path) -> typing.Generator[str, None, None]:
    with file_path.open("r") as fp:
        for line in fp:
            yield line


def read_input(file_path: pathlib.Path) -> str:
    with file_path.open("r") as fp:
        return fp.read()
