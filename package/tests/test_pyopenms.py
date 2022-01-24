from pyopenms import *
import json
import requests
# mzml_file = r"C:\Users\Shubhi Ambast\group_3\package\tests\data\sample_ms_file1.mzML"
# exp = MSExperiment()
# MzMLFile().load(mzml_file, exp)
# spectrum_data = exp.getSpectrum(0).get_peaks()
# chromatogram_data = exp.getChromatogram(0).get_peaks()
# print(spectrum_data)
# help(exp)
# for spectrum in exp:
#     print(spectrum.size())

# mz, intensities = spectrum.get_peaks()
# print(exp.getNrSpectra())
# print(exp.getNrChromatograms())
# for spec in exp:
#   print ("MS Level:", spec.getMSLevel())
#
# spec = exp[1]
# mz, intensity = spec.get_peaks()
# print(sum(intensity))
#
# for peak in spec:
#     print (peak.getIntensity())
#
# # Calculates total ion current of an LC-MS/MS experiment
# def calcTIC(exp, mslevel):
#     tic = 0
#     # Iterate through all spectra of the experiment
#     for spec in exp:
#         # Only calculate TIC for matching (MS1) spectra
#         if spec.getMSLevel() == mslevel:
#             mz, i = spec.get_peaks()
#             tic += sum(i)
#     return tic
#
# print(calcTIC(exp, 1))
# print(sum([sum(s.get_peaks()[1]) for s in exp if s.getMSLevel() == 1]))
# print(calcTIC(exp, 2))


mzml_file = r'C:\Users\Shubhi Ambast\group_3\package\tests\data\test_files_1\BSA1.mzML'
fasta_file = r'C:\Users\Shubhi Ambast\group_3\package\tests\data\test_files_1\BSA.fasta'
protein_ids = list()
peptide_ids = list()
peptide_list = list()
SimpleSearchEngineAlgorithm().search(mzml_file,fasta_file, protein_ids, peptide_ids)
for peptide_id in peptide_ids:
  # Peptide identification values
  print (35*"=")
  print ("Peptide ID m/z:", peptide_id.getMZ())
  print ("Peptide ID rt:", peptide_id.getRT())
  print ("Peptide scan index:", peptide_id.getMetaValue("scan_index"))
  print ("Peptide scan name:", peptide_id.getMetaValue("scan_index"))
  print ("Peptide ID score type:", peptide_id.getScoreType())
  # PeptideHits

  for hit in peptide_id.getHits():
    print(" - Peptide hit rank:", hit.getRank())
    print(" - Peptide hit charge:", hit.getCharge())
    print(" - Peptide hit sequence:", hit.getSequence())
    mz = hit.getSequence().getMonoWeight(Residue.ResidueType.Full, hit.getCharge()) / hit.getCharge()
    print(" - Peptide hit monoisotopic m/z:", mz)
    print(" - Peptide ppm error:", abs(mz - peptide_id.getMZ())/mz *10**6 )
    print(" - Peptide hit score:", hit.getScore())

for peptide_id in peptide_ids:
  for hit in peptide_id.getHits():
    print(" - Peptide hit sequence:", hit.getSequence())
    print(" - Peptide hit score:", hit.getScore())

for protein_id in protein_ids:
  for hit in protein_id.getHits():
    print("Protein hit accession:", hit.getAccession())
    print("Protein hit sequence:", hit.getSequence())
    print("Protein hit score:", hit.getScore())


#to check if peptide atlas API works on single peptide derived from above results

peptides = ['DDSPDLPK','LVTDLTK']
for peptide in peptides:
  api_query = f"http://www.peptideatlas.org/api/promast/v1/map?peptide={peptide}"
  r = requests.get(api_query, headers={"Accept": "application/json"})
  print(r.status_code)
  print(r.text)
  print(r.json())