#!/bin/bash
#
# ==============================================================================
#
# bio_pipeline.sh (Organized Directories & Integrated Docs Version)
#
# Description:
#   A unified script to perform common bioinformatics data preparation tasks.
#   It organizes output into directories and includes a full user guide.
#
# ==============================================================================

# --- Global Configuration ---
CHROMOSOMES=(
    "chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10"
    "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19"
    "chr20" "chr21" "chr22" "chrX" "chrY" "chrM"
)
VARIATION_DATA=(
    "HG002" "HG003" "HG004"
)
HG38_BASE_URL="https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/"
BIGBED_BASENAME="dbSnp155Common.bb"
BIGBED_URL="https://hgdownload.soe.ucsc.edu/gbdb/hg38/snp/dbSnp155Common.bb"

# --- Directory Configuration ---
CHR_DIR="chr"
DBSNP_DIR="dbSNP"
FILES_DIR="files"


# --- Core Functions ---

# Displays the basic usage instructions.
usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "A unified script for bioinformatics data preparation with organized output."
    echo ""
    echo "Commands:"
    echo "  --download-hg38                 Downloads hg38 genome files into '${CHR_DIR}/'."
    echo "  --prepare-dbsnp                 Prepares dbSNP files in '${DBSNP_DIR}/'."
    echo "  --process-giab-trio             Automatically downloads and processes the GIAB HG002, HG003, and HG004 VCFs."
    echo "  --process-vcf <in.vcf> <out.txt>  Manually processes a single VCF file from '${FILES_DIR}/'."
    echo "  --all-prep                      Runs both --download-hg38 and --prepare-dbsnp."
    echo "  --guide                         Displays the full user and methods guide."
    echo "  --help, -h                      Show this help message."
    echo ""
    exit 1
}

# Displays the detailed guide integrated from the Markdown file.
show_guide() {
cat << 'EOF'

================================================================================
 VCF to Custom Format Conversion Guide
================================================================================

This document outlines the steps to convert a high-confidence VCF file from
the Genome in a Bottle (GIAB) project into a custom, sorted, comma-separated
format.

The script classifies variants as SNPs (0), deletions (1), or insertions (2),
applies special formatting for indels, and sorts the final output.

--------------------------------------------------------------------------------
Prerequisites
--------------------------------------------------------------------------------

Before you begin, ensure you have the following software installed:

1. `bcftools`: A powerful toolset for manipulating VCF files.
2. Standard Unix Tools: The script uses `wget`, `awk`, and `sort`, which are
   pre-installed on virtually all Linux and macOS systems.

--------------------------------------------------------------------------------
Automated GIAB Trio Workflow
--------------------------------------------------------------------------------

This script can automatically download and process the high-confidence VCF
files for the GIAB Ashkenazim Trio (Son HG002, Father HG003, Mother HG004).

To run the entire automated pipeline, use the `--process-giab-trio` command:

   Example:
   ./bio_pipeline.sh --process-giab-trio

The script will perform the following steps for each of the three samples:
1.  Check if the VCF file exists in the 'files/' directory.
2.  If not found, it will download the correct file from the GIAB FTP server.
3.  Process the VCF file into the sorted, comma-separated format.
4.  Save the output to a file named 'HG00#_GRCh38_sorted_variants.txt'.

--------------------------------------------------------------------------------
Manual VCF Processing
--------------------------------------------------------------------------------

If you wish to process a different VCF file, you can still use the manual
`--process-vcf` command.

1.  Place your input VCF file (e.g., my_variants.vcf.gz) inside the 'files/'
    directory.

2.  Run the script providing the input and desired output filenames.

    Example:
    ./bio_pipeline.sh --process-vcf my_variants.vcf.gz my_processed_variants.txt

--------------------------------------------------------------------------------
Output Format Explained
--------------------------------------------------------------------------------

The output is a comma-separated text file with four columns:
Flag,Chromosome,Position,Alleles

Example line: 0,chr20,64283802,C/T

1.  **Flag**: An integer (0, 1, or 2) indicating the variant type.
    * `0`: SNP (Single Nucleotide Polymorphism) or MNP (Multi-Nucleotide Polymorphism).
    * `1`: Deletion.
    * `2`: Insertion.

2.  **Chromosome**: The chromosome identifier (e.g., `chr20`).

3.  **Position**: The 1-based genomic coordinate of the variant.

4.  **Alleles**: A representation of the reference and alternate alleles.
    * For SNPs/MNPs (`Flag 0`): `REF/ALT` (e.g., `C/T`)
    * For Deletions (`Flag 1`): `REF/---` (e.g., `GTC/---`)
    * For Insertions (`Flag 2`): `---/ALT` (e.g., `---/AAG`)

The final file is numerically sorted by Flag, then chromosomally by Position.

EOF
exit 0
}


# Checks if all required command-line utilities are installed.
check_dependencies() {
    for tool in "$@"; do
        if ! command -v "$tool" &> /dev/null; then
            echo "Error: Required utility '$tool' could not be found."
            echo "Please install it and ensure it is in your system's PATH."
            exit 1
        fi
    done
}

# --- Task 1: Download hg38 Reference Genome ---
download_genome_references() {
    echo "--- Starting Download of hg38 Chromosome Files ---"
    echo "Output directory: ./${CHR_DIR}/"
    check_dependencies "wget" "gunzip"
    mkdir -p "$CHR_DIR"

    for CHR in "${CHROMOSOMES[@]}"; do
        GZ_BASENAME="${CHR}.fa.gz"
        FA_PATH="${CHR_DIR}/${CHR}.fa"
        GZ_PATH="${CHR_DIR}/${GZ_BASENAME}"
        FULL_URL="${HG38_BASE_URL}${GZ_BASENAME}"

        echo ""
        echo "Processing ${CHR}..."

        if [ -f "$FA_PATH" ]; then
            echo "--> '${FA_PATH}' already exists. Skipping."
            continue
        fi

        echo "--> Downloading ${GZ_BASENAME}..."
        wget -q -P "$CHR_DIR" --show-progress "$FULL_URL"

        if [ $? -ne 0 ]; then
            echo "--> ERROR: Download failed for ${GZ_BASENAME}."
        else
            echo "--> Unpacking ${GZ_PATH}..."
            gunzip "$GZ_PATH"
            echo "--> Done."
        fi
    done
    echo ""
    echo "--- hg38 Chromosome Download Complete ---"
}

# --- Task 2: Prepare dbSNP Common Variants ---
prepare_dbsnp() {
    echo "--- Starting Preparation of dbSNP Data ---"
    echo "Output directory: ./${DBSNP_DIR}/"
    check_dependencies "wget" "bigBedToBed"
    mkdir -p "$DBSNP_DIR"

    local BIGBED_FILE_PATH="${DBSNP_DIR}/${BIGBED_BASENAME}"

    if [ ! -f "$BIGBED_FILE_PATH" ]; then
        echo "Input file '$BIGBED_FILE_PATH' not found. Attempting to download..."
        wget -P "$DBSNP_DIR" "$BIGBED_URL"
        if [ $? -ne 0 ]; then
            echo "Error: Download failed. Please check the URL or your network connection."
            exit 1
        fi
        echo "Download complete."
    fi

    echo "Starting batch conversion of '$BIGBED_FILE_PATH'..."
    for CHR in "${CHROMOSOMES[@]}"; do
        OUTPUT_FILE="${DBSNP_DIR}/${CHR}.txt"

        # Check if the output file already exists to avoid re-processing.
        if [ -f "$OUTPUT_FILE" ]; then
            echo "--> '${OUTPUT_FILE}' already exists. Skipping."
            continue
        fi

        echo "Extracting ${CHR} to ${OUTPUT_FILE}..."
        bigBedToBed "$BIGBED_FILE_PATH" -chrom="$CHR" "$OUTPUT_FILE"
        if [ $? -ne 0 ]; then
            echo "Warning: Command failed for ${CHR}."
        fi
    done
    echo ""
    echo "--- dbSNP Data Preparation Complete ---"
}

# --- Task 3: Process VCF File ---
process_vcf() {
    local INPUT_BASENAME="$1"
    local OUTPUT_BASENAME="$2"
    mkdir -p "$FILES_DIR"
    local INPUT_VCF="${FILES_DIR}/${INPUT_BASENAME}"
    local OUTPUT_FILE="${FILES_DIR}/${OUTPUT_BASENAME}"

    echo "--- Starting VCF Conversion for: $INPUT_VCF ---"
    check_dependencies "bcftools" "awk" "sort"

    if [ ! -f "$INPUT_VCF" ]; then
        echo "Error: Input file '$INPUT_VCF' not found."
        echo "Please ensure '$INPUT_BASENAME' is placed inside the '$FILES_DIR' directory."
        exit 1
    fi

    bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\n' "$INPUT_VCF" | \
    awk 'BEGIN { OFS="," } {
        chrom = $1; pos = $2; ref = $3;
        n_alts = split($4, alts, ",");
        for (j=1; j<=n_alts; j++) {
            alt = alts[j];
            rlen = length(ref);
            alen = length(alt);
            if (rlen == alen) {
                flag = 0; alleles = ref "/" alt; print flag, chrom, pos, alleles;
            } else if (rlen > alen) {
                flag = 1; dashes = sprintf("%*s", rlen, ""); gsub(/ /, "-", dashes);
                alleles = ref "/" dashes; print flag, chrom, pos, alleles;
            } else {
                flag = 2; inserted_seq = substr(alt, rlen + 1); ins_len = length(inserted_seq);
                dashes = sprintf("%*s", ins_len, ""); gsub(/ /, "-", dashes);
                alleles = dashes "/" inserted_seq; print flag, chrom, pos, alleles;
            }
        }
    }' | sort -t, -k1,1n -k2,2V > "$OUTPUT_FILE"

    echo "Conversion complete. Output saved to: $OUTPUT_FILE"
    echo "--- VCF Processing Complete ---"
}

# --- Task 4: Automated GIAB Trio Processing ---
process_giab_trio() {
    echo "--- Starting Automated Download & Processing of GIAB Ashkenazim Trio ---"
    check_dependencies "wget"

    # Use standard indexed arrays for bash v3 compatibility
    local SAMPLES=("HG002" "HG003" "HG004")
    local URLS=(
        "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
        "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG003_NA24149_father/NISTv4.2.1/GRCh38/HG003_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
        "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG004_NA24143_mother/NISTv4.2.1/GRCh38/HG004_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
    )

    mkdir -p "$FILES_DIR"

    # --- Step 1: Download all necessary VCF files ---
    echo "--> Checking for and downloading required VCF files..."
    for i in "${!SAMPLES[@]}"; do
        local sample=${SAMPLES[$i]}
        local vcf_url=${URLS[$i]}
        local input_vcf_basename=$(basename "$vcf_url")
        local input_vcf_path="${FILES_DIR}/${input_vcf_basename}"

        if [ ! -f "$input_vcf_path" ]; then
            echo "    -> Downloading VCF for ${sample}..."
            wget -q -P "$FILES_DIR" --show-progress "$vcf_url"
            if [ $? -ne 0 ]; then
                echo "    -> ERROR: Download failed for ${sample}."
            else
                echo "    -> Download for ${sample} complete."
            fi
        else
            echo "    -> VCF for ${sample} already exists."
        fi
    done
    echo "--> Download check complete."
    echo ""

    # --- Step 2: Verify all files exist before processing ---
    local all_files_present=true
    for vcf_url in "${URLS[@]}"; do
        local input_vcf_basename=$(basename "$vcf_url")
        local input_vcf_path="${FILES_DIR}/${input_vcf_basename}"
        if [ ! -f "$input_vcf_path" ]; then
            echo "Error: Missing VCF file '${input_vcf_basename}' after download attempt. Cannot proceed."
            all_files_present=false
        fi
    done

    if [ "$all_files_present" = false ]; then
        exit 1
    fi
    echo "--> All VCF files verified. Starting processing..."
    echo ""


    # --- Step 3: Process each VCF file ---
    for i in "${!SAMPLES[@]}"; do
        local sample=${SAMPLES[$i]}
        local vcf_url=${URLS[$i]}
        local input_vcf_basename=$(basename "$vcf_url")
        local output_txt_basename="${sample}_GRCh38_sorted_variants.txt"

        echo "==========================================================="
        echo "Processing Sample: ${sample}"
        echo "==========================================================="

        process_vcf "$input_vcf_basename" "$output_txt_basename"
    done
    echo ""
    echo "--- GIAB Trio Processing Complete ---"
}

# --- Main Script Logic: Argument Parsing ---

if [ "$#" -eq 0 ]; then
    echo "Error: No command provided."
    usage
fi

case "$1" in
    --download-hg38)
        download_genome_references
        ;;
    --prepare-dbsnp)
        prepare_dbsnp
        ;;
    --process-vcf)
        if [ "$#" -ne 3 ]; then
            echo "Error: The --process-vcf command requires an input VCF basename and an output filename."
            usage
        fi
        process_vcf "$2" "$3"
        ;;
    --process-giab-trio)
        process_giab_trio
        ;;
    --all-prep)
        download_genome_references
        echo ""
        prepare_dbsnp
        ;;
    --guide)
        show_guide
        ;;
    -h|--help)
        usage
        ;;
    *)
        echo "Error: Unknown command '$1'"
        usage
        ;;
esac

exit 0

