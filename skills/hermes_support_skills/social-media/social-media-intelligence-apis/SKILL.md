---
name: social-media-intelligence-apis
description: Extract social metrics, comments, and engagement data.
platforms: [linux, macos, windows]
---

# Social Media Intelligence & API Extraction Playbook

Panduan komprehensif untuk mengekstrak metrik, postingan, views, likes, shares, dan komentar dari berbagai platform media sosial (Instagram, TikTok, YouTube, Facebook, X/Twitter) guna analisis digital marketing, audit konten, dan intent mining.

---

## 1. Arsitektur Ekstraksi Data Sosial

```
[Social Media URL / Handle]
         │
         ├──► 1. Native CLI / Metadata Extraction (yt-dlp, curl, regex)
         │       └─ Ekstraksi caption, likes, audio, uploader tanpa login
         │
         ├──► 2. Cloud Actor / Microservice Scrapers (Apify / RapidAPI)
         │       └─ Ekstraksi views riil, nested comments, profile followers, reach
         │
         ├──► 3. Official Developer Graph API (Meta, TikTok Business, YouTube Data)
         │       └─ Ekstraksi private insights (Saves, Accounts Reached, Video Plays)
         │
         ▼
[Python AI Intelligence Engine]
         │
         ├──► Hook Strength Score & Thumb-Stopper Rating (1-100)
         ├──► True Engagement Rate: (Likes + Comments + Shares + Saves) / Reach
         ├──► NLP Comment Intent Mining (Buying Leads vs General Discussion)
         └──► Actionable Paid Ads & Organic Scaling Playbook
```

---

## 2. Metode Ekstraksi per Platform

### A. Instagram (Reels & Feed Posts)
* **Metadata & Caption (Tanpa Login):**
  ```bash
  yt-dlp --dump-json --no-warnings "https://www.instagram.com/reel/SHORTCODE/"
  ```
  *Mengembalikan:* `title`, `description` (caption lengkap), `like_count`, `comment_count`, `uploader`.
* **Full Comment & Plays Extraction (Cloud Proxy / Apify Actor):**
  * Endpoint: `apify/instagram-scraper` atau `apify/instagram-comment-scraper`
  * Input: `{"directUrls": ["https://www.instagram.com/reel/SHORTCODE/"], "resultsType": "comments"}`
  * Output: Array komentar lengkap (`text`, `ownerUsername`, `likesCount`, `timestamp`).

### B. TikTok (Videos & Profiles)
* **Video Metrics & Sound:**
  ```bash
  yt-dlp --dump-json "https://www.tiktok.com/@username/video/VIDEO_ID"
  ```
* **Comment & Share Velocity:**
  * Endpoint: `clockworks/tiktok-scraper` atau `apify/tiktok-comments-scraper`
  * Parameter: `videoViews`, `likes`, `shares`, `commentCount`.

### C. YouTube (Shorts & Long Videos)
* **Video Analytics:**
  ```bash
  yt-dlp --dump-json "https://www.youtube.com/watch?v=VIDEO_ID"
  ```
  *Mengembalikan:* `view_count` riil, `like_count`, `comment_count`, `tags`, `categories`.
* **YouTube Data API v3:**
  ```http
  GET https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=VIDEO_ID&key=API_KEY
  ```

---

## 3. Rumus & Metrik Analisis Digital Marketing

### 1. True Engagement Rate (True ER %)
$$\text{True ER} = \frac{\text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}}{\text{Estimated Views / Reach}} \times 100$$
* **Benchmark:**
  * `< 1.5%`: Low engagement / Need Hook & CTA overhaul.
  * `1.5% - 4.0%`: Healthy industry standard.
  * `> 4.0%`: High viral traction / Ready to scale with Paid Ads.

### 2. Virality & Share Multiplier
$$\text{Virality Score} = \frac{\text{Shares}}{\text{Likes}} \times 100$$
* Indikator apakah konten memiliki nilai retensi tinggi dan memicu percakapan organik antar audiens.

### 3. Hook Strength Score (0 - 100)
Evaluasi kekuatan visual dan teks pembuka 3 detik pertama berdasarkan deteksi NLP pattern:
* *Visionary Statement:* +18 poin
* *Actionable How-To:* +20 poin
* *Fear Of Missing Out (Negative Bias):* +25 poin
* *Hands-On Interactive Demo:* +22 poin
* *Transformation Proof (Before/After):* +24 poin

---

## 4. NLP Intent Mining (Klasifikasi Komentar Prospek)

Ekstrak prospek bernilai tinggi dari komentar publik:
1. **High Buying Intent (Hot Lead):** Mengandung kata *"harga", "biaya", "pricelist", "cara order", "DM min", "paket"*.
2. **Consultation / Service Need:** Mengandung kata *"konsultasi", "demo", "jadwal", "bisa datang ke kampus/kantor"*.
3. **Location / Accessibility:** Mengandung kata *"lokasi", "alamat", "cabang", "daerah mana"*.
4. **Social Proof & Value Retention:** Mengandung kata *"save", "bermanfaat banget", "keren", "izin share"*.

---

## 5. Implementasi Python FastAPI

```python
import subprocess, json

def extract_social_post(url: str) -> dict:
    cmd = ["yt-dlp", "--dump-json", "--no-warnings", url]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if res.returncode == 0 and res.stdout.strip():
        data = json.loads(res.stdout)
        return {
            "title": data.get("title"),
            "caption": data.get("description"),
            "uploader": data.get("uploader"),
            "likes": data.get("like_count", 0),
            "comments": data.get("comment_count", 0),
            "views": data.get("view_count", 0)
        }
    return {}
```
