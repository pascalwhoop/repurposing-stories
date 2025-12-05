#!/usr/bin/env python3
"""
CLI tool to convert transcript markdown files to audio using Google Gemini TTS.
"""

import sys
import re
import time
import json
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import typer
from google import genai
from google.genai import types
import wave
from pydub import AudioSegment
from pydantic_settings import BaseSettings, SettingsConfigDict
from tenacity import retry, stop_after_delay, wait_fixed, retry_if_exception_type

app = typer.Typer()


# Pricing per 1 million tokens (in USD)
PRICING = {
    "gemini-2.5-pro-preview-tts": {
        "input": 1.00,
        "output": 20.00,
    },
    "gemini-2.5-flash-preview-tts": {
        "input": 0.30,
        "output": 2.50,
    },
}

# Output audio tokens are fixed at 25 tokens per second
OUTPUT_TOKENS_PER_SECOND = 25


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    gemini_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def get_model_name(model: str) -> str:
    """Map model shorthand to full model name."""
    if model == "pro":
        return "gemini-2.5-pro-preview-tts"
    elif model == "flash":
        return "gemini-2.5-flash-preview-tts"
    else:
        typer.echo(f"Error: Unknown model '{model}'. Use 'pro' or 'flash'.", err=True)
        sys.exit(1)


def sanitize_transcript(content: str) -> str:
    """
    Filter transcript content to only include dialogue lines.

    Removes markdown headers, separators, and other metadata.
    Only keeps lines matching the pattern: SPEAKER: [optional_tone] dialogue
    """
    lines = content.split('\n')
    dialogue_lines = []

    for line in lines:
        # Strip whitespace
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip markdown headers (lines starting with #)
        if stripped.startswith('#'):
            continue

        # Skip horizontal rules (---)
        if stripped.startswith('---'):
            continue

        # Check if line matches speaker pattern: WORD: (content)
        # Speaker names are typically all caps (MARCUS, ELENA)
        if ':' in stripped:
            speaker_part = stripped.split(':', 1)[0]
            # Check if speaker part looks like a speaker name (uppercase, no spaces)
            if speaker_part.isupper() and ' ' not in speaker_part:
                dialogue_lines.append(stripped)

    return '\n'.join(dialogue_lines)


def analyze_speaker_distribution(content: str) -> dict:
    """
    Analyze word count distribution by speaker.

    Returns dict with speaker names as keys and word counts as values.
    """
    sanitized = sanitize_transcript(content)
    speaker_words = {}

    for line in sanitized.split('\n'):
        if ':' not in line:
            continue

        speaker, dialogue = line.split(':', 1)
        speaker = speaker.strip()

        # Remove tone tags like [excited], [thoughtful], etc.
        dialogue = re.sub(r'\[.*?\]', '', dialogue)

        # Count words
        word_count = len(dialogue.split())

        speaker_words[speaker] = speaker_words.get(speaker, 0) + word_count

    return speaker_words


def estimate_audio_duration(text: str) -> float:
    """
    Estimate audio duration in seconds based on text length.

    Uses average speaking rate of 150 words per minute (2.5 words/second).
    """
    word_count = len(text.split())
    words_per_second = 2.5
    return word_count / words_per_second


def calculate_cost(input_tokens: int, audio_duration_seconds: float, model_name: str) -> dict:
    """
    Calculate estimated cost for TTS generation.

    Args:
        input_tokens: Number of input tokens
        audio_duration_seconds: Duration of generated audio in seconds
        model_name: Full model name (e.g., 'gemini-2.5-pro-preview-tts')

    Returns:
        Dictionary with cost breakdown
    """
    pricing = PRICING.get(model_name)
    if not pricing:
        return {
            "error": f"Unknown model: {model_name}",
            "input_cost": 0,
            "output_cost": 0,
            "total_cost": 0,
        }

    # Calculate output tokens based on audio duration
    output_tokens = int(audio_duration_seconds * OUTPUT_TOKENS_PER_SECOND)

    # Calculate costs (pricing is per 1M tokens)
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "audio_duration_seconds": audio_duration_seconds,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def parse_retry_delay(error_str: str) -> int:
    """
    Parse retryDelay from Gemini API error response.

    Returns delay in seconds, or 30 as default.
    """
    try:
        # Try to parse the error as JSON
        if 'retryDelay' in error_str:
            # Extract the retryDelay value (e.g., "26s" or "26.662656266s")
            import re
            match = re.search(r"'retryDelay': '([\d.]+)s'", error_str)
            if match:
                return int(float(match.group(1))) + 1  # Add 1 second buffer
    except Exception:
        pass
    return 30  # Default to 30 seconds


def generate_audio_with_retry(
    sanitized_content: str,
    output_path: Path,
    model_name: str,
    client: genai.Client,
    filename: str = "file",
    semaphore: threading.Semaphore = None,
):
    """
    Generate audio with automatic retry on rate limits.

    Respects API's retryDelay and retries up to 10 minutes total.
    Uses semaphore to limit concurrent API calls.
    """
    max_wait_time = 600  # 10 minutes
    start_time = time.time()
    attempt = 0

    while True:
        attempt += 1
        elapsed = time.time() - start_time

        if elapsed > max_wait_time:
            raise Exception(f"Timeout: Exceeded 10 minute retry limit")

        try:
            # Acquire semaphore before making API call
            if semaphore:
                semaphore.acquire()

            try:
                return generate_audio(sanitized_content, output_path, model_name, client)
            finally:
                # Always release semaphore
                if semaphore:
                    semaphore.release()

        except Exception as e:
            error_str = str(e)

            # Check if it's a rate limit error (429)
            if "429" in error_str and "RESOURCE_EXHAUSTED" in error_str:
                retry_delay = parse_retry_delay(error_str)
                remaining_time = max_wait_time - elapsed

                if retry_delay > remaining_time:
                    raise Exception(f"Rate limit delay ({retry_delay}s) exceeds remaining retry time")

                typer.echo(f"   ⏳ Rate limit hit for {filename}. Waiting {retry_delay}s (attempt {attempt})...")
                time.sleep(retry_delay)
                typer.echo(f"   🔄 Retrying {filename}...")
                continue
            else:
                # Not a rate limit error, re-raise
                raise


def generate_audio(
    sanitized_content: str,
    output_path: Path,
    model_name: str,
    client: genai.Client,
):
    """Generate audio from sanitized transcript content using Gemini TTS API."""

    prompt = f"TTS the following conversation between Marcus and Elena:\n{sanitized_content}"

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker="MARCUS",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Charon",
                                )
                            ),
                        ),
                        types.SpeakerVoiceConfig(
                            speaker="ELENA",
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name="Autonoe",
                                )
                            ),
                        ),
                    ]
                )
            ),
        ),
    )

    data = response.candidates[0].content.parts[0].inline_data.data
    wave_file(str(output_path), data)


def merge_wav_files(input_folder: Path, output_path: Path):
    """Merge all WAV files in a folder into a single MP3 file."""

    # Get all WAV files
    wav_files = sorted(input_folder.glob("*.wav"))

    if not wav_files:
        typer.echo(f"Error: No .wav files found in {input_folder}", err=True)
        sys.exit(1)

    typer.echo(f"Found {len(wav_files)} WAV file(s) to merge:")
    for wav_file in wav_files:
        typer.echo(f"  - {wav_file.name}")

    typer.echo(f"\n🔗 Merging audio files...")

    # Load and merge all WAV files
    try:
        combined = AudioSegment.empty()

        for wav_file in wav_files:
            typer.echo(f"   Adding {wav_file.name}...")
            audio = AudioSegment.from_wav(str(wav_file))
            combined += audio

        # Export to MP3 with good quality
        typer.echo(f"\n💾 Exporting to MP3: {output_path}")
        combined.export(
            str(output_path),
            format="mp3",
            bitrate="128k",
            parameters=["-q:a", "2"]  # VBR quality 2 (high quality)
        )

        # Calculate duration
        duration_seconds = len(combined) / 1000
        duration_minutes = duration_seconds / 60

        typer.echo(f"✅ Merged {len(wav_files)} files into {output_path.name}")
        typer.echo(f"📊 Total duration: {duration_minutes:.2f} minutes ({duration_seconds:.1f} seconds)")

    except Exception as e:
        typer.echo(f"Error merging audio files: {e}", err=True)
        sys.exit(1)


def process_files(files: list[Path], process_fn, parallel: bool = False, max_workers: int = 3):
    """
    Generic file processor supporting both sequential and parallel execution.

    Args:
        files: List of files to process
        process_fn: Function to call for each file (must return dict with 'status' key)
        parallel: Whether to process in parallel
        max_workers: Max parallel workers (only used if parallel=True)

    Returns:
        List of result dictionaries from process_fn
    """
    results = []

    if parallel:
        typer.echo(f"Starting parallel processing with {max_workers} workers...\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks and track them
            future_to_file = {executor.submit(process_fn, f): f for f in files}
            total = len(future_to_file)
            completed = 0

            # Process results as they complete
            for future in as_completed(future_to_file):
                completed += 1
                file_path = future_to_file[future]

                try:
                    result = future.result()
                    results.append(result)

                    # Show progress
                    status_icon = {
                        "success": "✅",
                        "skipped": "⏭️",
                        "error": "❌"
                    }.get(result.get("status"), "❓")

                    typer.echo(f"[{completed}/{total}] {status_icon} {file_path.name}")

                except Exception as e:
                    # Handle exceptions that weren't caught in the worker
                    typer.echo(f"[{completed}/{total}] ❌ {file_path.name}: Unexpected error: {e}", err=True)
                    results.append({
                        "status": "error",
                        "file": file_path.name,
                        "error": str(e)
                    })
    else:
        for f in files:
            results.append(process_fn(f))

    return results


def process_single_file_for_generation(
    md_file: Path,
    model_name: str,
    client: genai.Client,
    overwrite: bool,
    limit: int = None,
    semaphore: threading.Semaphore = None,
) -> dict:
    """Process a single file for audio generation."""
    wav_file = md_file.with_suffix(".wav")

    # Check if we should skip
    if not overwrite and wav_file.exists():
        return {"status": "skipped", "file": md_file.name}

    # Read and prepare content
    try:
        content = md_file.read_text(encoding="utf-8")
        if limit:
            content = content[:limit]
            truncated = len(md_file.read_text(encoding="utf-8")) > limit
        else:
            truncated = False

        sanitized = sanitize_transcript(content)
        if not sanitized.strip():
            return {"status": "error", "file": md_file.name, "error": "No dialogue found"}
    except Exception as e:
        return {"status": "error", "file": md_file.name, "error": str(e)}

    # Generate audio (delegate to core function with retry)
    try:
        generate_audio_with_retry(
            sanitized, wav_file, model_name, client,
            filename=md_file.name, semaphore=semaphore
        )
        return {"status": "success", "file": md_file.name, "truncated": truncated}
    except Exception as e:
        return {"status": "error", "file": md_file.name, "error": str(e)}


@app.command()
def main(
    input_path: Path = typer.Argument(
        ..., help="Path to transcript file or folder containing transcript files"
    ),
    model: str = typer.Option(
        "pro", "--model", "-m", help="Model to use: 'pro' or 'flash'"
    ),
    limit: int = typer.Option(
        None, "--limit", "-l", help="Limit transcript to first N characters for testing"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing audio files"
    ),
    no_merge: bool = typer.Option(
        False, "--no-merge", help="Skip merging WAV files into final MP3"
    ),
    output: Path = typer.Option(
        None, "--output", "-o", help="Output path for merged MP3 (default: <folder>/full-episode.mp3)"
    ),
    parallel: bool = typer.Option(
        False, "--parallel", help="Process files in parallel for faster generation"
    ),
    max_concurrent: int = typer.Option(
        3, "--max-concurrent", "-c", help="Maximum concurrent API calls (default: 3)"
    ),
):
    """
    Convert transcript markdown files to audio using Google Gemini TTS.

    Generates .wav files with the same name as input .md files.
    By default, merges all WAV files into a single MP3 at the end.
    Skips files with existing .wav files unless --overwrite is used.
    """

    # Validate input path
    if not input_path.exists():
        typer.echo(f"Error: Path '{input_path}' does not exist.", err=True)
        sys.exit(1)

    # Get list of files to process
    if input_path.is_file():
        if input_path.suffix != ".md":
            typer.echo(
                f"Error: File must be a .md file, got {input_path.suffix}", err=True
            )
            sys.exit(1)
        files_to_process = [input_path]
    else:
        files_to_process = sorted(input_path.glob("*.md"))
        if not files_to_process:
            typer.echo(f"Error: No .md files found in {input_path}", err=True)
            sys.exit(1)

    # Get model name
    model_name = get_model_name(model)

    # Display configuration
    typer.echo(f"Model: {model_name}")
    typer.echo(f"Files: {len(files_to_process)}")
    typer.echo(f"Mode: {'Parallel' if parallel else 'Sequential'}")
    if parallel:
        typer.echo(f"Max Concurrent: {max_concurrent}")
    if overwrite:
        typer.echo(f"Overwrite: Yes")
    typer.echo("")

    # Load settings and initialize Gemini client
    typer.echo("Initializing Gemini client...")
    try:
        settings = Settings()
        client = genai.Client(api_key=settings.gemini_api_key)
        typer.echo("✅ Client initialized\n")
    except Exception as e:
        typer.echo(f"❌ Error loading settings: {e}", err=True)
        typer.echo("Make sure GEMINI_API_KEY is set in your environment or .env file", err=True)
        sys.exit(1)

    # Create semaphore for limiting concurrent API calls
    semaphore = threading.Semaphore(max_concurrent) if parallel else None

    # Create closure to capture parameters
    def process_fn(md_file):
        return process_single_file_for_generation(
            md_file, model_name, client, overwrite, limit, semaphore
        )

    # Process files
    results = process_files(files_to_process, process_fn, parallel=parallel)

    # Count statuses (progress already shown in parallel mode)
    processed_count = skipped_count = error_count = 0
    for result in results:
        status = result["status"]
        if status == "success":
            processed_count += 1
        elif status == "skipped":
            skipped_count += 1
        elif status == "error":
            error_count += 1

    typer.echo(f"\n🎉 Done! Processed: {processed_count}, Skipped: {skipped_count}, Errors: {error_count}")
    if error_count > 0:
        typer.echo(f"⚠️  {error_count} file(s) had errors", err=True)

    # Merge WAV files into MP3 unless --no-merge is set
    if not no_merge and input_path.is_dir():
        typer.echo("\n" + "=" * 60)
        typer.echo("🎙️  MERGE PHASE")
        typer.echo("=" * 60 + "\n")

        # Determine output path for merged MP3
        if output is None:
            output = input_path / "full-episode.mp3"

        merge_wav_files(input_path, output)


@app.command()
def merge(
    input_folder: Path = typer.Argument(
        ..., help="Folder containing WAV files to merge"
    ),
    output: Path = typer.Option(
        ..., "--output", "-o", help="Output path for the merged MP3 file"
    ),
):
    """
    Merge all WAV files in a folder into a single MP3 file.

    WAV files are sorted alphabetically by filename before merging.
    """

    # Validate input folder
    if not input_folder.exists():
        typer.echo(f"Error: Folder '{input_folder}' does not exist.", err=True)
        sys.exit(1)

    if not input_folder.is_dir():
        typer.echo(f"Error: '{input_folder}' is not a folder.", err=True)
        sys.exit(1)

    # Call the merge function
    merge_wav_files(input_folder, output)


@app.command()
def cost(
    input_path: Path = typer.Argument(
        ..., help="Path to transcript file or folder containing transcript files"
    ),
    model: str = typer.Option(
        "pro", "--model", "-m", help="Model to use: 'pro' or 'flash'"
    ),
):
    """
    Estimate the cost of generating audio from transcript files.

    Analyzes transcript files and shows estimated costs before generation.
    """

    # Validate input path
    if not input_path.exists():
        typer.echo(f"Error: Path '{input_path}' does not exist.", err=True)
        sys.exit(1)

    # Get list of files to analyze
    if input_path.is_file():
        if input_path.suffix != ".md":
            typer.echo(
                f"Error: File must be a .md file, got {input_path.suffix}", err=True
            )
            sys.exit(1)
        files_to_process = [input_path]
    else:
        files_to_process = sorted(input_path.glob("*.md"))
        if not files_to_process:
            typer.echo(f"Error: No .md files found in {input_path}", err=True)
            sys.exit(1)

    # Get model name
    model_name = get_model_name(model)
    typer.echo(f"Cost Estimation for Model: {model_name}")
    typer.echo("=" * 80 + "\n")

    # Load settings
    try:
        settings = Settings()
    except Exception as e:
        typer.echo(f"Error loading settings: {e}", err=True)
        typer.echo("Make sure GEMINI_API_KEY is set in your environment or .env file", err=True)
        sys.exit(1)

    client = genai.Client(api_key=settings.gemini_api_key)

    # Analyze each file
    total_cost = total_duration = total_input_tokens = total_output_tokens = 0

    for md_file in files_to_process:
        # Read and sanitize
        try:
            content = md_file.read_text(encoding="utf-8")
            sanitized = sanitize_transcript(content)
            if not sanitized.strip():
                typer.echo(f"⚠️  {md_file.name}: No dialogue found")
                continue
        except Exception as e:
            typer.echo(f"❌ {md_file.name}: {e}", err=True)
            continue

        # Count tokens and calculate cost
        try:
            input_tokens = client.models.count_tokens(model=model_name, contents=sanitized).total_tokens
            audio_duration = estimate_audio_duration(sanitized)
            cost_info = calculate_cost(input_tokens, audio_duration, model_name)

            # Display and accumulate
            typer.echo(f"📄 {md_file.name}")
            typer.echo(f"   Input tokens:  {cost_info['input_tokens']:,}")
            typer.echo(f"   Output tokens: {cost_info['output_tokens']:,}")
            typer.echo(f"   Duration:      {cost_info['audio_duration_seconds']:.1f}s ({cost_info['audio_duration_seconds']/60:.2f} min)")
            typer.echo(f"   Cost:          ${cost_info['total_cost']:.4f}\n")

            total_input_tokens += cost_info['input_tokens']
            total_output_tokens += cost_info['output_tokens']
            total_duration += cost_info['audio_duration_seconds']
            total_cost += cost_info['total_cost']
        except Exception as e:
            typer.echo(f"❌ {md_file.name}: {e}\n", err=True)

    # Display summary
    typer.echo("=" * 80)
    typer.echo("📊 TOTAL SUMMARY")
    typer.echo(f"   Files:         {len(files_to_process)}")
    typer.echo(f"   Input tokens:  {total_input_tokens:,}")
    typer.echo(f"   Output tokens: {total_output_tokens:,}")
    typer.echo(f"   Duration:      {total_duration:.1f}s ({total_duration/60:.2f} min)")
    typer.echo(f"   Total cost:    ${total_cost:.4f}")
    typer.echo("")

    # Show pricing breakdown
    pricing = PRICING[model_name]
    typer.echo("💰 PRICING DETAILS")
    typer.echo(f"   Model:         {model_name}")
    typer.echo(f"   Input:         ${pricing['input']}/1M tokens")
    typer.echo(f"   Output:        ${pricing['output']}/1M tokens")
    typer.echo(f"   Output rate:   {OUTPUT_TOKENS_PER_SECOND} tokens/second of audio")


@app.command()
def stats(
    input_path: Path = typer.Argument(
        ..., help="Path to transcript file or folder containing transcript files"
    ),
):
    """
    Analyze speaker distribution and balance across transcript files.

    Shows word count per speaker to ensure balanced dialogue.
    """

    # Validate input path
    if not input_path.exists():
        typer.echo(f"Error: Path '{input_path}' does not exist.", err=True)
        sys.exit(1)

    # Get list of files to analyze
    if input_path.is_file():
        if input_path.suffix != ".md":
            typer.echo(
                f"Error: File must be a .md file, got {input_path.suffix}", err=True
            )
            sys.exit(1)
        files_to_process = [input_path]
    else:
        files_to_process = sorted(input_path.glob("*.md"))
        if not files_to_process:
            typer.echo(f"Error: No .md files found in {input_path}", err=True)
            sys.exit(1)

    typer.echo("Speaker Distribution Analysis")
    typer.echo("=" * 80 + "\n")

    # Aggregate totals across all files
    total_speaker_words = {}
    file_stats = []

    for md_file in files_to_process:
        try:
            content = md_file.read_text(encoding="utf-8")
            speaker_words = analyze_speaker_distribution(content)

            if not speaker_words:
                typer.echo(f"⚠️  {md_file.name}: No dialogue found\n")
                continue

            # Store per-file stats
            file_stats.append((md_file.name, speaker_words))

            # Accumulate totals
            for speaker, count in speaker_words.items():
                total_speaker_words[speaker] = total_speaker_words.get(speaker, 0) + count

        except Exception as e:
            typer.echo(f"❌ {md_file.name}: {e}\n", err=True)
            continue

    if not total_speaker_words:
        typer.echo("No speaker data found in any files.")
        sys.exit(0)

    # Display per-file breakdown
    typer.echo("PER-FILE BREAKDOWN")
    typer.echo("-" * 80 + "\n")

    for filename, speaker_words in file_stats:
        total_words = sum(speaker_words.values())
        typer.echo(f"📄 {filename}")

        for speaker in sorted(speaker_words.keys()):
            count = speaker_words[speaker]
            percentage = (count / total_words) * 100
            bar_length = int(percentage / 2)  # Scale to 50 chars max
            bar = "█" * bar_length
            typer.echo(f"   {speaker:8} {count:6,} words ({percentage:5.1f}%) {bar}")

        typer.echo("")

    # Display overall summary
    typer.echo("=" * 80)
    typer.echo("OVERALL SUMMARY")
    typer.echo("=" * 80 + "\n")

    total_words = sum(total_speaker_words.values())

    for speaker in sorted(total_speaker_words.keys()):
        count = total_speaker_words[speaker]
        percentage = (count / total_words) * 100
        bar_length = int(percentage / 2)  # Scale to 50 chars max
        bar = "█" * bar_length
        typer.echo(f"{speaker:8} {count:6,} words ({percentage:5.1f}%) {bar}")

    typer.echo(f"\n{'TOTAL':8} {total_words:6,} words")

    # Balance check
    typer.echo("\n" + "=" * 80)
    if len(total_speaker_words) == 2:
        speakers = list(total_speaker_words.keys())
        counts = [total_speaker_words[s] for s in speakers]
        balance_ratio = min(counts) / max(counts)
        typer.echo(f"⚖️  Balance Ratio: {balance_ratio:.2%}")

        if balance_ratio >= 0.45:
            typer.echo("   ✅ Well balanced dialogue")
        elif balance_ratio >= 0.35:
            typer.echo("   ⚠️  Slightly unbalanced - consider adjusting")
        else:
            typer.echo("   ❌ Significantly unbalanced - recommend rebalancing")


if __name__ == "__main__":
    app()
