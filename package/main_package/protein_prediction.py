import logging
import requests
import sys
import json
import pandas as pd
from collections import defaultdict

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProteinSearch:

    def __init__(self, peptide_list: list):
        self.peptide_list = peptide_list

        self.sel_peptides = []
        self.protein_response = ""
        self.ans_df = None

    def filter_peptides(self):
        """Filters peptide sequence if it contains special characters and divides
        into chunks of length 15 for submitting to API.
        Parameters
        ----------
        peptide_list: List of peptide sequences

        """
        filtered_pep_list = [pep for pep in self.peptide_list if "(" not in pep and ")" not in pep]
        for i in range(0, len(filtered_pep_list), 15):
            chunks = filtered_pep_list[i:i + 15]
            self.sel_peptides.append(chunks)

    def get_api_query(self, list_peps: list) -> str:
        """Converts the list of peptides to The Proteins API query format
        Parameters
        ----------
        list_peps: list of peptides

        Returns
        -------
        api_query: str ->  converted API format
        """
        api_query = ""
        for pep in list_peps:
            if list_peps.index(pep) == 0:
                api_query = pep
            else:
                api_query += "%2C" + pep
        return api_query

    def proteins_api(self):
        """Make API query for 15 peptides at a time
        The Proteins API is used, which searches in the databases: MaxQB, PeptideAtlas, EPD and  ProteomicsDB
        The response in json format is saved
        """
        self.filter_peptides()
        for pep_lil in self.sel_peptides:
            api_query = self.get_api_query(pep_lil)
            requestURL = f"https://www.ebi.ac.uk/proteins/api/proteomics?offset=0&size=100&peptide={api_query}"
            r = requests.get(requestURL, headers={"Accept": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            self.protein_response += r.text

    def parse_content(self):
        """Function to parse the API request into dataframe
        """
        self.proteins_api()

        ans_dict = defaultdict(lambda: defaultdict(str))
        for l in range(len(json.loads(self.protein_response))):
            ind = json.loads(self.protein_response)[l]
            ans_dict[l + 1]["Peptide"] = ind["features"][0]["peptide"]
            ans_dict[l + 1]["Protein_Accession"] = ind["accession"]
            ans_dict[l + 1]["Sequence"] = ind["sequence"]

        self.ans_df = pd.DataFrame.from_dict(ans_dict, orient="index")

# Test
# pep_l = ['DDSPDLPK', 'YIC(Carbamidomethyl)DNQDTISSK', 'C(Carbamidomethyl)C(Carbamidomethyl)TESLVNR',
#          'LC(Carbamidomethyl)VLHEK', 'DLGEEHFK', 'LC(Carbamidomethyl)VLHEK', 'LVTDLTK', 'DLGEEHFK', 'AEFVEVTK',
#          'EAC(Carbamidomethyl)FAVEGPK', 'EAC(Carbamidomethyl)FAVEGPK', 'GAC(Carbamidomethyl)LLPK', 'YLYEIAR',
#          'LVVSTQTALA', 'YLYEIAR']
#
# search = ProteinSearch(pep_l)
# search.parse_content()
# print(search.ans_df)
