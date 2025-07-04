# pi_ai_scraper

AI-powered web scraper built with Python.  
Fetches, summarizes, and emails web content using OpenAI and Gmail.

## Features
- Scrapes web pages using BeautifulSoup
- Summarizes text with OpenAI API
- Sends results via email (Gmail + App Password)

# Technologies Used

- Python 3.x – Core language.
- BeautifulSoup – HTML parsing and cleanup.
- OpenAI GPT API – Natural language summarization.
- smtplib + Gmail SMTP – Secure email sending.
- dotenv – Secure environment variable management.

## Requirements
- Python 3.8+
- OpenAI API key
- Gmail app password (for sending email)

## Usage

python email_web_summary.py

## Installation

1. Clone the repository:

    git clone git@github.com:pasha-projects/py_ai_scraper.git
    cd py_ai_scraper

2. Create a .env file with the following variables

    OPENAI_API_KEY=your_openai_api_key
    SENDER_EMAIL=your_gmail_address
    GMAIL_APP_PASSWORD=your_gmail_app_password
