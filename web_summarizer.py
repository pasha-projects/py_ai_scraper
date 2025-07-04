import os
import requests
import re
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import textwrap

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Did you forget the .env file?")

client = OpenAI(api_key=api_key)

def clean_text(text):
    text = re.sub(r"(Watch.*on YouTube|Subscribe.*channel|Follow.*)", "", text, flags=re.I)
    text = re.sub(r"(Written by|About the author).*", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
    return text.strip()

def extract_article_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('article') or soup.find('main') or soup.body
    return main.get_text(separator=' ', strip=True) if main else soup.get_text()

def summarize_url(url):
    response = requests.get(url, timeout=10)
    raw_text = extract_article_text(response.content)
    cleaned = clean_text(raw_text)

    # Limit by words instead of characters (~1500 words ≈ 2000 tokens)
    words = cleaned.split()
    limited_text = ' '.join(words[:1500])

    summary_prompt = [
        {
            "role": "system",
            "content": textwrap.dedent("""
                You are a research assistant summarizing online articles.
                Ignore superficial or promotional statements like “Watch this on YouTube.”
                Focus on key arguments, evidence, insights, and implications.

                Return 6–8 bullet points capturing the most important, *non-obvious* takeaways.
            """)
        },
        {
            "role": "user",
            "content": limited_text
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",  # use "gpt-4o" if possible; fallback to "gpt-3.5-turbo"
        messages=summary_prompt,
        temperature=0.3
    )

    summary = response.choices[0].message.content.strip()
    summary = summary.replace("\n", "\n\n")

    return textwrap.dedent(f"""
    Summary of: {url}

    {summary}
    """).strip()
