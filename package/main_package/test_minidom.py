from xml.dom import minidom as md
from typing import List, Dict
import base64, zlib, struct


def parse_file(path: str):
    """Reads input mzML file and returns the parsed file.

    Parameters
    ----------
    path: str
        path to the mzML file

    Returns
    -------
    parsed file: xml.dom object
        parsed mzml file
    """
    parsed_file = md.parse(path)
    return parsed_file


def get_spectrum_list(parsed_file) -> List:
    """Reads parsed mzML file and returns a list of DOM element objects containing the spectra.

    Parameters
    ----------
    parsed_file: xml.dom object
        parsed mzMl file

    Returns
    -------
    spectrum_list: List[xml.dom object]
        spectrum list contains the spectrum objects from the parsed input file
    """
    spectrum_list = parsed_file.getElementsByTagName('spectrum')
    return spectrum_list


def get_spectrum_dict(spectrum_list: List) -> Dict:
    """Takes list of DOM objects containing the spectrum information and returns dictionary with data to each spectrum.

    Parameters
    ----------
    spectrum_list: xml.dom object
        Spectrum list object. Contains spectrum list from parsed mzML file.

    Returns
    -------
    spectrum_dict: Dict[]
        Dictionary that contains the spectrum information to the spectra contained in the parsed file.
        The keys are integers and the values dom objects.
    """
    spectrum_dict = dict()
    for spectrum in spectrum_list:
        ids = int(spectrum.getAttribute("index"))
        spectrum_dict[ids] = spectrum
    # print(spectrum_dict.keys())
    return spectrum_dict


def get_spectrum_values(spectrum_dict: Dict) -> Dict[str, Dict]:
    """Takes a spectrum dictionary and returns a dictionary of the spectrum index and the m/z ratio and the intensity
    values in binary format.

    Parameters
    ----------
    spectrum_dict: Dict
        Spectrum dictionary. Contains spectrum ids as keys and the corresponding spectrum object from the mzMl file.

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
    return bin_dict


def decode_decompress(vals: dict) -> Dict:
    """
    Takes the raw spectrum values and returns a dictionary of decoded and uncompressed m/z and intensity values.
    Parameters
    ----------
    vals: Dict
        dictionary of raw spectrum values

    Returns
    -------
    spectrum_data: Dict
        dictionary of decoded and uncompressed m/z and intensity values
    """
    spectrum_data = dict()
    for key in vals:
        encoded_mz_data, encoded_int_data = vals[key]['mz'], vals[key]['intensity']
        if encoded_mz_data is not None or encoded_int_data is not None:
            decoded_mz_data, decoded_int_data = base64.standard_b64decode(encoded_mz_data), base64.standard_b64decode(encoded_int_data)  # # decodes the string
            decompressed_mz_data, decompressed_int_data = zlib.decompress(decoded_mz_data), zlib.decompress(decoded_int_data)  # decompresses the data
            mz_data = struct.unpack('<%sf' % (len(decompressed_mz_data) // 4), decompressed_mz_data)  # unpacks 32-bit m/z values as floats
            int_data = struct.unpack('<%sf' % (len(decompressed_int_data) // 4), decompressed_int_data)  # unpacks 32-bit intensity values as floats
            spectrum_data[key] = {'mz': mz_data, 'intensity': int_data}
        else:
            spectrum_data[key] = {'mz': None, 'intensity': None}
    return spectrum_data


def analyse_spectrum(path: str) -> Dict:
    """
    Wrapper function for the parsing of an mzML file and the extraction of the m/z and intensity values.
    Parameters
    ----------
    path: str
        path to mzML file

    Returns
    -------
    vals: Dict
        dictionary with intensity and m/z values
    """
    p_file = parse_file(path)
    s_list = get_spectrum_list(p_file)
    spectrum_dictionary = get_spectrum_dict(s_list)
    vals = get_spectrum_values(spectrum_dictionary)
    data = decode_decompress(vals)
    # print(data)
    return data


analyse_spectrum("../tests/data/sample_ms_file1.mzML")
