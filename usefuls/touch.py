#!/usr/bin/python3
import os
import sys

import click


@click.command()
@click.argument("path", required=True)
def main(path: str = None) -> None:
    if os.path.exists(path):
        os.utime(path)
        return

    with open(path, "wb+"):
        pass


if __name__ == "__main__":
    main()
