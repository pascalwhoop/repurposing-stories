import fs from "fs";
import path from "path";

const episodesPath = path.join(process.cwd(), "episodes.json");
const htmlPath = path.join(process.cwd(), "docs", "index.html");
const templatePath = path.join(process.cwd(), "scripts", "index.template.html");

try {
  const episodes = JSON.parse(fs.readFileSync(episodesPath, "utf-8"));
  const template = fs.readFileSync(templatePath, "utf-8");

  // Generate episode cards
  const episodeCards = episodes
    .sort((a, b) => b.episode_number - a.episode_number)
    .map((episode) => {
      const drug = episode.drug;
      const disease = episode.disease;
      const githubUrl = `https://github.com/pascalwhoop/repurposing-stories/tree/main/stories/pair-${drug}-${disease}`;
      const durationMinutes = Math.floor(episode.duration_seconds / 60);

      return `            <article class="episode-card">
                <div class="episode-number">Episode ${String(episode.episode_number).padStart(2, "0")}</div>
                <h3 class="episode-title">${escapeHtml(episode.title)}</h3>
                <div class="episode-meta">
                    <span>📅 ${escapeHtml(episode.pub_date)}</span>
                    <span>⏱️ ${durationMinutes} minutes</span>
                </div>
                <p class="episode-description">
                    ${escapeHtml(episode.description)}
                </p>
                <div class="episode-actions">
                    <a href="episodes/${escapeHtml(episode.mp3_filename)}" class="btn btn-primary btn-small">
                        ▶️ Play Episode
                    </a>
                    <a href="episodes/${escapeHtml(episode.mp3_filename)}" download class="btn btn-outline btn-small">
                        ⬇️ Download MP3
                    </a>
                    <a href="${githubUrl}" class="btn btn-outline btn-small" target="_blank">
                        📚 Show Notes
                    </a>
                </div>
            </article>
`;
    })
    .join("\n");

  // Replace placeholder in template
  const html = template.replace("<!-- EPISODES_PLACEHOLDER -->", episodeCards);

  fs.writeFileSync(htmlPath, html, "utf-8");
  console.log(`✅ Generated: ${htmlPath}`);
} catch (error) {
  console.error("❌ Error generating HTML:", error.message);
  process.exit(1);
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}
