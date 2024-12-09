import pathlib
import typing


def read_input_lines(file_path: pathlib.Path) -> typing.Generator[str, None, None]:
    with file_path.open("r") as fp:
        for line in fp:
            yield line


def read_input_lines_v2(file_path: pathlib.Path) -> typing.Generator[str, None, None]:
    with file_path.open("r") as fp:
        for line in fp:
            line = line.strip()

            if len(line) > 0:
                yield line


def read_input(file_path: pathlib.Path) -> str:
    with file_path.open("r") as fp:
        return fp.read()
