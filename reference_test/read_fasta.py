#!/usr/bin/env python3

# ##############################################################################
#
# File: read_fasta.py
#
# Authors:
#
# Date: October 4, 2025
#
# Description: This script parses a FASTA file from the NCBI human
#              reference genome dataset (GRCh38). It iterates through
#              each sequence record, printing its ID and length.
#
# Usage: python read_fasta.py
#
# Dependencies:
#   - BioPython: A library for computational biology.
#     Install using: pip install biopython
#
# Notes:
#   - Ensure the 'fasta_file' variable points to the correct location
#     of your '.fna' genomic file.
#
# ##############################################################################


from Bio import SeqIO

ryan_fasta_file = "/Users/ryanson/Documents/Comps/comps_repo_venvs/human_genome/GRCh38.p14/ncbi_dataset/data/GCF_000001405.40/GCF_000001405.40_GRCh38.p14_genomic.fna"

fasta_file = ryan_fasta_file

for seq_record in SeqIO.parse(fasta_file, "fasta"):
    print("ID:", seq_record.id)
    print("Length:", len(seq_record))
    # You can also access the sequence itself:
    print("Sequence:", repr(seq_record.seq))