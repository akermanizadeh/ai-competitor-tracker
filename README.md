# AI Competitor Tracker

A simple web scraping application that monitors AI companies and generates daily competitive intelligence reports.

This project serves as a complete tutorial example for learning web scraping, Claude Code, and GitHub workflows.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper**:
   ```bash
   python scraper.py
   ```

3. **Check the generated report**:
   Reports are saved in the `reports/` directory with the format: `ai_competitive_report_YYYY-MM-DD.md`

## Features

- Scrapes latest blog posts from major AI companies
- Generates markdown reports with article summaries
- Configurable through `config.json`
- Respectful scraping with delays between requests
- Error handling and retry logic

## Configuration

Edit `config.json` to:
- Add/remove competitor websites
- Adjust CSS selectors for different site layouts
- Change scraping frequency and limits
- Modify request delays and timeouts

## Monitored Companies

- OpenAI
- Google AI
- Microsoft AI
- DeepMind

## Tutorial

This project was built following the Claude Code tutorial for beginners. It demonstrates:
- Setting up a GitHub repository
- Using Claude.md for project documentation
- Building a web scraper with Python
- Working with VS Code and Claude Code
- Git workflow with commits and pull requests

## Files Structure

```
ai-competitor-tracker/
├── Claude.md           # Project overview for Claude Code
├── README.md          # This file
├── scraper.py         # Main scraping logic
├── config.json        # Website URLs and settings
├── requirements.txt   # Python dependencies
└── reports/           # Generated daily reports
    └── .gitkeep
```

## Next Steps

- Add email notifications
- Implement automated scheduling
- Add more competitor sources
- Improve article content extraction
- Add sentiment analysis