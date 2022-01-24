import xml.dom.minidom
from xml.dom import minidom as md
from typing import List, Dict
import base64
import zlib
import struct
import logging


logger = logging.getLogger(__name__)


class Reader:
    def __init__(self, path):
        self.path = path
        self.format = None  # can be 'mzml' or 'mzxml', set in check_extension
        self.compression = None
        self.binary_values = None
        self.spectrum_data = None
        # self.parsed_file = None

    def check_extension(self) -> bool:
        """Checks if the extension of the parsed file is either .mzML or .mzXML.

        Returns
        -------
        bool: True if allowed extension else False

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

    def parse_file(self) -> xml.dom.minidom.Document:
        """Parses the input file and creates minidom object.

        Returns
        -------
        parsed_file: xml.dom.minidom.Document
            xml.dom.minidom.Document from the parsed input file

        Raises
        -------
        ValueError: if the input file has non-allowed extension
        """
        if self.check_extension():
            parsed_file = md.parse(self.path)
            print(parsed_file)
            return parsed_file
        else:
            raise ValueError('Please parse an input file of either .mzML or .mzXML format.')

    def get_spectrum_list(self, parsed_file: xml.dom.minidom.Document) -> List[xml.dom.minidom.Element]:
        """Creates and returns list with spectra from the xml.dom.minidom.Document of the input file.

        Parameters
        ----------
        parsed_file: xml.dom.minidom.Document
            xml.dom.minidom.Document of the parsed input file

        Returns
        -------
        spectrum_list: List[xml.dom.minidom.Element]
            list containing the spectra as xml.dom.minidom.Element
        """
        if self.format == 'mzml':
            spectrum_list = parsed_file.getElementsByTagName('spectrum')
        elif self.format == 'mzxml':
            pass
        return spectrum_list

    def get_spectrum_dict(self, spectrum_list: List[xml.dom.minidom.Element]) -> Dict[int, xml.dom.minidom.Element]:
        """Creates and returns dictionary with spectrum ids as key and xml.dom.minidom.Element as values from
        spectrum list.

        Parameters
        ----------
        spectrum_list: List[xml.dom.minidom.Element]
            list containing the spectra as xml.dom.minidom.Element

        Returns
        -------
        spectrum_dict: Dict[int, xml.dom.minidom.Element]
            dictionary with spectrum ids as key and xml.dom.minidom.Element as values

        """
        spectrum_dict = dict()
        for spectrum in spectrum_list:
            if self.format == 'mzml':
                ids = int(spectrum.getAttribute("index"))
                spectrum_dict[ids] = spectrum
            elif self.format == 'mzxml':
                pass
        return spectrum_dict

    def get_compression(self, spectrum_dict: Dict):
        """Gathers information about the encoding of the binary arrays in the parsed input file.

        Parameters
        ----------
        spectrum_dict: Dict[int, xml.dom.minidom.Element]
            dictionary with spectrum ids as key and xml.dom.minidom.Element as values

        Returns
        -------

        """
        compression_dict = dict()
        for key in spectrum_dict:
            if self.format == 'mzml':
                params = spectrum_dict[key].getElementsByTagName('binaryDataArray')
                data = list()
                for array in params:
                    p = array.getElementsByTagName('cvParam')
                    for e in p:
                        data.append(e.getAttribute('name'))
                compression_dict[key] = data
            elif self.format == 'mzxml':
                pass
        compression_list = list()
        for key in compression_dict:
            mz = compression_dict[key].index('m/z array')
            intensity = compression_dict[key].index('intensity array')
            length = len(compression_dict[key])
            if mz < intensity:
                mz_comp = compression_dict[key][:int(length/2)]
                int_comp = compression_dict[key][int(length/2):]
            else:
                int_comp = compression_dict[key][:int(length/2)]
                mz_comp = compression_dict[key][int(length/2):]
            compression_list.append([mz_comp, int_comp])
        dict_final = dict()
        for key in compression_dict:
            dict_final[key] = {'mz': dict(), 'intensity': dict()}
            value_mz = compression_list[key][0]
            value_int = compression_list[key][1]
            for val in value_mz:
                if 'float' in val or 'bit' in val:
                    dict_final[key]['mz']['data_type'] = val
                elif 'compression' in val:
                    dict_final[key]['mz']['compression'] = val
            for val in value_int:
                if 'float' in val or 'bit' in val:
                    dict_final[key]['intensity']['data_type'] = val
                elif 'compression' in val:
                    dict_final[key]['intensity']['compression'] = val
        self.compression = dict_final
        return

    def get_binary_spectrum_values(self, spectrum_dict: Dict[int, xml.dom.minidom.Element]):
        """

        Parameters
        ----------
        spectrum_dict: Dict[int, xml.dom.minidom.Element]
            dictionary with spectrum ids as key and xml.dom.minidom.Element as values

        Returns
        -------

        """
        vals = dict()
        bin_dict = dict()
        for key in spectrum_dict:
            if spectrum_dict[key].getAttribute('defaultArrayLength') != '0':
                mz_array, intensity_array = spectrum_dict[key].getElementsByTagName('binary')
                vals[key] = {'mz': mz_array, 'intensity': intensity_array}
            else:
                vals[key] = {'mz': None, 'intensity': None}
        for key in vals:
            if vals[key]['mz'] is not None and vals[key]['intensity'] is not None:
                bin_dict[key] = {'mz': vals[key]['mz'].firstChild.nodeValue,
                                 'intensity': vals[key]['intensity'].firstChild.nodeValue}
            else:
                bin_dict[key] = {'mz': None, 'intensity': None}
        self.binary_values = bin_dict
        return

    def decode_decompress(self):
        """Takes the raw spectrum values and creates a dictionary of decoded and uncompressed m/z and intensity values.
        Parameters
        ----------

        Returns
        -------

        """
        spectrum_data = dict()
        for key in self.binary_values:
            encoded_mz_data, encoded_int_data = self.binary_values[key]['mz'], self.binary_values[key]['intensity']
            if encoded_mz_data is not None or encoded_int_data is not None:
                decoded_mz_data = base64.standard_b64decode(encoded_mz_data)
                decoded_int_data = base64.standard_b64decode(encoded_int_data)  # # decodes the string
                if self.compression[key]['mz']['compression'] == 'zlib compression':
                    decompressed_mz_data = zlib.decompress(decoded_mz_data)
                else:
                    decompressed_mz_data = decoded_mz_data
                if self.compression[key]['intensity']['compression'] == 'zlib compression':
                    decompressed_int_data = zlib.decompress(decoded_int_data)  # decompresses the data
                else:
                    decompressed_int_data = decoded_int_data
                if self.compression[key]['mz']['data_type'] == '32-bit float':
                    mz_data = struct.unpack('<%sf' % (len(decompressed_mz_data) // 4),
                                            decompressed_mz_data)  # unpacks 32-bit m/z values as floats
                elif self.compression[key]['mz']['data_type'] == '64-bit float':
                    mz_data = struct.unpack('<%sd' % (len(decompressed_mz_data) // 8),
                                            decompressed_mz_data)
                if self.compression[key]['intensity']['data_type'] == '32-bit float':
                    int_data = struct.unpack('<%sf' % (len(decompressed_int_data) // 4),
                                             decompressed_int_data)  # unpacks 32-bit intensity values as floats
                elif self.compression[key]['intensity']['data_type'] == '64-bit float':
                    int_data = struct.unpack('<%sd' % (len(decompressed_int_data) // 8),
                                             decompressed_int_data)
                spectrum_data[key] = {'mz': mz_data, 'intensity': int_data}
            else:
                spectrum_data[key] = {'mz': None, 'intensity': None}
        self.spectrum_data = spectrum_data
        return

    def analyse_spectrum(self):
        """Wrapper function for the parsing of an mzML file and the extraction of the m/z and intensity values.
        Parameters
        ----------

        Returns
        -------

        """
        parsed_file = self.parse_file()
        s_list = self.get_spectrum_list(parsed_file)
        spectrum_dictionary = self.get_spectrum_dict(s_list)
        self.get_compression(spectrum_dictionary)
        self.get_binary_spectrum_values(spectrum_dictionary)
        self.decode_decompress()
        data = self.spectrum_data
        return data


if __name__ == '__main__':
    test = Reader("../tests/data/test_files_1/BSA1.mzML")
    data_test = test.analyse_spectrum()