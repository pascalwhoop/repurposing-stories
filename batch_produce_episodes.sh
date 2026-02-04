#!/bin/bash
#
# Batch Production Script for Drug Repurposing Podcast Episodes
#
# This script contains Claude Code invocations for all pending episodes.
# Run lines one-by-one to test, or uncomment the loop at the bottom to run all.
#
# Usage:
#   ./batch_produce_episodes.sh          # Run all episodes sequentially
#   bash -x batch_produce_episodes.sh    # Run with debug output
#
# Or run individual lines manually:
#   claude "Create an episode for Aspirin and Cardiovascular Disease Prevention"
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Drug Repurposing Podcast Batch Producer${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Array of episodes to produce (excluding completed: minoxidil-alopecia, rituximab-ms, sirolimus-lymphangioleiomyomatosis)
declare -a EPISODES=(
    "Aspirin and Cardiovascular Disease Prevention"
    "Dexamethasone and COVID-19 Severe"
    "Zidovudine and HIV AIDS"
    "Sildenafil and Erectile Dysfunction"
    "Thalidomide and Multiple Myeloma"
    "Methotrexate and Rheumatoid Arthritis"
    # Minoxidil-Alopecia COMPLETED
    "Botulinum Toxin and Chronic Migraine"
    "Finasteride and Androgenetic Alopecia"
    "Imatinib and GIST Stromal Tumors"
    "Metformin and PCOS"
    "Propranolol and Infantile Hemangioma"
    # Rituximab-MS COMPLETED
    "Ketamine and Depression TRD"
    "Spironolactone and Heart Failure"
    "Amantadine and Parkinsons Disease"
    "Colchicine and Pericarditis"
    "Dimethyl Fumarate and Multiple Sclerosis"
    "Topiramate and Migraine Prophylaxis"
    "Gabapentin and Neuropathic Pain"
    "Bupropion and Smoking Cessation"
    "Hydroxychloroquine and Lupus"
    "Amphotericin B and Visceral Leishmaniasis"
    "Raloxifene and Breast Cancer Prevention"
    "Sildenafil and Pulmonary Hypertension"
    "Miltefosine and Visceral Leishmaniasis"
    # Sirolimus-Lymphangioleiomyomatosis COMPLETED
    "Eflornithine and Sleeping Sickness"
    "Pregabalin and Generalized Anxiety Disorder"
    "Duloxetine and Stress Urinary Incontinence"
)

# Function to produce a single episode
produce_episode() {
    local episode="$1"
    local index="$2"
    local total="$3"

    echo -e "${BLUE}[$index/$total] Starting: $episode${NC}"
    echo "--------------------"

    # Invoke Claude Code with the podcast-producer skill
    # The skill should automatically trigger when we phrase it this way
    if claude "Create an episode for $episode"; then
        echo -e "${GREEN}✓ Success: $episode${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}✗ Failed: $episode${NC}"
        echo -e "${RED}  Check for PRODUCTION_ERROR.md in the story directory${NC}"
        echo ""
        return 1
    fi
}

# Main execution
echo "Total episodes to produce: ${#EPISODES[@]}"
echo ""
echo "Mode: ${1:-interactive}"
echo ""

if [ "$1" = "--auto" ]; then
    # Automatic batch mode - run all episodes
    echo -e "${BLUE}Running in AUTOMATIC mode...${NC}"
    echo ""

    success_count=0
    fail_count=0

    for i in "${!EPISODES[@]}"; do
        index=$((i + 1))
        episode="${EPISODES[$i]}"

        if produce_episode "$episode" "$index" "${#EPISODES[@]}"; then
            ((success_count++))
        else
            ((fail_count++))
            # Continue to next episode even on failure
        fi

        # Small delay between episodes to avoid rate limits
        if [ $index -lt ${#EPISODES[@]} ]; then
            echo "Waiting 10 seconds before next episode..."
            sleep 10
        fi
    done

    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Batch Production Complete${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}Successful: $success_count${NC}"
    echo -e "${RED}Failed: $fail_count${NC}"
    echo ""
    echo "Search for errors with: grep -r 'TODO' stories/"

else
    # Interactive mode - print commands for manual execution
    echo -e "${BLUE}Running in INTERACTIVE mode...${NC}"
    echo ""
    echo "Copy and paste these commands one at a time:"
    echo "================================================"
    echo ""

    for i in "${!EPISODES[@]}"; do
        index=$((i + 1))
        episode="${EPISODES[$i]}"
        echo "# Episode $index of ${#EPISODES[@]}"
        echo "claude \"Create an episode for $episode\""
        echo ""
    done

    echo "================================================"
    echo ""
    echo "To run ALL episodes automatically (overnight):"
    echo "  ./batch_produce_episodes.sh --auto"
    echo ""
    echo "To run with verbose output:"
    echo "  bash -x ./batch_produce_episodes.sh --auto"
fi
