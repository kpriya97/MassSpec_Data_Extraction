import click
from minidom_oop import Reader
import logging


logger = logging.getLogger(__name__)


@click.group
def main():
    """Entry method"""
    pass


@main.command()
@click.argument('path')
def get_spectrum_values(path: str):
    reader = Reader(path=path)
    data = reader.analyse_spectrum()
