# 🧑‍💼 GetCoditer

A minimal Python tool to automatically find and extract developer candidate data from Reddit’s **“Who’s looking for work?”** monthly megathreads (e.g. r/DevelopersIndia).

Useful for:
- Recruiters & hiring managers
- Developer communities
- Resume or CV aggregators
- Job boards and bots

---

## 🔍 Features

- **Auto-locates** the latest “Monthly Megathread” post.
- **Scrapes title, body**, and **top-level comments**.
- Filters out deleted/empty replies.
- Extracts useful details like:
  - Tech stack
  - Resume links
  - Availability and location
- Extensible with:
  - SQLite DB insert
  - Telegram bot interface

---

## 🚀 Quick Start

### 1. Clone the repository

```bash

cd GetCoditer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests
```

### 3. Run the scraper

```bash
python routine.py
```

It will fill data into SQLite. You can add a cron job for automation.


## 💬 Telegram Bot Setup

You can interact with your scraped candidate data via Telegram using the provided bot file: `DItele_bot.py`.


---

## 🧪 Sample Output

```
📝 Who's looking for work? - Monthly Megathread - June 2025

📄 I'm a backend developer from Mumbai, 5+ years experience in Node.js and Go. Open to remote roles...

🗨️ Comments:
1. johndoe123 (32 pts): Full-stack engineer, React/Django, 4 YOE. Portfolio: johndoe.dev
2. devgirl (15 pts): Frontend only, TS + Tailwind. Remote only. Resume: devgirl.site
```

---

## ⚙️ Config

You can customize:

- `SUBREDDIT`: default is `developersIndia`
- `MEGATHREAD_QUERY`: auto-matches monthly threads (e.g., “Who’s looking for work?”)

---

## ✅ Use Cases

- Feed scraped comments to a database (SQLite or MongoDB).
- Filter candidates by tech, location, experience.
- Serve them via Telegram bot with inline query.

---

## 🤝 Contributing

PRs welcome. Open issues or drop your suggestions, it is extensible.

---

## ⭐️ Star if Useful!

If this saves you time, consider starring the repo. 
