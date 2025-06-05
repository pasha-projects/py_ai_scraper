import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import textwrap

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Did you forget the .env file?")

client = OpenAI(api_key=api_key)

def summarize_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text = ' '.join(text.split())  # collapse whitespace
    text = text[:3000]  # trim if needed

    summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize this webpage in 5 bullet points."},
            {"role": "user", "content": text}
        ]
    ).choices[0].message.content.strip()

    # Add paragraph spacing
    summary = summary.replace("\n", "\n\n")

    formatted = textwrap.dedent(f"""
    Summary of: {url}

    {summary}
    """).strip()

    return formatted
