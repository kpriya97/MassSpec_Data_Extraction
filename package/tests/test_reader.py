import pytest
import pandas as pd
from package.protein_spectra_package.reader import Reader
import xml.dom.minidom
import argparse


test1 = Reader('C:/Users/laras/PycharmProjects/group_3/package/tests/data/BSA1.mzML')
test2 = Reader('C:/Users/laras/PycharmProjects/group_3/package/tests/data/7MIX_STD_110802_1.mzXML')
test3 = Reader('C:/Users/laras/PycharmProjects/group_3/package/tests/data/BSA.fasta')


class TestReader:
    """A test class which conducts pytests on the Reader class."""

    def test_check_extension(self):
        """Tests whether the check_extension function returns True if a valid file format is passed and
        False if an invalid format is passed."""
        assert test1.check_extension() is True
        assert test2.check_extension() is True
        assert test3.check_extension() is False

    def test_parse_file(self):
        file1 = test1.parse_file()
        assert isinstance(file1, xml.dom.minidom.Document)
        file2 = test2.parse_file()
        assert isinstance(file2, xml.dom.minidom.Document)
        with pytest.raises(argparse.ArgumentTypeError):
            test3.parse_file()

    def test_get_spectrum_list(self):
        file1 = test1.parse_file()
        output1 = test1.get_spectrum_list(file1)
        assert isinstance(output1, list)
        assert isinstance(output1[0], xml.dom.minidom.Element)
        assert len(output1) == 1684
        file2 = test2.parse_file()
        output2 = test2.get_spectrum_list(file2)
        assert isinstance(output2, list)
        assert isinstance(output2[0], xml.dom.minidom.Element)
        assert len(output2) == 7161

    def test_get_spectrum_dict(self):
        file1 = test1.parse_file()
        list1 = test1.get_spectrum_list(file1)
        dict1 = test1.get_spectrum_dict(list1)
        assert isinstance(dict1, dict)
        assert len(dict1) == 1684
        assert isinstance(list(dict1.keys())[0], int)
        assert isinstance(dict1[0], xml.dom.minidom.Element)
        file2 = test2.parse_file()
        list2 = test2.get_spectrum_list(file2)
        dict2 = test2.get_spectrum_dict(list2)
        assert isinstance(dict2, dict)
        assert len(dict2) == 7161
        assert isinstance(list(dict2.keys())[0], int)
        assert isinstance(dict2[1], xml.dom.minidom.Element)

    def test_get_values(self):
        file1 = test1.parse_file()
        list1 = test1.get_spectrum_list(file1)
        dict1 = test1.get_spectrum_dict(list1)
        values1 = test1.get_values(dict1)
        assert isinstance(values1, dict)
        assert len(values1[0]) == 6
        keys = ['spectra_id', 'base_peak_m/z', 'base_peak_intensity', 'total_ion_current', 'lowest_observed_m/z',
                'highest_observed_m/z']
        assert keys == list(values1[0].keys())
        id0 = {'spectra_id': 0,
               'base_peak_m/z': 391.28,
               'base_peak_intensity': 928844.25,
               'total_ion_current': 6937649.0,
               'lowest_observed_m/z': 300.0,
               'highest_observed_m/z': 2008.46}
        assert values1[0] == id0

    def test_analyse_spectrum(self):
        result1 = test1.analyse_spectrum()
        assert isinstance(result1, pd.DataFrame)
