import pymzml


# Example on how to use pymzml
# Read file and get spectrum count
run = pymzml.run.Reader('../tests/data/sample_ms_file1.mzML')
print(run.get_spectrum_count())


# Access specific spectrum with its scan ID
spec_1 = run[5]


# Get intensity array from spectrum
intensity = spec_1.i
print(len(intensity))
print(intensity)


# Get m/z array from spectrum
mz = spec_1.mz
print(len(mz))
print(mz)


# Get spectrum index (from scan ID)
s_id = spec_1.index
print(s_id)

