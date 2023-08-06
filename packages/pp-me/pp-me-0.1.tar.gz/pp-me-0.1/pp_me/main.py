from argparse import ArgumentParser, Namespace
from json import load
from pprint import pprint as print
from typing import Any


def getKwargs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Pretty Print Me!",
        usage="Pretty print anything to the terminal",
    )

    parser.add_argument(
        "-j",
        "--json",
        type=str,
        help="JSON file to pretty print",
    )

    return parser.parse_args()


def loadJSON(filename: str) -> Any:
    data: Any
    with open(file=filename, mode="r") as file:
        data = load(file)
        file.close()
    return data


def main() -> None:
    args: Namespace = getKwargs()

    if args.json[-5::] != ".json":
        print("Invalid JSON file extension")
        quit(1)
    else:
        print(loadJSON(args.json))


if __name__ == "__main__":
    main()
