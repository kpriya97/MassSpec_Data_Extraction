""" Protein Prediction module tests """

import pytest
from package.protein_spectra_package.protein_prediction import ProteinSearch
from package.protein_spectra_package.peptide_prediction import PeptideSearch
from .constants import TEST_FASTA_FILE, TEST_MZML_FILE

pep = PeptideSearch(fasta_path=str(TEST_FASTA_FILE), mzml_path=str(TEST_MZML_FILE))
peptide_list = pep.peptide_wrapper()[1]


class TestProteinSearch:
    """Unit tests for ProteinSearch class """

    def test_filter_peptides(self):
        """Checks whether peptide list is filtered
        """
        pro = ProteinSearch(peptide_list=peptide_list)
        filterted_pep_list = pro.filter_peptides()
        assert isinstance(filterted_pep_list, list)
        # ['DDSPDLPK', 'DLGEEHFK', 'LVTDLTK', 'DLGEEHFK', 'AEFVEVTK', 'YLYEIAR', 'LVVSTQTALA', 'YLYEIAR']
        assert len(filterted_pep_list) == 8

    def test_divide_into_chunks(self):
        """Checks whether a given list is divided into list of 15 elements
        """
        pro = ProteinSearch(peptide_list=peptide_list)
        list_for_chunks = ['DDSPDLPK', 'DLGEEHFK', 'LVTDLTK', 'DLGEEHFK', 'LVTDLTK', 'LVVSTQTALA', 'YLYEIAR',
                           'AEFVEVTK', 'YLYEIAR', 'LVVSTQTALA', 'YLYEIAR', 'DLGEEHFK', 'AEFVEVTK', 'YLYEIAR',
                           'DDSPDLPK', 'DLGEEHFK', 'YLYEIAR', 'LVVSTQTALA', 'YLYEIAR']
        pro.divide_into_chunks(list_for_chunks)

        assert len(pro.sel_peptides) == 2
        assert pro.sel_peptides == [['DDSPDLPK', 'DLGEEHFK', 'LVTDLTK', 'DLGEEHFK', 'LVTDLTK', 'LVVSTQTALA', 'YLYEIAR',
                                     'AEFVEVTK', 'YLYEIAR', 'LVVSTQTALA', 'YLYEIAR', 'DLGEEHFK', 'AEFVEVTK', 'YLYEIAR',
                                     'DDSPDLPK'], ['DLGEEHFK', 'YLYEIAR', 'LVVSTQTALA', 'YLYEIAR']]

