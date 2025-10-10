# Genome Comparison Scripts

This document provides a comprehensive overview of four bash scripts designed for genome alignment and variant calling. The scripts progress from a generic tool to a highly specialized and efficient human genome comparator. The core workflow uses [**MUMmer4**](https://github.com/mummer4/mummer) for alignment and [**all2vcf**](https://github.com/MatteoSchiavinato/all2vcf) for converting results to a pseudo-VCF format.

## Tools Used

This suite of scripts relies on several command-line bioinformatics and utility tools:

* [**MUMmer4**](https://github.com/mummer4/mummer): A system for rapidly aligning entire genomes.
* [**all2vcf**](https://github.com/MatteoSchiavinato/all2vcf): A tool to convert various alignment formats to VCF.
* [**NCBI Datasets**](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/): A command-line tool for downloading data from NCBI.
* [**UCSC Genome Browser**](https://genome.ucsc.edu/): A graphical viewer and download portal for genome sequence data.
* [**bcftools**](http://www.htslib.org/download/): A set of utilities for variant calling and manipulating VCF files.
* [**Git**](https://git-scm.com/): A version control system used to download `all2vcf`.
* [**Python 3**](https://www.python.org/): The programming language required to run `all2vcf`.
* **Standard Utilities**:
  * [**wget**](https://www.gnu.org/software/wget/)
  * [**tar**](https://www.gnu.org/software/tar/)
  * [**gunzip**](https://www.gnu.org/software/gzip/)
  * [**awk**](https://www.gnu.org/software/gawk/)

-----

## 1\. `run_generic_pipeline.sh`

This is the foundational script for performing a whole-genome alignment between any two taxa available on NCBI.

* **Purpose**: Downloads two complete genomes based on their scientific names using [**NCBI Datasets**](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/), performs a single alignment of the entire reference against the target, and generates one pseudo-VCF file.
* **Usage**:

    ```bash
    ./run_generic_pipeline.sh "<Reference Taxon Name>" "<Target Taxon Name>"
    ```

* **Example**:

    ```bash
    ./run_generic_pipeline.sh "Escherichia coli" "Salmonella enterica"
    ```

* **Output**: A single VCF file, e.g., `files/output/escherichia_coli_vs_salmonella_enterica.vcf`.

-----

## 2\. `run_bacteria_pipeline.sh`

This is a hardcoded, example script demonstrating a specific use case of the generic pipeline.

* **Purpose**: Serves as a simple, ready-to-run example by automating the comparison between the reference genomes of *Escherichia coli* and *Salmonella enterica*. It requires no arguments.
* **Usage**:

    ```bash
    ./run_bacteria_pipeline.sh
    ```

* **Output**: A single VCF file named `files/bacteria_output/ecoli_vs_salmonella.vcf`.

-----

## 3\. `run_per_chromosome_pipeline.sh`

This script enhances the generic pipeline by performing the alignment on a per-chromosome basis, which is more robust for complex, multi-chromosomal genomes.

* **Purpose**: Downloads two genomes, splits each into separate FASTA files per chromosome, aligns each corresponding chromosome pair in a loop, and finally merges the individual VCFs into a single, comprehensive output file using [**bcftools**](http://www.htslib.org/download/).
* **Usage**:

    ```bash
    ./run_per_chromosome_pipeline.sh "<Reference Taxon Name>" "<Target Taxon Name>"
    ```

* **Example**:

    ```bash
    ./run_per_chromosome_pipeline.sh "Homo sapiens" "Pan troglodytes"
    ```

* **Output**: A final merged VCF file, e.g., `files/output/homo_sapiens_vs_pan_troglodytes.merged.vcf`.

-----

## 4\. `run_human_genome_comparison.sh`

This is the most advanced and efficient script, tailored specifically for comparing standard human genome assemblies by downloading chromosomes individually from the **UCSC Genome Browser**.

* **Purpose**:
  * **Direct UCSC Download**: Fetches individual chromosome files (e.g., `chr1.fa.gz`) directly from the [UCSC Genome Browser's](https://genome.ucsc.edu/) *goldenPath* server, which is often faster and more direct than using API-based tools.
  * **Efficient & Targeted**: Only downloads the specific chromosomes requested by the user in a given range. It also checks if a chromosome file already exists before downloading, saving time and bandwidth on subsequent runs.
  * **Hardcoded for hg38 vs. hg19**: The script is specifically configured to compare the `hg38` assembly (reference) against `hg19` (target).
* **Usage**:

    ```bash
    ./run_human_genome_comparison.sh [Start Chrom] [End Chrom]
    ```

* **Examples**:
  * **Compare all standard chromosomes**:

    ```bash
    ./run_human_genome_comparison.sh
    ```

  * **Compare a specific range (chromosomes 1 to 5)**:

    ```bash
    ./run_human_genome_comparison.sh 1 5
    ```

* **Output**: A merged VCF file named `files/output/hg38_vs_hg19.merged.vcf`.
