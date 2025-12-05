#!/usr/bin/env python3
"""
Script to add a new episode to The Pivot Podcast website.

Usage:
    python add_episode.py --drug minoxidil --disease alopecia
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from email.utils import formatdate


app = typer.Typer()


def get_mp3_size(mp3_path: Path) -> int:
    """Get the size of the MP3 file in bytes."""
    return mp3_path.stat().st_size


def get_episode_metadata(pair_folder: Path) -> dict:
    """Extract episode metadata from the episode structure file."""
    structure_file = pair_folder / "episode-structure.md"

    if not structure_file.exists():
        raise FileNotFoundError(f"Episode structure file not found: {structure_file}")

    content = structure_file.read_text()

    # Extract title (first heading)
    title_match = re.search(r"# Episode Structure: (.+)", content)
    title = title_match.group(1) if title_match else "Unknown Episode"

    # Extract cold open (description)
    cold_open_match = re.search(
        r"## 1\. THE COLD OPEN.*?\n\n(.+?)(?=\n\n---|\n\n##|$)",
        content,
        re.DOTALL
    )
    description = cold_open_match.group(1).strip() if cold_open_match else ""

    return {
        "title": title,
        "description": description,
    }


def add_episode_to_rss(
    feed_path: Path,
    episode_number: int,
    title: str,
    description: str,
    mp3_filename: str,
    mp3_size: int,
    duration_seconds: int,
    domain: str,
):
    """Add a new episode item to the RSS feed."""
    # Parse existing feed
    tree = ET.parse(feed_path)
    root = tree.getroot()
    channel = root.find("channel")

    # Create new item element
    item = ET.Element("item")

    # Add episode metadata
    ET.SubElement(item, "title").text = f"Episode {episode_number:02d}: {title}"
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}title").text = title
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}episode").text = str(episode_number)
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}episodeType").text = "full"
    ET.SubElement(item, "description").text = description
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}summary").text = description

    # Add enclosure (audio file)
    enclosure = ET.SubElement(item, "enclosure")
    enclosure.set("url", f"{domain}/episodes/{mp3_filename}")
    enclosure.set("length", str(mp3_size))
    enclosure.set("type", "audio/mpeg")

    # Add GUID
    guid = ET.SubElement(item, "guid")
    guid.set("isPermaLink", "false")
    guid.text = f"{mp3_filename.replace('.mp3', '')}-episode-{episode_number:02d}"

    # Add pub date (current date)
    pub_date = formatdate(timeval=None, localtime=False, usegmt=True)
    ET.SubElement(item, "pubDate").text = pub_date

    # Add duration
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}duration").text = str(duration_seconds)
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit").text = "no"

    # Add keywords
    keywords = f"drug repurposing, pharmaceutical, medicine, business"
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}keywords").text = keywords

    # Insert after the last item or at the end of channel
    items = channel.findall("item")
    if items:
        # Insert after the last item
        last_item_index = list(channel).index(items[-1])
        channel.insert(last_item_index + 1, item)
    else:
        # No items yet, append to channel
        channel.append(item)

    # Write back
    tree.write(feed_path, encoding="UTF-8", xml_declaration=True)

    # Pretty print (ElementTree doesn't do this well, so we'll do it manually)
    content = feed_path.read_text()
    feed_path.write_text(content)


def add_episode_to_html(
    html_path: Path,
    episode_number: int,
    title: str,
    description: str,
    mp3_filename: str,
    pub_date: str,
    duration_minutes: int,
):
    """Add a new episode card to the HTML index."""
    html_content = html_path.read_text()

    episode_card = f"""
            <article class="episode-card">
                <div class="episode-number">Episode {episode_number:02d}</div>
                <h3 class="episode-title">{title}</h3>
                <div class="episode-meta">
                    <span>📅 {pub_date}</span>
                    <span>⏱️ {duration_minutes} minutes</span>
                </div>
                <p class="episode-description">
                    {description}
                </p>
                <div class="episode-actions">
                    <a href="episodes/{mp3_filename}" class="btn btn-primary btn-small">
                        ▶️ Play Episode
                    </a>
                    <a href="episodes/{mp3_filename}" download class="btn btn-outline btn-small">
                        ⬇️ Download MP3
                    </a>
                </div>
            </article>
"""

    # Find the closing </section> of episodes-section and insert before it
    insertion_point = html_content.find("</section>", html_content.find('class="episodes-section"'))

    if insertion_point == -1:
        raise ValueError("Could not find episodes section in HTML")

    # Insert the new episode card
    new_content = html_content[:insertion_point] + episode_card + "\n        " + html_content[insertion_point:]

    html_path.write_text(new_content)


@app.command()
def main(
    drug: str = typer.Argument(..., help="Drug name (e.g., minoxidil)"),
    disease: str = typer.Argument(..., help="Disease name (e.g., alopecia)"),
    duration: Optional[int] = typer.Option(None, help="Episode duration in seconds (auto-calculated from MP3 if not provided)"),
    domain: str = typer.Option("YOUR_DOMAIN_HERE", help="Your podcast domain (e.g., https://pivot-podcast.com)"),
):
    """
    Add a new episode to The Pivot Podcast website.

    This script will:
    1. Copy the MP3 file to site/episodes/
    2. Add the episode to feed.xml
    3. Add the episode card to index.html
    """
    pair_name = f"pair-{drug}-{disease}"
    stories_folder = Path("stories") / pair_name
    transcript_folder = stories_folder / "transcript"

    # Find the MP3 file
    mp3_files = list(transcript_folder.glob("*.mp3"))
    if not mp3_files:
        typer.echo(f"❌ No MP3 file found in {transcript_folder}", err=True)
        raise typer.Exit(1)

    source_mp3 = mp3_files[0]
    typer.echo(f"📁 Found MP3: {source_mp3}")

    # Get episode metadata
    try:
        metadata = get_episode_metadata(stories_folder)
        typer.echo(f"📋 Title: {metadata['title']}")
    except Exception as e:
        typer.echo(f"⚠️  Could not extract metadata: {e}", err=True)
        metadata = {"title": f"{drug.title()} - {disease.title()}", "description": ""}

    # Setup paths
    site_folder = Path("site")
    episodes_folder = site_folder / "episodes"
    episodes_folder.mkdir(parents=True, exist_ok=True)

    mp3_filename = f"{drug}-{disease}.mp3"
    dest_mp3 = episodes_folder / mp3_filename

    # Copy MP3
    import shutil
    shutil.copy2(source_mp3, dest_mp3)
    typer.echo(f"✅ Copied MP3 to: {dest_mp3}")

    # Get MP3 size
    mp3_size = get_mp3_size(dest_mp3)
    typer.echo(f"📊 MP3 size: {mp3_size:,} bytes ({mp3_size / 1024 / 1024:.1f} MB)")

    # Calculate duration if not provided
    if duration is None:
        # Estimate: 128kbps MP3 = 16 KB/s
        duration = int(mp3_size / 16000)
        typer.echo(f"⏱️  Estimated duration: {duration // 60} minutes ({duration} seconds)")

    # Determine episode number (count existing items in RSS)
    feed_path = site_folder / "feed.xml"
    tree = ET.parse(feed_path)
    existing_items = tree.getroot().find("channel").findall("item")
    episode_number = len(existing_items) + 1
    typer.echo(f"🔢 Episode number: {episode_number}")

    # Add to RSS feed
    add_episode_to_rss(
        feed_path=feed_path,
        episode_number=episode_number,
        title=metadata["title"],
        description=metadata["description"],
        mp3_filename=mp3_filename,
        mp3_size=mp3_size,
        duration_seconds=duration,
        domain=domain,
    )
    typer.echo(f"✅ Added episode to RSS feed: {feed_path}")

    # Add to HTML
    pub_date = datetime.now().strftime("%B %d, %Y")
    add_episode_to_html(
        html_path=site_folder / "index.html",
        episode_number=episode_number,
        title=metadata["title"],
        description=metadata["description"],
        mp3_filename=mp3_filename,
        pub_date=pub_date,
        duration_minutes=duration // 60,
    )
    typer.echo(f"✅ Added episode to HTML: {site_folder / 'index.html'}")

    typer.echo("\n🎉 Episode added successfully!")
    typer.echo(f"\n📝 Next steps:")
    typer.echo(f"   1. Review the changes in site/")
    typer.echo(f"   2. If domain is still YOUR_DOMAIN_HERE, update it:")
    typer.echo(f"      sed -i '' 's|YOUR_DOMAIN_HERE|https://your-domain.com|g' site/index.html site/feed.xml")
    typer.echo(f"   3. Deploy the site/ folder to your hosting provider")


if __name__ == "__main__":
    app()
