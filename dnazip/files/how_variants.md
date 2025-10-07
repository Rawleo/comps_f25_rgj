# VCF to Custom Format Conversion

This document outlines the steps to convert a high-confidence VCF file from the [Genome in a Bottle (GIAB) project](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/) into a custom, sorted, comma-separated format.

The script classifies variants as SNPs (`0`), deletions (`1`), or insertions (`2`), applies special formatting for indels, and sorts the final output.

## Prerequisites

Before you begin, ensure you have the following software installed:

1. **`bcftools`**: A powerful toolset for manipulating VCF files. If you don't have it, you can download it from the [official website](http://www.htslib.org/download/) and compile it yourself.

2. **Standard Unix Tools**: The script uses `awk` and `sort`, which are pre-installed on virtually all Linux and macOS systems.

## Input Data

You'll need a high-confidence VCF file from the GIAB project.

* **Son**: [`HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz`](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/)

* **Father**: [`HG003_GRCh38_1_22_v4.2.1_benchmark.vcf.gz `](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG003_NA24149_father/NISTv4.2.1/GRCh38/)

* **Mother**: [`HG004_GRCh38_1_22_v4.2.1_benchmark.vcf.gz`](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG004_NA24143_mother/NISTv4.2.1/GRCh38/)

## Instructions

Follow these steps to generate the formatted file.

1.  **Save** the script as `process_variants.sh`.
2.  **Make it executable**: `chmod +x process_variants.sh`
3.  **Run it** from your terminal, providing the input VCF and desired output filename as arguments:
    ```
    ./process_variant.sh /path/to/your/input.vcf.gz /path/to/your/output.txt
    ```
    For example:
    ```
    ./process_variant.sh HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz HG002_GRCh38_sorted_variants.txt
    ```

The script will process the VCF file and create a new sorted txt file in the same directory.

## Output Format

The output file (`HG002_GRCh38_sorted_variants.txt`) will be a comma-separated file with the following columns:

| Column | Name | Description |
| :--- | :--- | :--- |
| 1 | **Flag** | A numeric flag indicating the variant type: `0` for SNP, `1` for deletion, and `2` for insertion. |
| 2 | **Chrom** | The chromosome on which the variant occurs. |
| 3 | **Pos** | The genomic position of the variant. |
| 4 | **Alleles** | The `REF/ALT` alleles, with custom dash (`-`) formatting for insertions and deletions. |