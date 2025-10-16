#!/bin/bash
# v9 - Formats indels with full nucleotides on one side and dashes for
#      the length difference on the other, without trimming the anchor base.

# Stop the script if any command fails
set -e

# --- 1. Configuration ---
SAMPLES=("HG004" "HG002" "HG003")

# --- Check for necessary tools ---
if ! command -v bcftools &> /dev/null; then
    echo "Error: bcftools is not installed or not in your PATH."
    exit 1
fi
if ! command -v awk &> /dev/null; then
    echo "Error: awk is not installed or not in your PATH."
    exit 1
fi

echo "Starting variant processing for ${#SAMPLES[@]} samples..."

# --- 2. Main Loop ---
for SAMPLE_ID in "${SAMPLES[@]}"; do
    echo "================================================="
    echo "Processing sample: $SAMPLE_ID"
    echo "================================================="

    # --- Variable Setup ---
    INPUT_VCF="${SAMPLE_ID}_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
    FINAL_OUTPUT="${SAMPLE_ID}_GRCh38_sorted_variants_v2.txt"
    NORMALIZED_VCF="${SAMPLE_ID}.norm.vcf.gz"
    SNPS_TXT="${SAMPLE_ID}.snps.txt"
    MNPS_TXT="${SAMPLE_ID}.mnps.txt"
    DELS_TXT="${SAMPLE_ID}.dels.txt"
    INS_TXT="${SAMPLE_ID}.ins.txt"

    if [ ! -f "$INPUT_VCF" ]; then
        echo "Warning: Input file not found for $SAMPLE_ID. Skipping."
        continue
    fi

    # --- STEP 1: Normalize VCF ---
    echo "-> Step 1/4: Normalizing VCF to split and left-align variants..."
    bcftools norm -m - "$INPUT_VCF" -Oz -o "$NORMALIZED_VCF"
    bcftools index "$NORMALIZED_VCF"

    # --- STEP 2: Query each variant type with advanced formatting ---
    echo "-> Step 2/4: Querying SNPs, MNPs, deletions, and insertions..."

    # Query Single-Nucleotide Polymorphisms (SNPs)
    bcftools query -i 'STRLEN(REF)==1 && STRLEN(ALT)==1 && TYPE="snp"' \
        -f'0,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" > "$SNPS_TXT"

    # Query Multi-Nucleotide Polymorphisms (MNPs) and filter for first letter
    bcftools query -i 'STRLEN(REF)>1 && STRLEN(REF)==STRLEN(ALT)' \
        -f'0,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" | \
        awk -F '[,/]' '{printf "%s,%s,%s,%s/%s\n", $1, $2, $3, substr($4,1,1), substr($5,1,1)}' > "$MNPS_TXT"

    # --- Reusable AWK script for advanced indel formatting ---
    AWK_INDEL_SCRIPT='
    {
        ref=$4; alt=$5;
        
        # Deletion: REF is longer than ALT
        if (length(ref) > length(alt)) {
            len_diff = length(ref) - length(alt);
            dashes = "";
            for (i=1; i<=len_diff; i++) { dashes = dashes"-" }
            ref_out = ref;
            alt_out = dashes;
        }
        # Insertion: ALT is longer than REF
        else if (length(alt) > length(ref)) {
            len_diff = length(alt) - length(ref);
            dashes = "";
            for (i=1; i<=len_diff; i++) { dashes = dashes"-" }
            ref_out = dashes;
            alt_out = alt;
        }
        # Fallback for any other case (should not be hit by bcftools query)
        else {
            ref_out = ref;
            alt_out = alt;
        }
        
        printf "%s,%s,%s,%s/%s\n", $1, $2, $3, ref_out, alt_out
    }'

    # Query Deletions and pipe to the AWK script
    bcftools query -i 'STRLEN(REF) > STRLEN(ALT)' -f'1,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" | \
        awk -F '[,/]' "$AWK_INDEL_SCRIPT" > "$DELS_TXT"

    # Query Insertions and pipe to the AWK script
    bcftools query -i 'STRLEN(REF) < STRLEN(ALT)' -f'2,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" | \
        awk -F '[,/]' "$AWK_INDEL_SCRIPT" > "$INS_TXT"

    # --- STEP 3: Concatenate ---
    echo "-> Step 3/4: Creating the unified file: $FINAL_OUTPUT..."
    cat "$SNPS_TXT" "$MNPS_TXT" "$DELS_TXT" "$INS_TXT" | sort -u > "$FINAL_OUTPUT"

    # --- STEP 4: Clean Up ---
    echo "-> Step 4/4: Cleaning up intermediate files for $SAMPLE_ID..."
    rm "$NORMALIZED_VCF" "$NORMALIZED_VCF.csi"
    rm "$SNPS_TXT" "$MNPS_TXT" "$DELS_TXT" "$INS_TXT"

    echo "Success! Unified file created: $FINAL_OUTPUT"
done

echo "================================================="
echo "All samples processed successfully."