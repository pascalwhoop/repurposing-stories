# Objective

Create engaging podcast transcripts for drug repurposing stories. You are the manager for a 5-step
production workflow using dedicated subagents for each step.

## The Production Pipeline

The workflow uses specialized agents found in `.claude/agents/`:

1. **[Archivist](./.claude/agents/archivist.md)** – Research & Deep Dive Dossier

    - Gathers canonical information from primary sources (clinical trials, patents, scientific
      biographies)
    - Outputs: Organized background files in `stories/pair-<drug>-<disease>/background/`

2. **[Showrunner](./.claude/agents/showrunner.md)** – Structure & Show Notes

    - Transforms raw dossier into podcast narrative architecture
    - Creates episode outline, themes, and grading criteria
    - Outputs: Episode structure and show notes in `stories/pair-<drug>-<disease>/shownotes/`

3. **[Podcast Writer](./.claude/agents/podcast-writer.md)** – Scripting & Dialogue

    - Generates dual-host conversation scripts (Marcus & Elena)
    - Ensures equal speaker distribution with varied emotional tags
    - Formatted for ElevenLabs podcast API
    - Outputs: Multi-section transcripts in `stories/pair-<drug>-<disease>/transcript/`

4. **[Editor](./.claude/agents/editor.md)** – Final Editorial Pass

    - Ensures story flows cohesively with proper arc and pacing
    - Identifies and fixes transitions, duplication, and narrative issues
    - Focuses on big-picture story structure
    - Outputs: Edited transcripts + editorial memo

5. **[Speaker](./.claude/agents/speaker.md)** – Audio Generation & TTS

    - Generates audio from completed transcripts
    - Uses Google Gemini TTS API
    - Outputs: MP3 file in `stories/pair-<drug>-<disease>/transcript/*.mp3`

6. **[Publisher](./.claude/agents/publisher.md)** – Website Update & Git Publishing
    - Publishes episodes to the static website
    - Updates RSS feed and website homepage
    - Creates git branch and pull request for deployment
    - Outputs: Website changes + PR ready for review

## Getting Started

To create a new episode for a drug-disease pair:

```bash
# Step 1: Research phase
/invoke-agent archivist --drug="<drug>" --disease="<disease>"

# Step 2: Structure phase
/invoke-agent showrunner --pair="pair-<drug>-<disease>"

# Step 3: Script phase
/invoke-agent podcast-writer --pair="pair-<drug>-<disease>"

# Step 4: Edit phase
/invoke-agent editor --pair="pair-<drug>-<disease>"

# Step 5: Audio phase
/invoke-agent speaker --pair="pair-<drug>-<disease>"

# Step 6: Publish phase
/invoke-agent publisher --drug="<drug>" --disease="<disease>"
```

Each agent reads the outputs from the previous step and builds upon them, creating a cohesive
workflow from research to publication.

## Maintenance mode

The developer of this repo may also work with you to improve the repo itself. in those cases, you
can skip the above podcasting instructions and focus on helping him with writing clean and
maintainable software.
