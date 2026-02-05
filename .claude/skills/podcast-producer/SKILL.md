---
name: podcast-producer
description: |
    Orchestrates end-to-end podcast episode production for drug repurposing stories. Use this skill
    when the user requests creating a podcast episode for a specific drug-disease pair (e.g., "Create
    an episode for Aspirin and Cardiovascular Disease Prevention" or "Produce the Metformin PCOS
    episode"). Automatically runs the full production pipeline: archivist (research) → showrunner
    (structure) → podcast-writer (scripting) → editor (editorial pass) → speaker (audio generation) →
    git commit. Handles error recovery with TODO markers and partial work commits.
---

# Podcast Producer: End-to-End Episode Orchestration

## Overview

This skill orchestrates the complete production of a drug repurposing podcast episode through a
sequential 5-agent pipeline. Each agent builds on the previous agent's output, creating a fully
produced episode ready for publishing.

## Production Pipeline

The pipeline runs agents in this order:

1. **Archivist** - Research and compile background dossier
2. **Showrunner** - Create episode structure and show notes (chooses arc based on evidence)
3. **Podcast-writer** - Generate dual-host dialogue transcript (follows showrunner structure)
4. **Editor** - Final editorial pass for narrative coherence
5. **Speaker** - Generate audio from completed transcript

After completion, changes are automatically committed to git (but not pushed).

## Workflow

### Step 1: Parse User Request

Extract the drug name and disease from user request. Common phrasings:
- "Create an episode for [Drug] and [Disease]"
- "Produce the [Drug]-[Disease] episode"
- "Generate podcast for [Drug] treating [Disease]"
- "Make an episode about [Drug] for [Disease]"

Normalize to format: `pair-<drug>-<disease>` (lowercase, hyphens for spaces)

### Step 2: Verify Working Directory

Ensure the working directory structure exists:
```
stories/pair-<drug>-<disease>/
├── background/      (created by archivist)
├── shownotes/       (created by showrunner)
└── transcript/      (created by podcast-writer)
```

### Step 3: Run Production Pipeline

Execute agents sequentially using the Task tool. After each agent:
1. ✅ **Verify output** (check expected files exist)
2. ✅ **Auto-cleanup** (fix common naming/location mistakes)
3. ⚠️ **Retry once** if issues remain (with specific feedback)
4. ❌ **Fail** if still broken after retry

Execute agents in this order:

#### Agent 1: Archivist (Research)
```
Task tool parameters:
- subagent_type: "archivist"
- description: "Research background for [drug]-[disease]"
- prompt: "Research and compile a comprehensive, evidence-first background dossier for
           [Drug Name] repurposed for [Disease Name]. Use specialized sources first
           (PubMed, ClinicalTrials.gov, bioRxiv/medRxiv, patents, FDA/EMA docs), then
           general web search only to fill gaps. Generate detailed background files
           with citations covering context, origin, evidence of discovery/trigger,
           regulatory/adoption history, mechanism, and impact."
```

**Output**: `stories/pair-<drug>-<disease>/background/*.md` files

**Verification**: Check that at least 5 background files were created with substantial content

#### Agent 2: Showrunner (Structure)
```
Task tool parameters:
- subagent_type: "showrunner"
- description: "Create episode structure for [drug]-[disease]"
- prompt: "Using the background dossier at stories/pair-<drug>-<disease>/background/,
           choose the narrative structure that best fits the evidence, then create the episode
           structure with cold open, chapter outline, thematic playbook, and grading criteria.
           Output to stories/pair-<drug>-<disease>/shownotes/"
```

**Output**: `stories/pair-<drug>-<disease>/shownotes/*.md` files

**Verification**: Check that 00-episode-structure.md exists with narrative arc and timing

#### Agent 3: Podcast-writer (Scripting)
```
Task tool parameters:
- subagent_type: "podcast-writer"
- description: "Generate transcript for [drug]-[disease]"
- prompt: "Using the episode structure at stories/pair-<drug>-<disease>/shownotes/,
           generate full podcast transcript with dual-host dialogue (Marcus & Elena),
           following the showrunner's chosen structure. Ensure equal speaker distribution
           and varied emotional tags. Format for ElevenLabs podcast API. Output to
           stories/pair-<drug>-<disease>/transcript/"
```

**Output**: `stories/pair-<drug>-<disease>/transcript/*.md` files (one per chapter)

**Verification**: Check that multiple transcript sections exist with balanced speaker distribution

#### Agent 4: Editor (Editorial Pass)
```
Task tool parameters:
- subagent_type: "editor"
- description: "Editorial pass for [drug]-[disease]"
- prompt: "Perform comprehensive editorial pass on transcript at
           stories/pair-<drug>-<disease>/transcript/. Fix narrative flow, transitions,
           duplication, pacing issues. Update transcript files directly and create
           editorial summary."
```

**Output**: Updated transcript files + editorial notes

**Verification**: Check that editorial notes or summary file was created

#### Agent 5: Speaker (Audio Generation)
```
Task tool parameters:
- subagent_type: "speaker"
- description: "Generate audio for [drug]-[disease]"
- prompt: "Generate podcast audio from completed transcript at
           stories/pair-<drug>-<disease>/transcript/ using Google Gemini TTS API.
           Output MP3 file to stories/pair-<drug>-<disease>/transcript/"
```

**Output**: `stories/pair-<drug>-<disease>/transcript/*.mp3` file

**Verification**: Check that MP3 file exists and has non-zero size

### Step 4: Git Commit

After successful completion, commit all work:

```bash
git add stories/pair-<drug>-<disease>/
git commit -m "Complete episode production: <Drug> - <Disease>

- Research: Background dossier compiled by archivist
- Structure: Episode outline and show notes created
- Script: Dual-host transcript generated
- Editorial: Final narrative pass completed
- Audio: Full episode MP3 generated

Episode ready for review and publishing.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Important**: Do NOT push to remote. Only commit locally.

### Step 5: Report Completion

Provide summary to user:
- Episode location
- Files created
- Git commit hash
- Next steps (review audio, gather feedback, publish)

## Error Handling

If any agent fails during the pipeline:

### 1. Create Error File

Write detailed error report to:
```
stories/pair-<drug>-<disease>/PRODUCTION_ERROR.md
```

**Error file format:**
```markdown
# Production Error: [Drug] - [Disease]

**Date**: [ISO timestamp]
**Failed Agent**: [Agent name that failed]
**Pipeline Stage**: [Stage number and name]

## Error Description

[Detailed error message and stack trace if available]

## Work Completed

- [x] Archivist: Background dossier completed
- [x] Showrunner: Episode structure completed
- [ ] Podcast-writer: FAILED HERE
- [ ] Editor: Not started
- [ ] Speaker: Not started

## Files Created

[List of files successfully created before failure]

## Required Action

TODO: Human intervention required to resolve this error and continue production.

[Specific guidance on what needs to be fixed based on the error]

## Resuming Production

After fixing the error, resume from the failed agent:
[Command to resume, e.g., "Continue podcast production from podcast-writer step"]
```

### 2. Commit Partial Work

Even on failure, commit what was completed:

```bash
git add stories/pair-<drug>-<disease>/
git commit -m "PARTIAL: Episode production incomplete: <Drug> - <Disease>

Pipeline failed at [Agent Name] stage.
See PRODUCTION_ERROR.md for details.

Work completed:
- [List completed stages]

TODO: Human intervention required to resolve production error.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### 3. Report Failure to User

Clearly communicate:
- Which agent failed
- What was completed successfully
- Location of error file
- How to search for TODO markers: `grep -r "TODO" stories/pair-<drug>-<disease>/`

## User Control Options

### Stop at Specific Step

If user specifies stopping early:
- "Create episode for X and Y, but stop after showrunner"
- "Only run archivist for X and Y"
- "Generate up to transcript for X and Y"

Then run only the specified agents and stop. Still commit the partial work.

### Skip Completed Steps

If directory already has completed work:
- Check which agents have already produced output
- Ask user: "I see [X agent] already completed. Resume from [Y agent]?"
- Or if user is explicit: "Continue from editor step"

### Re-run Specific Agent

If user wants to re-run a single agent:
- "Re-run the podcast-writer for X and Y"
- "Regenerate audio for X and Y"

Then run only that agent, potentially overwriting previous output.

## Quality Checks & Cleanup

After each agent completes, perform verification and automatic cleanup:

### Verification Process

1. **Check expected files exist** (see checklists below)
2. **Check file content** (not empty, no error messages)
3. **Detect file structure violations** (wrong names, wrong locations)
4. **Automatically fix common mistakes** (rename, move files)
5. **Report what was cleaned up** to user

### Agent-Specific Checks & Cleanup

#### After Archivist

**Expected files (9 total):**
```bash
README.md
background/00-dossier-overview.md
background/01-context.md
background/02-origin.md
background/03-struggle.md
background/04-pivot-point.md
background/05-renaissance.md
background/06-mechanism.md
background/07-impact.md
```

**Common mistakes to auto-fix:**
- `background/00-summary.md` → rename to `00-dossier-overview.md`
- `background/01-context-era.md` → rename to `01-context.md`
- `background/02-origin-intended-use.md` → rename to `02-origin.md`
- `background/03-struggle-failure.md` → rename to `03-struggle.md`
- `background/dossier-overview.md` → rename to `00-dossier-overview.md`

**Verification:**
- All 9 files exist
- README.md is 400-600 words
- Background files cite sources

#### After Showrunner

**Expected files (5 total in shownotes/):**
```bash
shownotes/00-episode-structure.md
shownotes/01-cold-open.md
shownotes/02-narrative-arc.md
shownotes/03-playbook.md
shownotes/04-grading-criteria.md
```

**Common mistakes to auto-fix:**
- `episode-structure.md` at root → move to `shownotes/00-episode-structure.md`
- `shownotes/EPISODE_STRUCTURE.md` → rename to `00-episode-structure.md`
- `shownotes/02-chapter-outline.md` → rename to `02-narrative-arc.md`
- Duplicate files (e.g., both `EPISODE_STRUCTURE.md` and `01-episode-structure.md`) → keep numbered one, delete duplicate

**Verification:**
- All 5 files exist in shownotes/
- Episode structure has timing information
- Grading criteria has weighted rubrics

#### After Podcast-writer

**Expected files (9 total in transcript/):**
```bash
transcript/01-cold-open.md
transcript/02-context.md
transcript/03-origin.md
transcript/04-struggle.md
transcript/05-pivot-point.md
transcript/06-renaissance.md
transcript/07-impact.md
transcript/08-playbook.md
transcript/09-grading.md
```

**Common mistakes to auto-fix:**
- `transcript/02-chapter1-wrong-target.md` → rename to `02-context.md`
- `transcript/easter-island.md` → rename based on position to appropriate chapter
- Story-specific names → standardize to chapter names
- Missing files → flag as error (can't auto-fix dialogue content)

**Verification:**
- All 9 files exist in transcript/
- Each file has MARCUS: and ELENA: speakers
- Speaker distribution roughly balanced (45-55%)

#### After Editor

**Expected files (1 new file):**
```bash
EDITORIAL_NOTES.md
```

**Common mistakes to auto-fix:**
- `00-EDITORIAL-NOTES.md` → rename to `EDITORIAL_NOTES.md`
- `EDITORIAL_SUMMARY.md` → rename to `EDITORIAL_NOTES.md`
- `editorial-notes.md` → rename to `EDITORIAL_NOTES.md` (uppercase)

**Verification:**
- EDITORIAL_NOTES.md exists at root
- Contains summary of changes made

#### After Speaker

**Expected files (1 audio file):**
```bash
transcript/<drug>-full-episode.mp3
```

**Common mistakes to auto-fix:**
- `transcript/full-episode.mp3` → rename to `<drug>-full-episode.mp3`
- `transcript/episode.mp3` → rename to `<drug>-full-episode.mp3`
- `transcript/<drug>-<disease>-full-episode.mp3` → rename to `<drug>-full-episode.mp3`

**Verification:**
- MP3 file exists
- File size > 1MB (has actual content)

### Cleanup Actions

When issues are detected, automatically:

1. **Rename files** with wrong names:
   ```bash
   mv "old-name.md" "correct-name.md"
   ```

2. **Move files** to correct locations:
   ```bash
   mv "episode-structure.md" "shownotes/00-episode-structure.md"
   ```

3. **Delete duplicate files**:
   ```bash
   rm "EPISODE_STRUCTURE.md"  # Keep the numbered version
   ```

4. **Report cleanup** to user:
   ```
   ✓ Cleaned up file structure after [Agent] completed:
     - Renamed: background/00-summary.md → 00-dossier-overview.md
     - Moved: episode-structure.md → shownotes/00-episode-structure.md
     - Deleted duplicate: EPISODE_STRUCTURE.md
   ```

### When Cleanup Cannot Fix

If issues cannot be auto-fixed, use **retry-with-feedback mechanism**:

#### Step 1: Identify Issues

Detect problems that require agent re-work:
- Missing required files
- Empty or corrupted files
- Files with error messages instead of content
- Wrong file structure that can't be auto-renamed
- Content quality issues (no citations, missing timings, etc.)

#### Step 2: Re-invoke Agent Once with Feedback

Give the agent ONE chance to fix issues by re-invoking with specific feedback:

```
Task tool parameters:
- subagent_type: "[agent-name]"
- description: "Fix issues in [agent] output"
- prompt: "You previously generated output for [drug]-[disease] but there were issues.

           Problems found:
           - [Specific issue 1]
           - [Specific issue 2]
           - [Specific issue 3]

           Please fix these issues. Your output should include:
           - [Expected file 1]
           - [Expected file 2]
           - [Expected file 3]

           Do NOT repeat the mistakes. Follow the file structure exactly as specified
           in your instructions."
```

**Feedback should be specific:**
- ✅ "Missing required file: background/04-pivot-point.md"
- ✅ "File background/02-origin.md is empty (0 bytes)"
- ✅ "README.md is only 150 words, needs 400-600 words"
- ✅ "No sources cited in any background files"
- ❌ "Files are wrong" (too vague)

#### Step 3: Verify Again After Retry

After agent re-runs:
1. Check if issues are fixed
2. Run cleanup again (in case of new mistakes)
3. If STILL broken → treat as failure

#### Step 4: Fail After One Retry

If agent fails twice (original + one retry), give up and follow error handling:
- Create PRODUCTION_ERROR.md with specific details
- Note that agent was given feedback and failed to fix
- Commit partial work
- Report failure to user

**Example error report:**
```markdown
## Error Description

Archivist agent failed to create required files after two attempts.

First attempt issues:
- Missing file: background/04-pivot-point.md
- File background/02-origin.md was empty

Agent was re-invoked with specific feedback.

Second attempt issues:
- Still missing file: background/04-pivot-point.md
- File now has content but no citations

After two attempts, agent could not produce correct output.

## Required Action

TODO: Human needs to manually create background/04-pivot-point.md
```

### Retry vs. Auto-Fix Decision

**Auto-fix (no retry needed):**
- Wrong filename (can rename)
- Wrong location (can move)
- Duplicate files (can delete)
- Incorrect casing (can rename)

**Retry with feedback:**
- Missing files (agent needs to create content)
- Empty files (agent needs to write content)
- Missing critical elements (citations, timings, etc.)
- Quality issues (too short, wrong format, etc.)

**Fail immediately (no retry):**
- Agent crashes or returns error
- Agent refuses to run
- Downstream dependency failures (e.g., showrunner can't run if archivist failed)

## Agent Configuration

All agents are defined in `.claude/agents/` directory:
- `archivist.md`
- `showrunner.md`
- `podcast-writer.md`
- `editor.md`
- `speaker.md`
- `feedback.md` (used separately after episode completion)

These files contain detailed instructions for each agent's specific responsibilities.

## Integration with Feedback Loop

After episode completion and user review:
1. User collects listener feedback in `stories/pair-<drug>-<disease>/feedback.md`
2. After 2-3 episodes, user runs feedback agent separately
3. Feedback agent updates agent instructions in `.claude/agents/`
4. Future episodes benefit from improved instructions

The podcast-producer skill does NOT automatically run the feedback agent. Feedback is a separate,
periodic process run across multiple episodes.

## Example Usage

**User**: "Create an episode for Aspirin and Cardiovascular Disease Prevention"

**Skill Actions**:
1. Parse: drug="aspirin", disease="cardiovascular-disease-prevention"
2. Create: `stories/pair-aspirin-cardiovascular-disease-prevention/`
3. Run archivist agent → research background
4. Run showrunner agent → create structure
5. Run podcast-writer agent → generate transcript
6. Run editor agent → editorial pass
7. Run speaker agent → generate audio
8. Commit all files to git (no push)
9. Report: "Episode complete! Audio at stories/pair-aspirin-cardiovascular-disease-prevention/transcript/aspirin-full-episode.mp3"

## Success Criteria

Episode production succeeds when:
- All 5 agents complete without errors
- All expected output files exist with substantial content
- Git commit created with complete work
- User receives clear completion summary
- Episode is ready for review and publishing

## Common Issues

### Agent Timeout
If an agent runs too long, it may timeout. Consider:
- Running agents with longer timeout if available
- Breaking into smaller manual steps for complex episodes
- Checking if API rate limits are being hit (Gemini TTS, web search)

### Missing Dependencies
If agents fail due to missing tools:
- Archivist needs: web search, academic databases
- Speaker needs: Google Gemini API key, audio processing tools
- All agents need: file system access, proper directory permissions

### Git Conflicts
If git commit fails due to conflicts:
- Check if files are being modified elsewhere
- Ensure working directory is clean before starting
- Manually resolve conflicts and re-commit
