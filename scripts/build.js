import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.dirname(__dirname);
const storiesDir = path.join(rootDir, "stories");
const episodesDir = path.join(rootDir, "docs", "episodes");
const episodesJsonPath = path.join(rootDir, "episodes.json");

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function copyMp3Files() {
  ensureDir(episodesDir);

  const episodes = JSON.parse(fs.readFileSync(episodesJsonPath, "utf-8"));

  for (const episode of episodes) {
    const sourceDir = path.join(storiesDir, `pair-${episode.drug}-${episode.disease}`, "transcript");
    // Use source_mp3 if provided, otherwise use mp3_filename to find the source
    const sourceFilename = episode.source_mp3 || episode.mp3_filename;
    const sourceFile = path.join(sourceDir, sourceFilename);
    const destFile = path.join(episodesDir, episode.mp3_filename);

    if (fs.existsSync(sourceFile)) {
      if (!fs.existsSync(destFile)) {
        fs.copyFileSync(sourceFile, destFile);
        console.log(`📁 Copied: ${episode.mp3_filename}`);
      } else {
        console.log(`⏭️  Skipped (exists): ${episode.mp3_filename}`);
      }
    } else {
      console.warn(`⚠️  Not found: ${sourceFile}`);
    }
  }
}

try {
  console.log("🔨 Building...\n");
  console.log("📋 Copying MP3 files...");
  copyMp3Files();
  console.log("\n✅ Build complete!");
} catch (error) {
  console.error("❌ Build failed:", error.message);
  process.exit(1);
}
