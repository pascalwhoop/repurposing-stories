import fs from "fs";
import path from "path";
import { Feed } from "feed";

const episodesPath = path.join(process.cwd(), "episodes.json");
const feedPath = path.join(process.cwd(), "docs", "feed.xml");

try {
  const episodes = JSON.parse(fs.readFileSync(episodesPath, "utf-8"));

  const feed = new Feed({
    title: "The Pivot - Drug Repurposing Stories",
    description:
      "The Pivot analyzes the business and science of repurposed drugs, modeled after the structure of the Acquired podcast. Each episode deep-dives into a drug that failed at its original purpose but found massive success in treating a completely different condition.",
    id: "https://pascalwhoop.github.io/repurposing-stories",
    link: "https://pascalwhoop.github.io/repurposing-stories",
    language: "en",
    copyright: "© 2025 The Pivot Podcast",
    author: {
      name: "The Pivot Podcast",
      email: "contact@pascalwhoop.com",
    },
    favicon: "https://pascalwhoop.github.io/repurposing-stories/artwork.jpg",
    feedLinks: {
      rss2: "https://pascalwhoop.github.io/repurposing-stories/feed.xml",
    },
  });

  // Add categories
  feed.addCategory("Science");
  feed.addCategory("Business");

  // Add episodes (in reverse order so newest first)
  episodes.sort((a, b) => b.episode_number - a.episode_number).forEach((episode) => {
    feed.addItem({
      title: `Episode ${String(episode.episode_number).padStart(2, "0")}: ${episode.title}`,
      id: `${episode.mp3_filename.replace(".mp3", "")}-episode-${String(episode.episode_number).padStart(2, "0")}`,
      link: "https://pascalwhoop.github.io/repurposing-stories",
      description: episode.description,
      content: episode.description,
      author: [
        {
          name: "The Pivot Podcast",
          email: "contact@pascalwhoop.com",
        },
      ],
      date: new Date(episode.pub_date),
      enclosure: {
        url: `https://pascalwhoop.github.io/repurposing-stories/episodes/${episode.mp3_filename}`,
        type: "audio/mpeg",
      },
      extensions: [
        {
          name: "itunes",
          objects: {
            author: "The Pivot Podcast",
            explicit: "no",
            duration: episode.duration_seconds,
            keywords: "drug repurposing, pharmaceutical, medicine, business",
            summary: episode.description,
            image: "https://pascalwhoop.github.io/repurposing-stories/artwork.jpg",
          },
        },
      ],
    });
  });

  fs.writeFileSync(feedPath, feed.rss2(), "utf-8");
  console.log(`✅ Generated: ${feedPath}`);
} catch (error) {
  console.error("❌ Error generating feed:", error.message);
  process.exit(1);
}
