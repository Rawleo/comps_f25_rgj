#!/bin/bash

# --- Configuration ---
# The name of the input bigBed file.
# Make sure this file is in the same directory as the script, or provide a full path.
BIGBED_FILE="dbSnp155Common.bb"

# A list of chromosomes to process.
# We'll use the standard set for hg38.
CHROMOSOMES=(
    "chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10"
    "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19"
    "chr20" "chr21" "chr22" "chrX" "chrY" "chrM"
)

# --- Script Logic ---

# 1. Check if the bigBedToBed utility is installed and available in the PATH.
if ! command -v bigBedToBed &> /dev/null
then
    echo "Error: The 'bigBedToBed' utility could not be found."
    echo "Please download the UCSC Kent command-line utilities and ensure they are in your system's PATH."
    exit 1
fi

# 2. Check if the input bigBed file exists.
if [ ! -f "$BIGBED_FILE" ]; then
    echo "Error: Input file '$BIGBED_FILE' not found."
    echo "Please place the file in the same directory as this script or update the BIGBED_FILE variable."
    exit 1
fi

echo "Starting batch conversion of '$BIGBED_FILE'..."

# 3. Loop through each chromosome in the array.
for CHR in "${CHROMOSOMES[@]}"
do
    OUTPUT_FILE="${CHR}.txt"
    echo "Extracting ${CHR} to ${OUTPUT_FILE}..."

    # Run the bigBedToBed command for the current chromosome.
    bigBedToBed "$BIGBED_FILE" -chrom="$CHR" "$OUTPUT_FILE"

    # Optional: Check if the command was successful before continuing.
    if [ $? -ne 0 ]; then
        echo "Warning: Command failed for ${CHR}."
    fi
done

echo "-------------------------------------"
echo "All chromosomes processed successfully."
