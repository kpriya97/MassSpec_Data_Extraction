import click
from reader import Reader
from peptide_prediction import *
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def main():
    """Entry method"""
    pass


@main.command()
@click.argument('path')
@click.option('-v', '--verbose', default=False, is_flag=True, help="When used, will print the paths to STDOUT.")
def get_spectrum_values(path: str, verbose: bool = False):
    """Generates dataframe consisting of the spectrum values from the input mzml/mzxml file"""
    reader = Reader(path=path)
    data = reader.analyse_spectrum()
    if verbose:
        click.echo(data)


@main.command()
@click.argument('fasta_path')
@click.argument('mzml_path')
@click.option('-v','--verbose',default=False,is_flag = True,help='when used will print to STODUT')
def peptide_info(fasta_path: str, mzml_path: str,verbose: bool = False):
    """Generates dataframe consisting of peptide properties and list of peptide hit seqeunces"""
    search = PeptideSearch(fasta_path, mzml_path)
    info = search.peptide_wrapper()[0]
    peptide_list =search.peptide_wrapper()[1]
    if verbose:
        click.echo(info)
        click.echo(peptide_list)


if __name__ == '__main__':
    main()

