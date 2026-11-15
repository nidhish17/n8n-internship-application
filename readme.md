# 🤖 InternAgent

An AI-powered internship automation system built with **Python, SQLite, n8n, and LLMs**.

## Features

- **Internship Scraper:** Asynchronously fetches internships and stores them in SQLite using Peewee ORM.
- **Resume Extraction:** Extracts skills, projects, and experience from resumes.
- **AI Matching:** Evaluates internships against the candidate's resume.
- **Message Generation:** Creates personalized recruiter messages.
- **Application Automation:** Authenticated application submission.

## Tech Stack

`Python` · `HTTPX` · `asyncio` · `Peewee` · `SQLite` · `n8n` · `Docker` · `LLMs`

## Project Structure

```text
internAgent/
├── n8n workflows/
│   ├── Main Internship Extractor.json
│   ├── resume extractor.json
│   └── internship applier.json
├── scraper/
│   ├── database/
│   │   └── db_schema.py
│   └── main.py
└── .gitignore
```

## Workflow

```text
Scrape Internships → SQLite
         ↓
Extract Resume + Job Details
         ↓
AI Suitability Evaluation
         ↓
Generate Recruiter Message
         ↓
Store Results in n8n Data Tables
         ↓
Review & Apply (In Progress)
```

## Roadmap

- [x] Async internship scraping
- [x] Resume extraction
- [x] AI-based internship matching
- [x] Personalized message generation
- [x] Store matching results
- [x] Automated application submission
- [ ] Application status tracking
- [ ] Telegram/email notifications
