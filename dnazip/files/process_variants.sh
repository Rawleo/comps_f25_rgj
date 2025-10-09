#!/bin/bash

# --- Usage function ---
# This function displays instructions on how to run the script.
usage() {
    echo "Usage: $0 <input.vcf.gz> <output.txt>"
    echo "Processes a VCF file into a sorted, comma-separated format with variant flags."
    echo "  <input.vcf.gz>: Path to the input VCF file (can be gzipped)."
    echo "  <output.txt>: Path for the resulting text file."
    exit 1
}

# --- Argument Parsing ---
# Check if exactly two arguments (input and output file) are provided.
if [ "$#" -ne 2 ]; then
    echo "Error: Incorrect number of arguments provided."
    usage
fi

INPUT_VCF="$1"
OUTPUT="$2"

# --- Pre-run Checks ---
# Check if bcftools is installed and available in the system's PATH.
if ! command -v bcftools &> /dev/null
then
    echo "Error: 'bcftools' could not be found."
    echo "Please install bcftools and ensure it is in your system's PATH to continue."
    exit 1
fi

# Check if the input VCF file exists before proceeding.
if [ ! -f "$INPUT_VCF" ]; then
    echo "Error: Input file '$INPUT_VCF' not found."
    echo "Please provide a valid path to your VCF file."
    exit 1
fi

# --- Main Pipeline ---
# This command chain converts the VCF to the desired format and sorts it.

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
