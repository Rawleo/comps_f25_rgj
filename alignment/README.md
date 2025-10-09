# Automated Genome Comparison Pipeline

This script automates the process of downloading two genomes, aligning them with [**MUMmer4**](https://mummer4.github.io/), and generating a pseudo-VCF file using [**all2vcf**](https://github.com/MatteoSchiavinato/all2vcf).

Simply provide the scientific names of two taxa, and the pipeline does the rest—from download to variant calling.

---

## Tools Used

| Tool            | Description                                     | Link                                                                 |
|-----------------|-------------------------------------------------|----------------------------------------------------------------------|
| `datasets`      | NCBI CLI for downloading genomic data           | <https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/> |
| `MUMmer4`       | Genome alignment toolkit                        | <https://github.com/mummer4/mummer>                                  |
| `nucmer`        | MUMmer tool for aligning two genome sequences   | Included in MUMmer4                                                 |
| `delta-filter`  | Filters alignment blocks from `nucmer` output   | Included in MUMmer4                                                 |
| `show-snps`     | Extracts SNPs and indels from delta files       | Included in MUMmer4                                                 |
| `all2vcf`       | Converts alignment output into VCF-like format  | <https://github.com/MatteoSchiavinato/all2vcf>                      |
| `python3` + `pip` | Required for running `all2vcf`                 | <https://www.python.org/downloads/>                                   |
| `git`           | Used to clone the `all2vcf` repo                | <https://git-scm.com/downloads>                                       |

---

## Prerequisites

Before using the script, make sure the following are installed and available in your `PATH`:

### Command-Line Tools
- `git`
- `python3` and `pip`
- [NCBI `datasets` CLI](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/)
- [**MUMmer4** suite](https://mummer4.github.io/):  
  - `nucmer`  
  - `delta-filter`  
  - `show-snps`

### Python Dependencies
The script uses a `requirements.txt` to set up a virtual environment for [`all2vcf`](https://github.com/MatteoSchiavinato/all2vcf). Make sure the following file exists:

```
requirements.txt
```

```text
Bio==1.8.0
biopython==1.85
pandas==2.3.3
```

---

## Directory Structure

Start with this structure:

```
alignment/
├── run_generic_pipeline.sh
└── requirements.txt
```

After execution, the pipeline will generate:

```
alignment/
├── run_generic_pipeline.sh
├── requirements.txt
├── all2vcf/                     # Cloned GitHub repo
├── files/
│   ├── genomes/
│   │   ├── reference_genome.fna
│   │   └── target_genome.fna
│   └── output/
│       ├── ref_vs_target.delta
│       ├── ref_vs_target.filtered.delta
│       ├── ref_vs_target.snps
│       └── ref_vs_target.vcf
```

---

## Usage

### 1. Make the Script Executable

```bash
chmod +x run_generic_pipeline.sh
```

### 2. Run the Pipeline

```bash
./run_generic_pipeline.sh "<Reference Taxon Name>" "<Target Taxon Name>"
```

### Example

Compare *Pseudomonas aeruginosa* with *Pseudomonas fluorescens*:

```bash
./run_generic_pipeline.sh "Pseudomonas aeruginosa" "Pseudomonas fluorescens"
```

---

## Pipeline Workflow

Here’s what the script does step by step:

1. **Dependency Check**  
   Ensures required tools and Python are available.

2. **Directory Setup**  
   Creates working directories under `files/`.

3. **Genome Download**  
   Fetches genome assemblies via NCBI `datasets` CLI.

4. **all2vcf Installation**  
   Clones the `all2vcf` repo and sets up a virtual environment.

5. **Genome Alignment**  
   Uses `nucmer` from MUMmer4 to align genomes.

6. **Delta Filtering**  
   Filters for 1-to-1 alignments using `delta-filter`.

7. **SNP Extraction**  
   Generates SNP data using `show-snps`.

8. **VCF Conversion**  
   Converts SNPs to VCF format using `all2vcf`.

---

## Output

Your final result will be a VCF-like file:

```
files/output/ref_vs_target.vcf
```

This file represents the genomic variants between the reference and target genomes in standard VCF format (as close as possible, given the pseudo nature of the data).

---
