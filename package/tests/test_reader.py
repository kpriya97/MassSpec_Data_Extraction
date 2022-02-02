import pytest
import pandas as pd
from reader.py import Reader
import xml.dom.minidom


class TestReader:
    """A test class which conducts pytests on the Reader class."""

    def test_check_extension(self):
        """Tests whether the check_extension function returns True if a valid file format is passed and
        False if an invalid format is passed."""
        test = Reader('package/tests/data/BSA1.mzML')
        assert test.check_extension is True
        test1 = Reader('package/tests/data/7MIX_STD_110802_1.mzXML')
        assert test1.check_extension is True
        test2 = Reader('package/tests/data/BSA.fasta')
        assert test2.check_extension is False

    def test_parse_file(self):
        test = Reader('package/tests/data/BSA1.mzML')
        file = test.parse_file()
        assert file.isinstance(xml.dom.minidom.Document)
        test2 = Reader('package/tests/data/BSA.fasta')
        # assert raise error?

    def test_get_spectrum_list(self):
        test = Reader('package/tests/data/BSA1.mzML')
        output = get_spectrum_list()

