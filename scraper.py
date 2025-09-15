#!/usr/bin/env python3
"""
AI Competitor Tracker - Web Scraper
Monitors competitor websites and generates daily reports
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time


class CompetitorScraper:
    def __init__(self, config_file='config.json'):
        """Initialize the scraper with configuration"""
        self.config = self.load_config(config_file)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CompetitorTracker/1.0)'
        })

    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using default settings.")
            return self.get_default_config()

    def get_default_config(self):
        """Return default configuration"""
        return {
            "competitors": {
                "OpenAI": {
                    "blog_url": "https://openai.com/blog",
                    "selectors": {
                        "title": "h3 a",
                        "date": ".published-date",
                        "summary": ".excerpt"
                    }
                },
                "Google AI": {
                    "blog_url": "https://ai.googleblog.com/",
                    "selectors": {
                        "title": ".post-title a",
                        "date": ".published",
                        "summary": ".post-body"
                    }
                }
            },
            "max_articles": 5,
            "delay_between_requests": 2
        }

    def scrape_competitor(self, name, config):
        """Scrape articles from a single competitor"""
        print(f"Scraping {name}...")

        try:
            response = self.session.get(config['blog_url'], timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            # Find article titles
            title_elements = soup.select(config['selectors']['title'])[:self.config['max_articles']]

            for title_element in title_elements:
                article = {
                    'title': title_element.get_text().strip(),
                    'url': title_element.get('href', ''),
                    'source': name,
                    'scraped_at': datetime.now().isoformat()
                }

                # Make URL absolute if it's relative
                if article['url'] and not article['url'].startswith('http'):
                    base_url = '/'.join(config['blog_url'].split('/')[:3])
                    article['url'] = base_url + article['url']

                articles.append(article)

            print(f"Found {len(articles)} articles from {name}")
            return articles

        except Exception as e:
            print(f"Error scraping {name}: {str(e)}")
            return []

    def scrape_all_competitors(self):
        """Scrape all configured competitors"""
        all_articles = []

        for name, config in self.config['competitors'].items():
            articles = self.scrape_competitor(name, config)
            all_articles.extend(articles)

            # Delay between requests to be respectful
            time.sleep(self.config['delay_between_requests'])

        return all_articles

    def generate_report(self, articles):
        """Generate a markdown report from scraped articles"""
        today = datetime.now().strftime('%Y-%m-%d')
        report_content = f"""# AI Competitive Intelligence Report
**Date**: {today}
**Articles Found**: {len(articles)}

## Summary
This report contains the latest updates from key AI companies and competitors.

"""

        # Group articles by source
        by_source = {}
        for article in articles:
            source = article['source']
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(article)

        # Generate sections for each competitor
        for source, source_articles in by_source.items():
            report_content += f"## {source} ({len(source_articles)} articles)\n\n"

            for article in source_articles:
                report_content += f"### {article['title']}\n"
                if article['url']:
                    report_content += f"**Link**: [{article['url']}]({article['url']})\n"
                report_content += f"**Scraped**: {article['scraped_at']}\n\n"

        return report_content

    def save_report(self, report_content):
        """Save the report to a file"""
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)

        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"reports/ai_competitive_report_{today}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Report saved to {filename}")
        return filename

    def run_daily_scrape(self):
        """Run the complete daily scraping process"""
        print("Starting daily competitive intelligence scrape...")

        # Scrape all competitors
        articles = self.scrape_all_competitors()

        if articles:
            # Generate and save report
            report = self.generate_report(articles)
            filename = self.save_report(report)

            print(f"Daily scrape completed successfully!")
            print(f"Report saved: {filename}")
            print(f"Total articles found: {len(articles)}")
        else:
            print("No articles found during scraping.")


def main():
    """Main function to run the scraper"""
    scraper = CompetitorScraper()
    scraper.run_daily_scrape()


if __name__ == "__main__":
    main()