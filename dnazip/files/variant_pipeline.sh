#!/bin/bash
# v3 - Correctly handles multi-allelic sites by normalizing first.

# Stop the script if any command fails
set -e

# --- 1. Configuration ---
SAMPLES=("HG002" "HG003" "HG004")

# --- Check for bcftools installation ---
if ! command -v bcftools &> /dev/null; then
    echo "Error: bcftools is not installed or not in your PATH. Please install it to continue."
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
    FINAL_OUTPUT="${SAMPLE_ID}_GRCh38_sorted_variants.txt"
    
    # Define temporary files for this loop
    NORMALIZED_VCF="${SAMPLE_ID}.norm.vcf.gz"
    SNPS_TXT="${SAMPLE_ID}.snps.txt"
    DELS_TXT="${SAMPLE_ID}.dels.txt"
    INS_TXT="${SAMPLE_ID}.ins.txt"

    if [ ! -f "$INPUT_VCF" ]; then
        echo "Warning: Input file not found for $SAMPLE_ID. Skipping."
        continue
    fi

    # --- STEP 1: Normalize VCF to split multi-allelic sites ---
    # This is the most critical step. The '-m -' flag splits multi-allelic
    # sites into separate, simple VCF records.
    echo "-> Step 1/4: Normalizing VCF to split complex variants..."
    bcftools norm -m - "$INPUT_VCF" -Oz -o "$NORMALIZED_VCF"
    bcftools index "$NORMALIZED_VCF"

    # --- STEP 2: Query each variant type directly from the NORMALIZED file ---
    # Instead of creating intermediate VCFs, we run include and query in one step.
    # This is more efficient and prevents errors.
    echo "-> Step 2/4: Querying SNPs, deletions, and insertions..."
    
    # Query SNPs (0)
    bcftools query -i 'TYPE="snp"' -f'0,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" > "$SNPS_TXT"
    
    # Query Deletions (1)
    bcftools query -i 'STRLEN(REF) > STRLEN(ALT)' -f'1,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" > "$DELS_TXT"
    
    # Query Insertions (2)
    bcftools query -i 'STRLEN(REF) < STRLEN(ALT)' -f'2,%CHROM,%POS,%REF/%ALT\n' "$NORMALIZED_VCF" > "$INS_TXT"

    # --- STEP 3: Concatenate and create the final unique file ---
    echo "-> Step 3/4: Creating the unified file: $FINAL_OUTPUT..."
    cat "$SNPS_TXT" "$DELS_TXT" "$INS_TXT" | sort -u > "$FINAL_OUTPUT"

    # --- STEP 4: Clean Up ---
    echo "-> Step 4/4: Cleaning up intermediate files for $SAMPLE_ID..."
    rm "$NORMALIZED_VCF" "$NORMALIZED_VCF.csi"
    rm "$SNPS_TXT" "$DELS_TXT" "$INS_TXT"

    echo "Success! Unified file created: $FINAL_OUTPUT"
done

echo "================================================="
echo "All samples processed successfully."
