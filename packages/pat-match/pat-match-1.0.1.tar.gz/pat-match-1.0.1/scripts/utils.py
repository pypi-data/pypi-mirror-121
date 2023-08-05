from Bio import SeqIO


# THE PARSER
# reads and returns the seq as string from the FASTA file
def get_seq_from_file(file_path, fmt="fasta"):
    seqs = []

    for seq_record in SeqIO.parse(file_path, fmt):
        seqs.append(seq_record)

    return seqs


def output_sam(matched_indices, fasta_seq, fastq_seq):
    if len(matched_indices) != 0:
        for matched_idx in matched_indices:
            # TODO: replace the print statement with proper SAM output logic
            print(f"{fastq_seq.seq}\t0\t{fasta_seq.description}\t{matched_idx}\t0\t", str(len(fastq_seq.seq))+'M', f"\t*\t0\t0\t{fastq_seq.seq}\t{len(fastq_seq.seq)*'~'}")
