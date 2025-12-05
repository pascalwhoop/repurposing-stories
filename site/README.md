# The Pivot Podcast - Static Website

This directory contains the static website and podcast RSS feed for "The Pivot" podcast.

## 📁 Directory Structure

```
site/
├── index.html          # Main website homepage
├── feed.xml            # Podcast RSS feed
├── episodes/           # Audio files
│   └── minoxidil-alopecia.mp3
└── README.md           # This file
```

## 🚀 Deployment Instructions

### Step 1: Configure Your Domain

Before deploying, you need to replace `YOUR_DOMAIN_HERE` with your actual domain in these files:

1. **index.html** - Line ~48, 51, and 54 (subscribe buttons)
2. **feed.xml** - Lines 5, 20, 27, and 38 (various URLs)

Example: If your domain is `https://pivot-podcast.com`, replace all instances:
```bash
# From the site/ directory:
sed -i '' 's|YOUR_DOMAIN_HERE|https://pivot-podcast.com|g' index.html feed.xml
```

Also update `YOUR_EMAIL_HERE` in feed.xml (line 21) with a contact email.

### Step 2: Optional - Add Podcast Artwork

If you want podcast artwork (recommended for better podcast app display):

1. Create a square image (1400x1400px minimum, 3000x3000px recommended)
2. Save it as `artwork.jpg` in the `site/` directory
3. The feed.xml already references it

### Step 3: Choose a Hosting Provider

This is a static site and can be hosted anywhere. Here are some free options:

#### Option A: GitHub Pages (Free)
```bash
# Initialize git repo in site/ directory
cd site
git init
git add .
git commit -m "Initial podcast site"

# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/pivot-podcast.git
git push -u origin main

# Enable GitHub Pages in repo settings
# Your site will be at: https://yourusername.github.io/pivot-podcast/
```

#### Option B: Netlify (Free)
1. Create account at netlify.com
2. Drag and drop the `site/` folder
3. Your site will be live at a random URL (can customize)

#### Option C: Cloudflare Pages (Free)
1. Create account at pages.cloudflare.com
2. Upload the `site/` directory
3. Configure custom domain if desired

#### Option D: AWS S3 + CloudFront (Paid, but cheap)
```bash
# Install AWS CLI, then:
aws s3 sync . s3://your-bucket-name --acl public-read
# Configure CloudFront for HTTPS and custom domain
```

### Step 4: Share the Magic Link

Once deployed, share the **podcast protocol link** with your audience:

**For iPhone users:**
```
podcast://your-domain.com/feed.xml
```

**For Android users:**
```
pcast://your-domain.com/feed.xml
```

**Universal landing page:**
```
https://your-domain.com
```

## 📱 How Users Subscribe

### iPhone
1. User clicks the `podcast://` link
2. iOS shows dialog: "Open in Podcasts?"
3. User taps "Open"
4. Apple Podcasts opens and shows your podcast
5. User subscribes and can download episodes

### Android
1. User clicks the `pcast://` link (works with many podcast apps)
2. Or they can manually add the RSS feed URL in their podcast app
3. Or they visit the website and download the MP3 directly

## 🔒 Privacy Note

This is a "private by obscurity" podcast. Anyone with the feed URL can subscribe. To make it more secure:

1. Use a non-obvious directory name (e.g., `x8s7_podcast` instead of `pivot-podcast`)
2. Add a `robots.txt` to prevent search engine indexing:
   ```
   User-agent: *
   Disallow: /
   ```
3. For true privacy, you'd need authentication (beyond static hosting)

## 🔄 Adding New Episodes

1. Generate the new episode audio using the transcript CLI
2. Copy the MP3 file to `site/episodes/`
3. Add a new episode card to `index.html`
4. Add a new `<item>` block to `feed.xml`
5. Redeploy the site

You can use this script to automate it:

```bash
# From the project root
python add_episode.py --drug "sildenafil" --disease "pulmonary-hypertension"
```

## 📊 Episode Metadata

Each episode in the RSS feed needs:
- **Title**: Episode name
- **Description**: Episode summary
- **enclosure url**: Direct link to MP3 file
- **length**: File size in bytes
- **duration**: Length in seconds
- **pubDate**: Publication date in RFC 2822 format
- **guid**: Unique identifier

## 🛠️ Testing Locally

To test the site locally before deploying:

```bash
# Simple Python server
cd site
python3 -m http.server 8000

# Visit: http://localhost:8000
```

**Note**: The `podcast://` protocol links won't work locally - you need to test them after deployment.

## 📞 Support

If users have trouble subscribing:
1. Send them the direct RSS feed URL: `https://your-domain.com/feed.xml`
2. They can manually add it in their podcast app's settings (usually under "Add by URL")
3. As a fallback, they can download MP3s directly from the website
