__author__ = 'Josh Daniel'

input_file = open('../contributions_fec_2008.csv', 'r')
out_files = [open('../contributions_fec_2008a_0.csv', 'w'),
             open('../contributions_fec_2008a_1.csv', 'w'),
             open('../contributions_fec_2008a_2.csv', 'w'),
             open('../contributions_fec_2008a_3.csv', 'w')]

# Write header line to all output files
header_line = input_file.readline()
for out_file in out_files:
    out_file.write(header_line)

# Write each line to one of 4 output files. Alternates which output file gets written to.
i = 0
for line in input_file:
    out_files[i%4].write(line)
    i += 1

# Close files.
input_file.close()
for out_file in out_files:
    out_file.close()