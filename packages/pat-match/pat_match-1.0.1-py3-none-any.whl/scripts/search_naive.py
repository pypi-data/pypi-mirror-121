import argparse
import sys

sys.path.append("../")
from scripts import utils


def run_naive(main_str, pattern):
    ms_len = len(main_str)
    ss_len = len(pattern)
    matched_indices = []

    for i in range(ms_len - ss_len + 1):
        for j in range(ss_len):
            if main_str[i + j] != pattern[j]:
                break
        if j + 1 == ss_len:
            matched_indices.append(i + 1)

    return matched_indices


def run(fa_file, fq_file):
    fasta_seqs = utils.get_seq_from_file(fa_file, "fasta")
    fastq_seqs = utils.get_seq_from_file(fq_file, "fastq")

    for fastq_seq in fastq_seqs:
        for fasta_seq in fasta_seqs:
            matched_indices = run_naive(fasta_seq.seq, fastq_seq.seq)
            utils.output_sam(matched_indices, fasta_seq, fastq_seq)


def main():
    parser = argparse.ArgumentParser(description="Matches a pattern using the naive approach")
    parser.add_argument("-fa", "--fasta-file", dest="fasta_file", default="resources/fasta_input.fa", help="fasta file")
    parser.add_argument("-fq", "--fastq-file", dest="fastq_file", default="resources/fastq_input.fq", help="fastq file")
    args = parser.parse_args()

    run(args.fasta_file, args.fastq_file)
