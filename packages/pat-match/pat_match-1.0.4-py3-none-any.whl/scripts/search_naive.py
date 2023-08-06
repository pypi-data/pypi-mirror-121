import argparse
from scripts import utils
import timeit


def run_naive(main_str, pattern):
    ms_len = len(main_str)
    ss_len = len(pattern)
    matched_indices = []
    counter = 0
    if ss_len > ms_len:
        return matched_indices
    if ss_len == 0:
        return matched_indices

    for i in range(ms_len - ss_len + 1):
        j = 0
        while j < ss_len:
            counter = counter + 1
            if main_str[i + j] != pattern[j]:
                break
            j = j + 1
        if j == ss_len:
            matched_indices.append(i + 1)

    # print('n', ms_len)
    # print('m', ss_len)
    # print('Iter Count', counter)
    return matched_indices


def run(fa_file, fq_file):
    fasta_seqs = utils.get_seq_from_file(fa_file, "fasta")
    fastq_seqs = utils.get_seq_from_file(fq_file, "fastq")

    for fastq_seq in fastq_seqs:
        for fasta_seq in fasta_seqs:
            time_start = timeit.default_timer()
            matched_indices = run_naive(fasta_seq.seq, fastq_seq.seq)
            time_end = timeit.default_timer()

            # print((time_end - time_start) * 10 ** 6)

            utils.output_sam(matched_indices, fasta_seq, fastq_seq)


def main():
    parser = argparse.ArgumentParser(description="Matches a pattern using the naive")
    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument("-fa", "-fasta-file", dest="fasta_file", help="fasta file", required=True)
    required_parser.add_argument("-fq", "-fastq-file", dest="fastq_file", help="fastq file", required=True)
    args = parser.parse_args()

    run(args.fasta_file, args.fastq_file)


if __name__ == "__main__":
    main()
