from xml.dom import minidom as md
from typing import List, Dict
import base64
import zlib
import struct
import logging


class Reader:
    def __init__(self, path):
        self.path = path
        self.format = None  # can be 'mzml' or 'mzxml', set in check_extension
        self.parsed_file = None
        pass

    def check_extension(self) -> bool:
        """Checks if the extension of the parsed file is either .mzML or .mzXML.

        :return:
            bool
        """
        if self.path.endswith('.mzML'):
            self.format = 'mzml'
            return True
        elif self.path.endswith('.mzXML'):
            self.format = 'mzxml'
            return True
        else:
            # logger: wrong file format
            return False

    def parse_file(self):
        if self.check_extension():
            parsed_file = md.parse(self.path)
            self.parsed_file = parsed_file
            return  # or: return parsed_file instead of self.parsed_file
        else:
            raise ValueError('Please parse an input file of either .mzML or .mzXML format.')

    def get_spectrum_list(self):
        spectrum_list = self.parsed_file.getElementsByTagName('spectrum')
        return spectrum_list