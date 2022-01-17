from xml.dom import minidom as md
from typing import List, Dict


# End of the file: chromatogram list, we only need spectrum list.
# Binary data arrays are also in the chromatogram block
def parse_file(path: str):
    """

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
    """

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


def get_spectrum_dict(spectrum_list) -> Dict:
    """

    Parameters
    ----------
    spectrum_list: xml.dom object
        Spectrum list object. Contains spectrum list from parsed mzML file.

    Returns
    -------
    intensity_arrays: List[xml.dom objects]
        list of intensity arrays contained in the mzMl file.
    """
    spectrum_dict = dict()
    for spectrum in spectrum_list:
        ids = int(spectrum.getAttribute("index"))
        # scan = spectrum.getAttribute("scan")
        spectrum_dict[ids] = spectrum
    print(spectrum_dict.keys())
    return spectrum_dict


def get_spectrum_values(spectrum_dict: Dict) -> Dict[str, Dict]:
    """

    Parameters
    ----------
    spectrum_dict: Dict
        Spectrum dictionary. Contains spectrum ids as keys and the corresponding spectrum object from the mzMl file.

    Returns
    -------
    vals: Dict[str, Dict]
        Dictionary of spectrum ids as keys and their mz values and intensity values as values.
    """
    vals = dict()
    for key in spectrum_dict:
        if spectrum_dict[key].getAttribute('defaultArrayLength') != '0':
            mz_array, intensity_array = spectrum_dict[key].getElementsByTagName('binary')
            vals[key] = {'mz': mz_array, 'intensity': intensity_array}
        else:
            vals[key] = {'mz': None, 'intensity': None}
    print(vals[0])
    return vals


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
    p_file = parse_file('sample_ms_file1.mzML')
    s_list = get_spectrum_list(p_file)
    spectrum_dictionary = get_spectrum_dict(s_list)
    vals = get_spectrum_values(spectrum_dictionary)
    return vals


values = analyse_spectrum('sample_ms_file1.mzML')



