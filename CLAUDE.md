# Objective

Create engaging podcast transcripts for drug repurposing stories using an automated production
pipeline orchestrated by a Claude Skill.

## The Production Pipeline

The workflow uses the **podcast-producer skill** to automatically orchestrate specialized agents
found in `.claude/agents/`:

1. **[Archivist](./.claude/agents/archivist.md)** – Research & Deep Dive Dossier
    - Gathers canonical information from primary sources using domain tools first (PubMed,
      ClinicalTrials.gov, bioRxiv/medRxiv, patents, FDA/EMA docs), then fills gaps with web search
    - Outputs: Organized background files in `stories/pair-<drug>-<disease>/background/`

2. **[Showrunner](./.claude/agents/showrunner.md)** – Structure & Show Notes
    - Chooses the narrative arc based on evidence and shapes the episode structure
    - Creates episode outline, themes, and grading criteria
    - Outputs: Episode structure and show notes in `stories/pair-<drug>-<disease>/shownotes/`

3. **[Podcast Writer](./.claude/agents/podcast-writer.md)** – Scripting & Dialogue
    - Generates dual-host conversation scripts (Marcus & Elena) following showrunner structure
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

6. **[Feedback](./.claude/agents/feedback.md)** – Continuous Quality Improvement
    - Analyzes listener feedback from completed episodes
    - Updates agent instructions to improve future episodes
    - Tracks quality improvements over time
    - Outputs: Updated agent instructions + improvement log

7. **[Publisher](./.claude/agents/publisher.md)** – Website Update & Git Publishing _(manual step)_
    - Publishes episodes to the static website
    - Updates RSS feed and website homepage
    - Creates git branch and pull request for deployment
    - Outputs: Website changes + PR ready for review

## Getting Started

### Single Episode Production (Automatic)

The podcast-producer skill orchestrates the entire pipeline automatically:

```bash
# Simple invocation - skill handles everything
Create an episode for [Drug] and [Disease]

# Examples:
Create an episode for Aspirin and Cardiovascular Disease Prevention
Produce the Metformin PCOS episode
Generate podcast for Ketamine treating Depression
```

The skill will:
1. Run all 5 agents sequentially (archivist → showrunner → podcast-writer → editor → speaker)
2. Verify each agent's output
3. Commit work to git (no push)
4. Report completion or create error file with TODO marker

### Batch Production

Use the batch script to produce multiple episodes:

```bash
# Interactive mode - prints commands to run manually
./batch_produce_episodes.sh

# Automatic mode - runs all episodes overnight
./batch_produce_episodes.sh --auto
```

The script contains 27 pending episodes from `stories/pairs_gemini.md`.

### Partial Production (Advanced)

Stop at a specific step:
```bash
Create an episode for Aspirin and Cardiovascular Disease, but stop after showrunner
Only run archivist for Metformin and PCOS
```

Resume from a specific step:
```bash
Continue podcast production for Aspirin and Cardiovascular Disease from editor step
```

Re-run a single agent:
```bash
Regenerate audio for Aspirin and Cardiovascular Disease
Re-run the podcast-writer for Metformin and PCOS
```

### Quality Improvement Workflow

After completing 2-3 episodes:

1. Collect listener feedback in `stories/pair-<drug>-<disease>/feedback.md`
2. Run feedback agent to analyze patterns and update instructions
3. Future episodes benefit from improved agent instructions

The feedback agent is run separately, not as part of the automatic pipeline.

### Publishing (Manual)

After reviewing the episode audio:

```bash
# Run publisher agent separately
/invoke-agent publisher --drug="<drug>" --disease="<disease>"
```

This creates a PR with website updates ready for deployment.

## Maintenance mode

The developer of this repo may also work with you to improve the repo itself. in those cases, you
can skip the above podcasting instructions and focus on helping him with writing clean and
maintainable software.
