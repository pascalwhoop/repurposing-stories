#!/bin/bash
#
# Batch Production Script for Drug Repurposing Podcast Episodes
#
# This script contains Claude Code invocations for all pending episodes.
# Run lines one-by-one to test, or uncomment the loop at the bottom to run all.
#
# Usage:
#   ./batch_produce_episodes.sh                     # Interactive mode (prints commands)
#   ./batch_produce_episodes.sh --auto              # Run all episodes sequentially
#   bash -x batch_produce_episodes.sh --auto        # Run with debug output
#
# Or run individual lines manually:
#   claude "Create an episode for Aspirin and Cardiovascular Disease Prevention"
#

set -e # Exit on error
set -o pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Drug Repurposing Podcast Batch Producer${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Default options
MODE="interactive"

# Parse args
for arg in "$@"; do
  case "$arg" in
  --auto) MODE="auto" ;;
  *)
    echo -e "${RED}Unknown argument: $arg${NC}"
    echo "Usage: ./batch_produce_episodes.sh [--auto]"
    exit 1
    ;;
  esac
done

# Build runner command as an array
CLAUDE_CMD=(claude --dangerously-skip-permissions)
CLAUDE_STREAM_FLAGS=(--print --verbose --output-format=stream-json)

ensure_jq() {
  if ! command -v jq >/dev/null 2>&1; then
    echo -e "${RED}jq is required for streaming output but was not found.${NC}"
    echo "Install it with: brew install jq"
    return 1
  fi
}

stream_claude_human() {
  local prompt="$1"

  set -o pipefail
  "${CLAUDE_CMD[@]}" "${CLAUDE_STREAM_FLAGS[@]}" "$prompt" |
    while IFS= read -r line; do
      # Show assistant text when present
      text=$(echo "$line" | jq -r '
        if .type == "assistant" then
          .message.content[]? | select(.type == "text") | .text // empty
        else
          empty
        end
      ' 2>/dev/null)
      if [ -n "$text" ]; then
        echo "$text"
      fi

      # Show tool use updates for feedback (optional, but useful)
      tool_line=$(echo "$line" | jq -r '
        if .type == "assistant" then
          .message.content[]? | select(.type == "tool_use") |
          ("[tool] " + (.name // "unknown"))
        else
          empty
        end
      ' 2>/dev/null)
      if [ -n "$tool_line" ]; then
        echo "$tool_line"
      fi
    done
}

format_cmd() {
  local out=""
  for part in "$@"; do
    out+=$(printf '%q ' "$part")
  done
  echo "${out% }"
}

# Array of episodes to produce (excluding completed: minoxidil-alopecia, rituximab-ms, sirolimus-lymphangioleiomyomatosis)
declare -a EPISODES=(
  #"Aspirin and Cardiovascular Disease Prevention" COMPLETED
  # "Dexamethasone and COVID-19 Severe"
  # "Zidovudine and HIV AIDS"
  # "Sildenafil and Erectile Dysfunction"
  # "Thalidomide and Multiple Myeloma"
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
  # Streaming output: human-readable text + tool use updates
  if ensure_jq && stream_claude_human "Create an episode for $episode"; then
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
echo "Mode: ${MODE}"
if [ "$MODE" = "auto" ]; then
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
    printf '%s %q\n' \
      "$(format_cmd "${CLAUDE_CMD[@]}" "${CLAUDE_STREAM_FLAGS[@]}")" \
      "Create an episode for $episode"
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
