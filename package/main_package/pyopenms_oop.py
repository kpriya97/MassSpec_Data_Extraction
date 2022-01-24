from pyopenms import *
from typing import Dict, List
from pyopenms.pyopenms_7 import SimpleSearchEngineAlgorithm

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
        self.peptide_ids = None
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

        if self.mzml_path and self.fasta_path:
            SimpleSearchEngineAlgorithm().search(self.mzml_path, self.fasta_path, protein_ids, peptide_ids)
            logger.info('mzml file and fasta file exists')
            return protein_ids, peptide_ids
        else:
            logger.error('Input files are invalid')

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
        self.peptide_ids = peptide_ids
        peptide_info = dict()
        if self.peptide_ids is not None:
            logger.info('SimpleSearchEngineAlgorithm identified peptide ids correctly')
            for peptide_id in self.peptide_ids:
                peptide_info['Peptide ID m/z'] = float(round(peptide_id.getMZ(), 2))
                peptide_info['Peptide ID rt'] = float(round(peptide_id.getRT(), 2))
                # print(peptide_info)
                for hit in peptide_id.getHits():
                    peptide_info['Peptide hit sequence'] = str(hit.getSequence())
                    peptide_info['Peptide hit score'] = float(round(hit.getScore(), 2))
            return peptide_info
        else:
            logger.warning(
                'No peptides were identified by SimpleSearchEngineAlgorithm and no peptide properties were stored')
            print('SimpleSearchEngineAlgorithm did not identify any peptides')

    def get_peptidesequence_list(self, peptide_ids) -> List:
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

        self.peptide_ids = peptide_ids
        peptide_list = []
        if peptide_ids is not None:
            for peptide_id in self.peptide_ids:
                for hit in peptide_id.getHits():
                    peptide_list.append(str(hit.getSequence()))
                    logger.info('Hit peptide sequences are stored in a list')
        return peptide_list

# mzml_path = r'A:\Semester_3\group_3\package\tests\data\test_files_1\BSA1.mzML'
# fasta_path = r'A:\Semester_3\group_3\package\tests\data\test_files_1\BSA.fasta'
# test = PeptideSearch(fasta_path, mzml_path)
# peptide_ids = test.peptide_search()[1]
# peptide_info = test.get_peptide_identification_values(peptide_ids=peptide_ids)
# peptide_list = test.get_peptidesequence_list(peptide_ids=peptide_ids)
# print(peptide_list)