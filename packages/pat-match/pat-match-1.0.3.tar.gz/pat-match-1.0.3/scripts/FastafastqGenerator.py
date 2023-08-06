import sys

# File output - fasta
fastafile = open(sys.argv[1], "w")

# File output - fastq
fastqfile = open(sys.argv[2], "w")

fastaCount = int(input("Enter number of fasta strings\n"))
fastainterval = int(10000 / fastaCount)
fastaseq = [None] * fastaCount
fastalength = fastainterval
for i in range(fastaCount):
    fastaseq[i] = "a" * fastalength
    fastalength = fastalength + fastainterval

fastqCount = int(input("Enter number of fasta strings\n"))
fastqinterval = int(500 / fastqCount)
fastqlength = fastqinterval
fastqseq = [None] * fastqCount
for i in range(fastqCount):
    fastqseq[i] = "a" * fastqlength
    fastqlength = fastqlength + fastqinterval

# Seq count
count = 1;

# Loop through each line in the input file
print("Converting to FASTA...")
for strLine in fastaseq:
    # Output the header
    fastafile.write(">" + str(count) + "\n")
    fastafile.write(strLine + "\n")

    count = count + 1
print("Done.")

# Seq count
count = 1;

# Loop through each line in the input file
print("Converting to FASTQ...")
for strLine in fastqseq:
    # Output the header
    fastqfile.write("@" + strLine + "\n")
    fastqfile.write(strLine + "\n")
    fastqfile.write("+" + "\n")
    fastqfile.write(len(strLine) * '~' + "\n")

    count = count + 1
print("Done.")

# Close the input and output file
fastafile.close()
fastqfile.close()
