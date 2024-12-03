import argparse
import logging
import pathlib
import sys
import typing


SolveFn = typing.Callable[[pathlib.Path], str]


def solver(solve_fn: SolveFn):
    cwd = pathlib.Path.cwd()

    script_path = pathlib.Path(sys.argv[0])

    solution_name = script_path.stem
    day_name = script_path.parent.name

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()

    input_file_path = pathlib.Path(args.input_file)
    debug: bool = args.debug

    logging.basicConfig(
        format="%(asctime)s %(levelname).2s: %(message)s",
        datefmt="%I:%M:%S %p",
        level=logging.INFO if not debug else logging.DEBUG,
    )

    logging.debug(f"provided input file: {input_file_path}")

    if not input_file_path.is_absolute():
        input_file_path = cwd.joinpath(input_file_path)

    logging.info(f"executing solver: {day_name=} {solution_name=}")
    logging.info(f"input_file: {input_file_path.relative_to(cwd)}")

    answer = solve_fn(input_file_path)

    logging.info("result: " + answer)
