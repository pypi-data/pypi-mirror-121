import argparse
import sys

sys.path.append("../")
from scripts import utils


def run_ba(main_str, pattern):
    border_arr_str = pattern + "$" + main_str
    n = len(border_arr_str)
    ba = [0] * n
    b = 0
    matched_indices = []

    for i in range(1, n):
        while b > 0 and border_arr_str[i] != border_arr_str[b]:
            b = ba[b - 1]
        if border_arr_str[i] == border_arr_str[b]:
            b = b + 1
        else:
            b = 0
        ba[i] = b

    for i in range(n):
        if ba[i] == len(pattern):
            matched_indices.append(i - 2 * len(pattern) + 1)

    return matched_indices


def run(fa_file, fq_file):
    fasta_seqs = utils.get_seq_from_file(fa_file, "fasta")
    fastq_seqs = utils.get_seq_from_file(fq_file, "fastq")

    for fastq_seq in fastq_seqs:
        for fasta_seq in fasta_seqs:
            matched_indices = run_ba(fasta_seq.seq, fastq_seq.seq)
            utils.output_sam(matched_indices, fasta_seq, fastq_seq)


def main():
    parser = argparse.ArgumentParser(description="Matches a pattern using the border-array approach")
    parser.add_argument("-fa", "--fasta-file", dest="fasta_file", default="resources/fasta_input.fa", help="fasta file")
    parser.add_argument("-fq", "--fastq-file", dest="fastq_file", default="resources/fastq_input.fq", help="fastq file")
    args = parser.parse_args()

    run(args.fasta_file, args.fastq_file)
