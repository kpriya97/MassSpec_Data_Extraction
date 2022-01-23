import click
from pyopenms_oop import *

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def main():
    """Entry method."""
    pass


# task 2 cli printing dictionary of peptide properties and list of peptide hit sequences
@main.command()
@click.argument('fasta_path')
@click.argument('mzml_path')
def info(fasta_path: str, mzml_path: str):
    """Generates peptide info dictionary and list of peptide hit sequences"""

    search = PeptideSearch(fasta_path, mzml_path)
    peptide_ids = search.peptide_search()[1]
    peptide_info = search.get_peptide_identification_values(peptide_ids=peptide_ids)
    click.echo(peptide_info)
    peptide_list = search.get_peptidesequence_list(peptide_ids=peptide_ids)
    click.echo('Hit peptide sequences after comparing experimental and theoretical MS data')
    print(peptide_list)


if __name__ == "__main__":
    main()
