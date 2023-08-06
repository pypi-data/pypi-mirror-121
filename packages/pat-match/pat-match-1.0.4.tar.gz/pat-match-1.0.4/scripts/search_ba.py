import argparse
from scripts import utils
import timeit


def run_ba(main_str, pattern):
    border_arr_str = pattern + "$" + main_str
    n = len(border_arr_str)
    ba = [0] * n
    b = 0
    matched_indices = []

    counter = 0
    for i in range(1, n):
        while b > 0 and border_arr_str[i] != border_arr_str[b]:
            counter = counter + 1
            b = ba[b - 1]
        if border_arr_str[i] == border_arr_str[b]:
            b = b + 1
        else:
            b = 0
        ba[i] = b

    for i in range(n):
        if ba[i] == len(pattern):
            matched_indices.append(i - 2 * len(pattern) + 1)

    # print('n', len(main_str))
    # print('m', len(pattern))
    # print('Iter Count', counter)
    return matched_indices


def run(fa_file, fq_file):
    fasta_seqs = utils.get_seq_from_file(fa_file, "fasta")
    fastq_seqs = utils.get_seq_from_file(fq_file, "fastq")

    for fastq_seq in fastq_seqs:
        for fasta_seq in fasta_seqs:
            time_start = timeit.default_timer()
            matched_indices = run_ba(fasta_seq.seq, fastq_seq.seq)
            time_end = timeit.default_timer()
            # print((time_end - time_start) * 10 ** 6)
            utils.output_sam(matched_indices, fasta_seq, fastq_seq)


def main():
    parser = argparse.ArgumentParser(description="Matches a pattern using the border-array")
    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument("-fa", "-fasta-file", dest="fasta_file", help="fasta file", required=True)
    required_parser.add_argument("-fq", "-fastq-file", dest="fastq_file", help="fastq file", required=True)
    args = parser.parse_args()

    run(args.fasta_file, args.fastq_file)


if __name__ == "__main__":
    main()
