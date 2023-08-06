from _typeshed import NoneType
from argparse import ArgumentParser, Namespace
from json import load
from pprint import pprint
from typing import Any


def getKwargs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Pretty Print Me!",
        usage="Pretty print anything to the terminal",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input file to pretty print",
        required=False
    )

    return parser.parse_args()


def loadJSON(filename: str) -> Any:
    data: Any
    try:
        with open(file=filename, mode="r") as file:
            data = load(file)
            file.close()
        return data
    except FileNotFoundError:
        print("Invalid file path")
        quit(3)


def main() -> None:
    args: Namespace = getKwargs()

    try:
        if args.input[-5::] == ".json":
            pprint(loadJSON(args.input))
        else:
            print("Invalid file extension")
            quit(1)
    except NoneType:
        print("No arguements passed")
        quit(2)


if __name__ == "__main__":
    main()
