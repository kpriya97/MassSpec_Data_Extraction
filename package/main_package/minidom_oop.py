from xml.dom import minidom as md
from typing import List, Dict
import base64
import zlib
import struct
import logging
import pandas as pd


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
            # self.parsed_file = parsed_file
            return parsed_file
        else:
            raise ValueError('Please parse an input file of either .mzML or .mzXML format.')

    @staticmethod
    def get_spectrum_list(parsed_file) -> List:
        spectrum_list = parsed_file.getElementsByTagName('spectrum')
        return spectrum_list

    @staticmethod
    def get_spectrum_dict(spectrum_list: List) -> Dict:
        spectrum_dict = dict()
        for spectrum in spectrum_list:
            ids = int(spectrum.getAttribute("index"))
            spectrum_dict[ids] = spectrum
        # print(spectrum_dict.keys())
        return spectrum_dict

    def get_compression(self, spectrum_dict: Dict):
        """Gathers information about the encoding of the binary arrays in the parsed input file.

        Parameters
        ----------
        spectrum_dict: Dict
            Spectrum dictionary. Contains spectrum ids and the corresponding spectrum object

        Returns
        -------
        dict_final: Dict[int, Dict]
            Dictionary containing the encoding information. Keys are the spectrum ids and the values are as followed:
            {'mz': {'data_type': data_type, 'compression': compression}, 'intensity': {'data_type': data_type,
            'compression': compression}}.

        """
        compression_dict = dict()
        for key in spectrum_dict:
            params = spectrum_dict[key].getElementsByTagName('binaryDataArray')
            data = list()
            for array in params:
                p = array.getElementsByTagName('cvParam')
                for e in p:
                    data.append(e.getAttribute('name'))
            compression_dict[key] = data
        print(compression_dict[0])
        compression_list = list()
        for key in compression_dict:
            mz = compression_dict[key].index('m/z array')
            intensity = compression_dict[key].index('intensity array')
            if mz < intensity:
                mz_comp = compression_dict[key][:mz]
                int_comp = compression_dict[key][mz + 1:intensity]
            else:
                int_comp = compression_dict[key][:intensity]
                mz_comp = compression_dict[key][intensity + 1:mz]
            compression_list.append([mz_comp, int_comp])
        dict_final = dict()
        for key in compression_dict:
            dict_final[key] = {'mz': dict(), 'intensity': dict()}
            value_mz = compression_list[key][0]
            value_int = compression_list[key][1]
            for val in value_mz:
                if 'float' in val or 'int' in val or 'bit' in val:
                    dict_final[key]['mz']['data_type'] = val
                elif 'compression' in val:
                    dict_final[key]['mz']['compression'] = val
            for val in value_int:
                if 'float' in val or 'int' in val or 'bit' in val:
                    dict_final[key]['intensity']['data_type'] = val
                elif 'compression' in val:
                    dict_final[key]['intensity']['compression'] = val
        print(dict_final[0])
        self.compression = dict_final
        return

    def get_binary_spectrum_values(self, spectrum_dict: Dict):
        """Takes a spectrum dictionary and returns a dictionary of the spectrum index and the m/z ratio and the
        intensity values in binary format.

        Parameters
        ----------
        spectrum_dict: Dict
            Spectrum dictionary. Contains spectrum ids as keys and the corresponding spectrum object from the mzMl file.

        compression_dict: Dict[int, Dict]
            Dictionary containing information regarding the encoding of the binary array.

        Returns
        -------
        vals: Dict[str, Dict]
            Dictionary of spectrum ids as keys and their mz values and intensity values in binary format as values.
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
        """
        Takes the raw spectrum values and returns a dictionary of decoded and uncompressed m/z and intensity values.
        Parameters
        ----------

        Returns
        -------
        spectrum_data: Dict
            dictionary of decoded and uncompressed m/z and intensity values
        """
        spectrum_data = dict()
        for key in self.binary_values:
            encoded_mz_data, encoded_int_data = self.binary_values[key]['mz'], self.binary_values[key]['intensity']
            if encoded_mz_data is not None or encoded_int_data is not None:
                decoded_mz_data, decoded_int_data = base64.standard_b64decode(
                    encoded_mz_data), base64.standard_b64decode(
                    encoded_int_data)  # # decodes the string
                decompressed_mz_data, decompressed_int_data = zlib.decompress(decoded_mz_data), zlib.decompress(
                    decoded_int_data)  # decompresses the data
                mz_data = struct.unpack('<%sf' % (len(decompressed_mz_data) // 4),
                                        decompressed_mz_data)  # unpacks 32-bit m/z values as floats
                int_data = struct.unpack('<%sf' % (len(decompressed_int_data) // 4),
                                         decompressed_int_data)  # unpacks 32-bit intensity values as floats
                spectrum_data[key] = {'mz': mz_data, 'intensity': int_data}
            else:
                spectrum_data[key] = {'mz': None, 'intensity': None}
        self.spectrum_data = spectrum_data
        return

    def analyse_spectrum(self):
        """
        Wrapper function for the parsing of an mzML file and the extraction of the m/z and intensity values.
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
        data = pd.DataFrame.from_dict(self.spectrum_data, orient='index', columns=['mz', 'intensity'])
        # print(data)
        return data
