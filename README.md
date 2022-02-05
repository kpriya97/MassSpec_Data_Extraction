# Group 3 (WS-2021)

## Programming Project 4 - Compute the Number of Peptides of a Given Total Mass

------------------

### Contributors

--------------

- Priya Kempanna
- Lara Schmalenstroer
- Rohitha Ravinder 
- Shubhi Ambast

### Introduction 

--------------

Mass spectrometry is used extensively in the biochemical field for calculating the molecular weight of isolated
proteins as well as identifying possible modifications made to the protein itself (post-translational modifications). MS works by
generating a spectrum (known as a mass spectrum) which plots the mass-to-charge ratio (m/z) of the ions in the sample. By
using the values derived from such a spectrum, one can determine with a high degree of accuracy what the compound (or
peptide) is.


### protein_spectra_package location in repository

--------------
```
├── package
│ └── protein_spectra_package
    └── __init__.py
    └── cli.py
    └── peptide_prediction.py
    └── protein_prediction.py
    └── reader.py
    └── startup.py
  └── tests
    └── data
    └── __init__.py
    └── test_peptide_prediction.py
    └── test_protein_prediction.py
    └── test_reader.py
  └── setup.py
```

### Description about the package

--------------

protein_spectra_package includes python scripts and tests to perform following tasks:
1. **Parse raw MS files** for their m/z values using */reader.py*
2. **Predict which peptides** using */peptide_prediction.py*
3. **Determine the proteins** that the predicted peptides could be derived from using */protein_prediction.py*
4. **Create a frontend** to upload a raw MS output file and obtain a list of possible peptides
5. **Containerize the Application** to bundle backend and frontend together

- [pyOpenMS](https://pyopenms.readthedocs.io/en/latest/) is an open source Python library used in this project for analysis of mass spectrometry raw data(mzXML, mzML, TraML, fasta, pepxml). The package helps in identifying of peptide fragments, isotopic abundances and peptide search.
  - pyOpenMS interacts with other search engines such as Mascot, MSFragger, OMSSA, Sequest, SpectraST, XTandem to identify proteins from peptide sequence databases.

- [EMBL-EBI Proteins API](https://www.ebi.ac.uk/proteins/api/doc/#/proteomics) is used to make API query which searches in the databases like MaxQB, PeptideAtlas, EPD and  ProteomicsDB and saves the output in json format.
  - Base url API for the task used here: "https://www.ebi.ac.uk/proteins/api/proteomics?offset=0&size=100&peptide={api_query}" ; api_query = peptide(str)
  
### References

-------

- Add research papers' links

### Installation

--------------

- To install pyOpenMS from command line:
```
pip install numpy
pip install pyopenms
```
- To install protein_spectra_package from command line, navigate to folder package and execute:
```
pip install protein_spectra_package
```

### Usage

-------


### License

-------

Code released under the [MIT license] (https://choosealicense.com/licenses/mit/).