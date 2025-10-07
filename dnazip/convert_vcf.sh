#!/bin/bash

# --- Configuration ---
# Set the input and output filenames here.
# Please update INPUT_VCF to the correct path for your system.
# bcftools should also be added to your $PATH variable.

INPUT_VCF="HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
OUTPUT="HG002_GRCh38_sorted_variants.txt"

# --- Main Pipeline ---
# This command chain converts the VCF to the desired format and sorts it.
# It is designed to be run from the command line.

echo "Starting VCF conversion for: $INPUT_VCF"

bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\n' "$INPUT_VCF" | \
awk 'BEGIN { OFS="," } {
    chrom = $1; pos = $2; ref = $3;
    n_alts = split($4, alts, ",");

    for (j=1; j<=n_alts; j++) {
        alt = alts[j];
        rlen = length(ref);
        alen = length(alt);

        # Flag 0: SNP/MNP
        if (rlen == alen) {
            flag = 0;
            alleles = ref "/" alt;
            print flag, chrom, pos, alleles;
        }
        # Flag 1: Deletion
        else if (rlen > alen) {
            flag = 1;
            dashes = sprintf("%*s", rlen, ""); gsub(/ /, "-", dashes);
            alleles = ref "/" dashes;
            print flag, chrom, pos, alleles;
        }
        # Flag 2: Insertion
        else {
            flag = 2;
            inserted_seq = substr(alt, rlen + 1);
            ins_len = length(inserted_seq);
            dashes = sprintf("%*s", ins_len, ""); gsub(/ /, "-", dashes);
            alleles = dashes "/" inserted_seq;
            print flag, chrom, pos, alleles;
        }
    }
}' | sort -t, -k1,1n -k2,2V > "$OUTPUT"

echo "Conversion complete. Output saved to: $OUTPUT"