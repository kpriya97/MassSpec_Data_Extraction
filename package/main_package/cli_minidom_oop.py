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
@click.option('-v', '--verbose', default=False, is_flag=True, help="When used, will print the paths to STDOUT.")
def get_spectrum_values(path: str, verbose: bool = False):
    reader = Reader(path=path)
    data = reader.analyse_spectrum()
    if verbose:
        click.echo(data)

