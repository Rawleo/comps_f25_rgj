# Guide: Genomic Data Preparation Pipeline

This document outlines a three-step command-line pipeline for preparing genomic data, which involves downloading a reference genome, extracting SNP data, and converting variant files.

The process uses three separate shell scripts:

1.  `download_hg_38.sh`
2.  `create_db_snps.sh`
3.  `process_variants.sh`

## Step 1: Download the Reference Genome

This script automates the download and decompression of all standard human chromosome FASTA files from the UCSC Genome Browser.

### How to Use

1.  **Save** the script as `download_hg_38.sh`.
2.  **Make it executable**: `chmod +x download_hg_38.sh`
3.  **Run it**: `./download_hg_38.sh`

## Step 2: Create dbSNP Files

This script extracts SNP data for each chromosome from a pre-downloaded `bigBed` file from UCSC.

### Prerequisites

You must have the `bigBedToBed` utility installed, which is part of the UCSC Kent command-line utilities.

### How to Use

1.  **Download** the `dbSnp155Common.bb` file from the [UCSC downloads page](https://www.google.com/search?q=http://hgdownload.soe.ucsc.edu/gbdb/hg38/snp/dbSnp155Common.bb).
2.  **Save** the script as `create_db_snps.sh`.
3.  **Make it executable**: `chmod +x create_db_snps.sh`
4.  **Run it**: `./create_db_snps.sh`

## Step 3: Process and Format VCF File

This script uses `bcftools` and `awk` to convert a VCF file into a specific, sorted, comma-separated format. It classifies each variant as a SNP/MNP (flag 0), a deletion (flag 1), or an insertion (flag 2).

### Prerequisites

You must have **`bcftools`** installed and available in your system's PATH.

### How to Use

1.  **Save** the script as `process_variants.sh`.
2.  **Make it executable**: `chmod +x process_variants.sh`
3.  **Run it** from your terminal, providing the input VCF and desired output filename as arguments:
    ```
    ./process_variant.sh /path/to/your/input.vcf.gz /path/to/your/output.txt
    ```
    For example:
    ```
    ./process_variant.sh HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz HG002_processed.txt
    ```

## Important Notes

This pipeline is designed to be run in a Unix-like environment (such as Linux or macOS) where shell scripts and standard command-line utilities are available.

> Ensure all necessary files, like the `dbSnp155Common.bb` file, are in the correct directory before running the scripts that depend on them.