# VCF to Custom Format Conversion

This document outlines the steps to convert a high-confidence VCF file from the [Genome in a Bottle (GIAB) project](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/) into a custom, sorted, comma-separated format.

The script classifies variants as SNPs (`0`), deletions (`1`), or insertions (`2`), applies special formatting for indels, and sorts the final output.

## Prerequisites

Before you begin, ensure you have the following software installed:

1. **`bcftools`**: A powerful toolset for manipulating VCF files. If you don't have it, you can download it from the [official website](http://www.htslib.org/download/) and compile it yourself.

2. **Standard Unix Tools**: The script uses `awk` and `sort`, which are pre-installed on virtually all Linux and macOS systems.

## Input Data

You'll need a high-confidence VCF file from the GIAB project. For this guide, we'll assume you're using the recommended file for most modern applications:

* **File**: `HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz`

## Instructions

Follow these steps to generate the formatted file.

### 1. Find the Conversion Script

Locate the file named `convert_vcf.sh`.

### 2. Make the Script Executable

In your terminal, give the script permission to run with the following command:

`chmod +x convert_vcf.sh`

### 3. Run the Script

Execute the script from your terminal:

`./convert_vcf.sh`

The script will process the VCF file and create a new sorted txt file in the same directory.

## Output Format

The output file (`HG002_GRCh38_sorted_variants.txt`) will be a comma-separated file with the following columns:

| Column | Name | Description |
| :--- | :--- | :--- |
| 1 | **Flag** | A numeric flag indicating the variant type: `0` for SNP, `1` for deletion, and `2` for insertion. |
| 2 | **Chrom** | The chromosome on which the variant occurs. |
| 3 | **Pos** | The genomic position of the variant. |
| 4 | **Alleles** | The `REF/ALT` alleles, with custom dash (`-`) formatting for insertions and deletions. |