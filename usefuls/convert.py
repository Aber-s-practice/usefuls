#!/usr/bin/python3
import click
from PIL import Image


@click.group(help="Convert format.")
def main():
    pass


@main.command(help="Convert picture format.")
@click.argument("source", type=click.Path(exists=True, dir_okay=False))
@click.argument("target", type=click.Path(exists=False, dir_okay=False, writable=True))
def image(source, target):
    img = Image.open(source)
    img.save(target)


if __name__ == "__main__":
    main()
