from pyopenms import *
from typing import Dict, List
from pyopenms.pyopenms_7 import SimpleSearchEngineAlgorithm
import pandas as pd

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PeptideSearch:
    """ PeptideSearch is a class which uses PyOpenMS to compare experimental mass spectrums from
    mzml file and fasta file to obtain peptide and peptide values."""

    def __init__(self, fasta_path: str, mzml_path: str):
        """
        parameters:
            fasta_path = file path of input fasta file
            mzml_path = file path of input mzml file consisting of mass spectrums
        """
        self.fasta_path = fasta_path
        self.mzml_path = mzml_path

    def peptide_search(self) -> tuple[list, list]:
        """ This method uses SimpleSearchEngineAlgorithm that compares experimental spectrum data from mzml file
        with theoretical data from fasta file of protein sequences.

        Returns
        -------
        list
            Returns peptide id and protein id lists which addresses respective peptide spectrum
        """
        protein_ids = list()
        peptide_ids = list()

        assert self.mzml_path.endswith('.mzML')
        assert self.fasta_path.endswith('.fasta')

        if not self.mzml_path and self.fasta_path:
            logger.error('Input files are invalid')
        else:
            SimpleSearchEngineAlgorithm().search(self.mzml_path, self.fasta_path, protein_ids, peptide_ids)
            logger.info('mzml file and fasta file exists')
            return protein_ids, peptide_ids

    def get_peptide_identification_values(self, peptide_ids) -> Dict:
        """ Gets peptide data corresponding to a single identified spectrum or feature.
        Each peptide hit stores the information of a specific peptide-to-spectrum match
        (e.g., the score and the peptide sequence)

        Parameters
        ----------
        peptide_ids: list
            List of peptide ids matched with theoretical data obtained from fasta file

        Returns
        -------
        dict
            peptide information stored in dictionary

        """
        peptide_info = dict()
        if peptide_ids is None:
            logger.error('SimpleSearchEngineAlgorithm did not identify any peptides')
        else:
            for peptide_id in peptide_ids:
                peptide_info['Peptide ID m/z'] = [float(round(peptide_id.getMZ(), 2))]
                peptide_info['Peptide ID rt'] = [float(round(peptide_id.getRT(), 2))]
                for hit in peptide_id.getHits():
                    peptide_info['Peptide hit sequence'] = [str(hit.getSequence())]
                    peptide_info['Peptide hit score'] = [float(round(hit.getScore(), 2))]
                    # print(peptide_info)
        logger.info('Algorithm returned peptide properties stored in a dictionary')
        return peptide_info

    def get_sequence(self, peptide_ids) -> List:
        """ Stores the hit protein sequences in a list after comparing experimental and theoretical MS data.

        Parameters
        ----------
         peptide_ids: list
            List of peptide ids matched with theoretical data obtained from fasta file

        Returns
        -------
        list
            peptide hit sequences stored in list
        """
        peptide_list = []
        if peptide_ids is not None:
            for peptide_id in peptide_ids:
                for hit in peptide_id.getHits():
                    peptide_list.append(str(hit.getSequence()))
                    logger.info('Hit peptide sequences are stored in a list')
        return peptide_list


    def peptide_wrapper(self):
        '''
        Wraaper function to create a dataframe with peptide values
        :return:
        '''
        peptide_ids = self.peptide_search()[1]
        peptide_info = self.get_peptide_identification_values(peptide_ids=peptide_ids)
        peptide_df = pd.DataFrame.from_dict(peptide_info)
        peptide_list = self.get_sequence(peptide_ids=peptide_ids)
        return peptide_df, peptide_list


if __name__ == '__main__':

    mzml_path = r'C:\Users\Shubhi Ambast\plab2_project\group_3\package\tests\data\test_files_1\BSA1.mzML'
    fasta_path = r'C:\Users\Shubhi Ambast\plab2_project\group_3\package\tests\data\test_files_1\BSA.fasta'
    test = PeptideSearch(fasta_path, mzml_path)
    peptides = test.peptide_wrapper()
    print(peptides[0])
    print(peptides[1])
