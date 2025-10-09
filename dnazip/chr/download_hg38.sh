#!/bin/bash
#
# Description:
# This script downloads all standard chromosome FASTA files for the hg38
# human genome assembly from the UCSC Genome Browser's goldenPath.
# After downloading, it unpacks each .gz file.
#
# Usage:
# 1. Save this script as download_hg38.sh
# 2. Make it executable: chmod +x download_hg38.sh
# 3. Run it: ./download_hg38.sh

# --- Configuration ---

# The base URL for the hg38 chromosome files.
BASE_URL="https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/"

# A list of the standard chromosomes to download.
# This includes autosomes (1-22), sex chromosomes (X, Y), and the mitochondrial chromosome (M).
CHROMOSOMES=(
    "chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10"
    "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19"
    "chr20" "chr21" "chr22" "chrX" "chrY" "chrM"
)

# --- Script Logic ---

# 1. Check if 'wget' is installed.
if ! command -v wget &> /dev/null
then
    echo "Error: 'wget' is not installed. Please install it to continue."
    exit 1
fi

# 2. Check if 'gunzip' is installed.
if ! command -v gunzip &> /dev/null
then
    echo "Error: 'gunzip' is not installed. Please install it to continue."
    exit 1
fi

echo "Starting download of hg38 chromosome files..."
echo "=============================================="

# 3. Loop through each chromosome in the array.
for CHR in "${CHROMOSOMES[@]}"
do
    # Define the compressed filename and the final uncompressed filename.
    GZ_FILE="${CHR}.fa.gz"
    FA_FILE="${CHR}.fa"
    FULL_URL="${BASE_URL}${GZ_FILE}"

    echo ""
    echo "Processing ${CHR}..."

    # Check if the uncompressed file already exists to avoid re-downloading.
    if [ -f "$FA_FILE" ]; then
        echo "--> '${FA_FILE}' already exists. Skipping."
        continue
    fi

    # Download the file using wget.
    echo "--> Downloading ${GZ_FILE}..."
    wget -q --show-progress "$FULL_URL"

    # Check if the download was successful.
    if [ $? -ne 0 ]; then
        echo "--> ERROR: Download failed for ${GZ_FILE}. Please check your connection or the URL."
    else
        # If download was successful, unpack the file.
        echo "--> Unpacking ${GZ_FILE}..."
        gunzip "$GZ_FILE"
        echo "--> Done."
    fi
done

echo ""
echo "=============================================="
echo "All chromosome downloads are complete."
