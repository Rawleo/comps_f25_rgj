#!/bin/bash

# --- Configuration ---
# The name of the input bigBed file.
BIGBED_FILE="dbSnp155Common.bb"
# The URL to download the file from if it's missing.
BIGBED_URL="https://hgdownload.soe.ucsc.edu/gbdb/hg38/snp/dbSnp155Common.bb"

# A list of chromosomes to process.
CHROMOSOMES=(
    "chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10"
    "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19"
    "chr20" "chr21" "chr22" "chrX" "chrY" "chrM"
)

# --- Script Logic ---

# 1. Check if required utilities are installed.
if ! command -v bigBedToBed &> /dev/null
then
    echo "Error: The 'bigBedToBed' utility could not be found."
    echo "Please download the UCSC Kent command-line utilities and ensure they are in your system's PATH."
    exit 1
fi

# 2. Check if the input bigBed file exists and download it if not.
if [ ! -f "$BIGBED_FILE" ]; then
    echo "Input file '$BIGBED_FILE' not found. Attempting to download..."

    # Check for wget before attempting to download
    if ! command -v wget &> /dev/null
    then
        echo "Error: 'wget' is not installed. Please install wget or download the file manually from:"
        echo "$BIGBED_URL"
        exit 1
    fi

    # Download the file using the URL
    wget "$BIGBED_URL"

    # Verify that the download was successful
    if [ $? -ne 0 ]; then
        echo "Error: Download failed. Please check the URL or your network connection."
        exit 1
    fi
    echo "Download complete."
fi

echo "Starting batch conversion of '$BIGBED_FILE'..."

# 3. Loop through each chromosome in the array.
for CHR in "${CHROMOSOMES[@]}"
do
    OUTPUT_FILE="${CHR}.txt"
    echo "Extracting ${CHR} to ${OUTPUT_FILE}..."

    # Run the bigBedToBed command for the current chromosome.
    bigBedToBed "$BIGBED_FILE" -chrom="$CHR" "$OUTPUT_FILE"

    # Optional: Check if the command was successful.
    if [ $? -ne 0 ]; then
        echo "Warning: Command failed for ${CHR}."
    fi
done

echo "-------------------------------------"
echo "All chromosomes processed successfully."