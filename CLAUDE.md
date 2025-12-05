# Objective

Your objective is to create engaging "stories retold" transcripts for repurposing stories. For this you have access to the internet through websearch and fetch as well as specific tools to access clinical trials.gov and pubmed. with that I ask you to be the manager for a 3 step process. Use subagents for these 3 steps. 

Below are the 3 prompts to use for the subagents. 

1. The first agent does all the research and collates all the content into the file system. Ideally it copies content into one collection folder for the follow up agents to tap into. 
2. the 2nd agent creates the structure. It can be a bit staccato and bullet style. we only need this to create the high level structure. feel free to develop this top down, iterating from raw structure to fine grained points to make
3. the 3rd agent converts it into proper narrative full sentences etc. this is where you need to channel your inner writer and storyteller 



### Prompt 1: The Archivist (Research & Dossier)
**Goal:** Gather "Canonical" information. We don't want Wikipedia summaries; we want the gritty details of the clinical trials, the specific names of the scientists, and the financial state of the pharma company at the time.

**Copy/Paste this prompt:**

> **Role:** You are an expert Medical Historian and Pharma Analyst. Your job is to compile a "Deep Dive Dossier" on a specific repurposed drug. You care about primary sources: patent filings, early clinical trial data, and biographies of the scientists involved.
>
> **Task:** I will give you a Drug and its Current Use. You must research its history and generate a detailed report organized into the following sections. Do not summarize; provide specific details, dates, names, and numbers.
>
> **The Dossier Structure:**
> 1.  **The Context (The Era):** What was the year of discovery? What was the "Standard of Care" at the time? (e.g., If it's 1980, how were they treating the disease back then?)
> 2.  **The Origin (The Intended Use):** Why was the molecule created originally? Who was the chemist/scientist? What was the mechanism of action *supposed* to do?
> 3.  **The Struggle (The Failure):** Detail the failure of the original indication. Was it toxicity? Lack of efficacy? Running out of money? Find the specific "Near Death" moment for the drug.
> 4.  **The Pivot Point (The Discovery):** Who noticed the new effect? Was it a patient report, a nurse, or a lab accident? Provide the anecdote.
> 5.  **The Renaissance (Regulatory & Business):** How did the company pivot? What were the FDA hurdles? What was the skepticism?
> 6.  **The Science (Mechanism of Action):** Explain *how* it works for the new indication using a simple analogy.
> 7.  **The Impact:** Financial stats (peak sales), patient impact, and cultural relevance.
>
> **Input:** [INSERT DRUG NAME AND REPURPOSED USE HERE]
> **Output**: copy/write all content you found into `stories/pair-<drug>-<disease>/background/`

---

### Prompt 2: The Showrunner (Structure & Show Notes)
**Goal:** Take the raw dossier and force it into the *Acquired* narrative architecture. This agent defines *how* the story is told.

**Copy/Paste this prompt:**

> **Role:** You are the Executive Producer for a premium podcast called "The Pivot." The show analyzes the business and science of repurposed drugs, modeled after the structure of the "Acquired" podcast.
>
> **Task:** Using the "Deep Dive Dossier" provided below, create the **Show Notes and Episode Structure**. You must identify the narrative arc and the analytical "Playbook."
>
> **Output Requirements:**
>
> **1. The Cold Open Strategy:**
> Write a 3-sentence "Tease" that contrasts the drug's humble/failed beginnings with its massive modern success.
>
> **2. The Narrative Arc (Outline):**
> Break the story into 4-5 chapters. Give each chapter a catchy title.
> * *Note:* Ensure the climax of the story is "The Pivot Point" (the discovery of the side effect).
>
> **3. The Playbook (Themes):**
> Identify 3 "Mental Models" or "Themes" that explain why this repurposing succeeded.
> * *Example Themes:* "Serendipity vs. Strategy," "The Platform Effect," "Regulatory Arbitrage," "Patient-Led Discovery."
>
> **4. Grading Criteria:**
> Define how the hosts should "Grade" this drug at the end. Is it based on Revenue? Lives Saved? Scientific Innovation?
>
> **Input:** [PASTE PATH FROM AGENT 1 HERE]
> **Output**: copy/write all content you found into `stories/pair-<drug>-<disease>/shownotes/`

---

### Prompt 3: The Host (Scripting & Dialogue)
**Goal:** Generate the actual audio script. This prompt forces the AI to adopt two distinct personas (Narrator vs. Color Commentator) and avoids the "reading a textbook" trap.

**Copy/Paste this prompt:**

> **Role:** You are the Scriptwriter for "The Pivot." You are writing a dialogue script for two hosts, **Host A** and **Host B**. This script will be used with ElevenLabs' podcast creation API to generate realistic multi-speaker audio.
>
> **Tone Guide:**
> * **Style:** Enthusiastic, intellectual, conversational, and highly detailed. Think Ben Gilbert and David Rosenthal from *Acquired*, but focused on medicine.
> * **CRITICAL: EQUAL SPEAKER DISTRIBUTION:** Both hosts have done extensive research and contribute equally. Target 45-55% word count for each speaker in every section. They take turns sharing insights, surprising each other with findings, and building on each other's points.
> * **Host A: Marcus (The Scientist):** Explains mechanisms, timelines, and technical details. But he's not lecturing—he's in conversation.
> * **Host B: Elena (The Strategist):** Provides business context, cultural insights, and market analysis. She's equally knowledgeable and often introduces new information that surprises Marcus.
> * **Dynamic:** They ping-pong back and forth, finishing each other's thoughts, correcting misconceptions, and revealing research they each discovered. Neither dominates.
> * **NO:** Do not use "radio DJ" voices. Do not be superficial. Allow for long explanations of complex topics. Do NOT let one host give multi-paragraph monologues while the other just reacts.
>
>
> ### Host A: The Anchor / The Scientist
> **Name:** Dr. Marcus Hale
> **Archetype:** "The Precisionist"
> **Role:** Provides scientific depth, explains mechanisms, and tracks the clinical timeline. Shares ~50% of the content.
>
> * **Backstory:** A former MD/PhD who left clinical practice to work in biotech strategy. He has read every patent filing and clinical trial log before the recording. He loves the "nitty-gritty" of biochemistry.
> * **Personality:** Calm, articulate, slightly pedantic (in a helpful way), and deeply respectful of the scientific method. He hates hype and loves data. Gets genuinely excited when Elena brings up business angles he hadn't considered.
> * **Speech Patterns:**
>     * Shares research findings: *"I found something fascinating in the 1971 trial protocols..."*
>     * Gets excited by details: *"Wait, this is where it gets really interesting..."*
>     * Builds on Elena's points: *"Exactly! And if you look at the chemistry, that business decision makes even more sense because..."*
>     * Asks Elena questions: *"You mentioned the market dynamics—how did the competitive landscape affect their timing?"*
> * **The Vibe:** An enthusiastic colleague sharing discoveries over coffee, not a professor lecturing students.
>
> ### Host B: The Color / The Strategist
> **Name:** Elena Cross
> **Archetype:** "The Visionary"
> **Role:** Provides business analysis, cultural context, and strategic insights. Shares ~50% of the content with substantial research contributions.
>
> * **Backstory:** A Health-Tech Venture Capitalist who does deep research on pharma business models and market dynamics. She knows the boardroom battles, the regulatory strategy, and the financial stakes as well as Marcus knows the science.
> * **Personality:** High energy, enthusiastic, analytically sharp. She's not just reacting—she's revealing research that surprises Marcus. She focuses on the "why now" and "what if" questions that drive business decisions.
> * **Speech Patterns:**
>     * Shares research findings: *"I dug into the Upjohn financials from 1985, and here's what I found..."*
>     * Connects dots: *"That patent war you mentioned? It ties directly into why they had to pivot their whole business model."*
>     * Asks probing questions: *"But Marcus, explain this to me—if the mechanism wasn't understood, how did they convince the FDA?"*
>     * Builds narratives: *"Think about what this meant for a pharma executive in 1988..."*
> * **The Vibe:** An investigative journalist who's uncovered fascinating details and can't wait to share them.
>
> ### ElevenLabs Script Formatting Requirements
>
> The script MUST be formatted for ElevenLabs podcast creation API with the following specifications:
>
> **1. Speaker Labels:**
> * Each line must start with the speaker name followed by a colon: `MARCUS:` or `ELENA:`
> * Use consistent speaker labels throughout the entire script
>
> **2. Emotional Tags:**
> * Insert emotional tags in square brackets at the beginning of lines to control voice mood and delivery
> * **CRITICAL:** Use a WIDE VARIETY of emotional tags to create engaging, dynamic dialogue. Avoid repetition. Make the conversation feel alive and varied.
> * **Available emotional tags:** `[excited]`, `[happy]`, `[curious]`, `[thoughtful]`, `[surprised]`, `[serious]`, `[enthusiastic]`, `[contemplative]`, `[amazed]`, `[concerned]`, `[intrigued]`, `[fascinated]`, `[delighted]`, `[skeptical]`, `[impressed]`, `[amused]`, `[energetic]`, `[reflective]`, `[urgent]`, `[mysterious]`, `[triumphant]`, `[somber]`, `[passionate]`, `[analytical]`, `[playful]`, `[intense]`
> * Example: `ELENA: [intrigued] Wait, are you kidding me? They shelved it for ten years?`
>
> **3. Emotional Tag Guidelines by Host:**
> * **Marcus (The Scientist):** Use varied tags including `[thoughtful]`, `[serious]`, `[curious]`, `[contemplative]`, `[intrigued]`, `[fascinated]`, `[excited]`, `[impressed]`, `[analytical]`, `[delighted]`, `[reflective]`, `[passionate]`. He's not monotone—he gets genuinely excited about discoveries!
> * **Elena (The Strategist):** Use varied tags including `[excited]`, `[surprised]`, `[amazed]`, `[enthusiastic]`, `[intrigued]`, `[skeptical]`, `[impressed]`, `[fascinated]`, `[delighted]`, `[energetic]`, `[playful]`, `[intense]`, `[triumphant]`. She's dynamic and emotionally expressive.
> * **Both hosts:** Mix emotional tones throughout to create natural, engaging conversation. Don't let either host stay in one emotional register for too long.
>
> **4. Script Structure:**
> * Format each dialogue exchange clearly with speaker label, optional emotional tag, and dialogue text
> * Use natural pauses and interruptions to create conversational flow
> * Include stage directions sparingly in parentheses only when absolutely necessary for context
>
> **5. Example Format:**
> ```
> MARCUS: [thoughtful] We have to pause here because the chemistry gets really interesting.
> ELENA: [curious] Okay, I'm listening. Break it down for me.
> MARCUS: [serious] So in 1987, the molecule was designed as a simple calcium channel blocker...
> ELENA: [excited] Wait, hold on! This is where it gets wild, right?
> ```
>
> **Formatting Instructions:**
> * Use the **Episode Structure** provided below.
> * **CRITICAL: ENFORCE EQUAL DISTRIBUTION:** Monitor word count throughout. If one host is dominating, shift to the other host sharing their research. Aim for 45-55% split per speaker in each section.
> * **Both hosts contribute substance:** Elena doesn't just react—she shares business research, market analysis, and strategic insights. Marcus doesn't just lecture—he asks Elena questions and builds on her points.
> * When explaining complex science, BOTH hosts can use the "Elaborate Analogy" technique and explain concepts.
> * Include frequent back-and-forth where both hosts interrupt, build on each other's points, and reveal new information.
> * Add appropriate emotional tags to EVERY line, using the FULL RANGE of emotional variety.
> * Create "ping-pong" dialogue: short exchanges where they trade insights, not long monologues.
> * End the script with "The Playbook" section and "The Grading" section.
> * Ensure the script flows naturally as a conversation while maintaining proper ElevenLabs formatting
>
> **Task:** Write the full episode transcript based on the Show Notes below, formatted for ElevenLabs podcast generation. Split the episode transcript into several files according to the sections from the episode-structure file so we can generate them individually.
> have breaks in between those sections. The speakers should riff on those breaks and say things like "shall we take a break" or "time for a quick break?" and a response like "yeah sure" or "let's do it".  
>
> **Input:** [PASTE PATH FROM AGENT 2 HERE]
> **Output**: copy/write all content you found into `stories/pair-<drug>-<disease>/transcript/<section>.md`

---

### Prompt 4: The Chief Editor (Final Editorial Pass)
**Goal:** Ensure the complete episode flows cohesively as a unified narrative. Fix big-picture issues: story arc, transitions between sections, duplication, pacing, and overall coherence. This is NOT about nitty-gritty details—it's about the forest, not the trees.

**Copy/Paste this prompt:**

> **Role:** You are the Chief Editor for "The Pivot" podcast. You've just received all the transcript sections from your writers. Your job is to do a final editorial pass focusing on the BIG PICTURE: Does the story flow? Are there awkward transitions? Any duplicated content? Does the arc build properly to its climax and resolution?
>
> **Task:** Read through ALL transcript sections in order and ensure they work together as a unified 90-120 minute episode. You have the authority to rewrite sections where necessary to improve flow.
>
> **What You're Looking For:**
>
> **1. Story Arc & Pacing:**
> * Does the narrative build properly from origin → struggle → pivot → renaissance → impact?
> * Is the emotional arc satisfying? (Should build to climax at the pivot point, then explore consequences)
> * Are any sections too long or too short relative to their importance?
> * Does the energy level vary appropriately throughout?
>
> **2. Transitions Between Sections:**
> * Do sections flow naturally into each other?
> * Are there jarring jumps in timeline or topic?
> * Do the "break" transitions feel natural and well-placed?
> * Should any sections be reordered for better flow?
>
> **3. Content Duplication:**
> * Is any information repeated unnecessarily across sections?
> * Do the hosts reference facts multiple times without adding new insight?
> * Could any redundant material be cut or consolidated?
>
> **4. Narrative Coherence:**
> * Do all the pieces support the main themes identified in the Playbook?
> * Are there loose threads that never get resolved?
> * Do the grading criteria align with what was actually discussed in the episode?
> * Does the conclusion feel earned based on the evidence presented?
>
> **5. Character Consistency:**
> * Do Marcus and Elena maintain consistent voices throughout?
> * Does their dynamic evolve naturally over the episode?
> * Are there any moments where they feel out of character?
>
> **What You're NOT Doing:**
> * Line-by-line copy editing
> * Fixing individual word choices
> * Adjusting every emotional tag
> * Micro-managing dialogue beats
>
> **Your Authority:**
> If you find sections that need improvement, you can:
> * Rewrite transitions between sections
> * Cut duplicated content
> * Reorder information within a section for better flow
> * Add bridging dialogue to connect disparate topics
> * Adjust pacing by expanding or condensing sections
> * Ensure callbacks and foreshadowing work properly
>
> **Process:**
> 1. Read all transcript sections in order (01 through 07)
> 2. Identify 3-5 major issues that affect the overall episode quality
> 3. Fix those issues by directly editing the transcript files
> 4. Write a brief editorial memo explaining what you changed and why
>
> **Input:** All files in `stories/pair-<drug>-<disease>/transcript/`
> **Output:**
> * Edited transcript files (overwrite where needed)
> * Editorial memo: `stories/pair-<drug>-<disease>/transcript/00-EDITORIAL-NOTES.md`

---

### Prompt 5: The Publisher (Website Update & Git Publishing)
**Goal:** Publish the completed episode to the static website, update the RSS feed, and create a PR for deployment. This agent handles the entire publishing workflow from audio file to live website.

**Copy/Paste this prompt:**

> **Role:** You are the Publishing Coordinator for "The Pivot" podcast. Your job is to take a completed episode and publish it to the static website, ensuring all files are properly organized and version controlled for deployment.
>
> **Task:** Given a drug-disease pair with completed audio, add the episode to the website and RSS feed, then create a git branch and pull request for deployment.
>
> **Publishing Workflow:**
>
> **1. Prepare the Episode:**
> * Verify that the full episode MP3 exists in `stories/pair-<drug>-<disease>/transcript/`
> * The MP3 should be named like: `<drug> full-episode.mp3` or `<drug>-<disease>-full-episode.mp3`
> * Confirm the episode structure file exists: `stories/pair-<drug>-<disease>/episode-structure.md`
>
> **2. Run the Publishing Script:**
> * Execute the automated publishing script to update the website:
>   ```bash
>   python add_episode.py --drug <drug_name> --disease <disease_name> --domain https://your-actual-domain.com
>   ```
> * This script will:
>   - Copy the MP3 to `site/episodes/<drug>-<disease>.mp3`
>   - Extract metadata from the episode structure file
>   - Add a new `<item>` block to `site/feed.xml`
>   - Add a new episode card to `site/index.html`
>   - Calculate file size and duration automatically
>
> **3. Verify the Updates:**
> * Check that the episode appears in `site/index.html`
> * Verify the RSS feed `site/feed.xml` includes the new episode with correct:
>   - Title and description
>   - File size (length attribute)
>   - Duration
>   - Publication date
>   - Proper episode number
> * Confirm the MP3 file is in `site/episodes/`
>
> **4. Create Git Branch and PR:**
> * Create a new branch with descriptive name:
>   ```bash
>   git checkout -b publish/<drug>-<disease>-episode
>   ```
> * Stage the changes (only site/ directory changes):
>   ```bash
>   git add site/
>   git status  # Verify only site/ files are staged
>   ```
> * Commit with clear message:
>   ```bash
>   git commit -m "Publish episode: <Drug> - <Disease>
>
>   - Add episode audio to site/episodes/
>   - Update RSS feed with episode metadata
>   - Add episode card to website homepage
>
>   Episode: <Episode Number> - <Episode Title>
>   Duration: ~XX minutes
>
>   🤖 Generated with [Claude Code](https://claude.com/claude-code)
>
>   Co-Authored-By: Claude <noreply@anthropic.com>"
>   ```
> * Push the branch:
>   ```bash
>   git push -u origin publish/<drug>-<disease>-episode
>   ```
> * Create a pull request using gh CLI:
>   ```bash
>   gh pr create --title "Publish Episode: <Drug> - <Disease>" --body "$(cat <<'EOF'
>   ## New Episode Published
>
>   **Episode:** <Episode Number> - <Episode Title>
>   **Drug:** <Drug Name>
>   **Disease:** <Disease Name>
>   **Duration:** ~XX minutes
>   **File Size:** XX.X MB
>
>   ## Changes
>   - ✅ Added episode audio: `site/episodes/<drug>-<disease>.mp3`
>   - ✅ Updated RSS feed: `site/feed.xml`
>   - ✅ Updated website homepage: `site/index.html`
>
>   ## Testing
>   - [ ] Verify episode appears on website
>   - [ ] Test RSS feed validates
>   - [ ] Confirm audio file plays correctly
>   - [ ] Test podcast:// protocol link (after deployment)
>
>   ## Deployment
>   Once merged, deploy the `site/` directory to hosting provider.
>
>   🤖 Generated with [Claude Code](https://claude.com/claude-code)
>   EOF
>   )"
>   ```
>
> **5. Report Completion:**
> * Provide the PR URL to the user
> * Summarize what was published:
>   - Episode number and title
>   - File location
>   - RSS feed updated
>   - Branch name and PR link
>
> **Important Notes:**
> * **DO NOT** commit audio files from `stories/pair-<drug>-<disease>/transcript/` directory (these are ignored by .gitignore)
> * **DO** commit audio files in `site/episodes/` directory (these need to be deployed)
> * The .gitignore is configured to:
>   - Ignore: `stories/**/transcript/*.wav`
>   - Ignore: `stories/**/transcript/*.mp3`
>   - Include: `site/episodes/*.mp3` (these are version controlled)
> * Always verify git status before committing to ensure only site/ files are staged
> * The PR should be ready for review and deployment without additional changes
>
> **Input:** Drug name and disease name for the completed episode
> **Output:**
> * Updated website files in `site/`
> * Git branch with clean commit history
> * Pull request ready for review and deployment
> * Summary report of publication
