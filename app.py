import re
import os
import json
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)


def load_page_with_js(url):
    """Load page fully rendered with JS using Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")
        html = page.content()

        browser.close()
        return html

def parse_example_block(text: str):
    lines = text.split("\n")

    input_part = []
    output_part = []
    explanation_part = []

    current = None  # can be "input", "output", "explanation"

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Input"):
            current = "input"
            continue
        if stripped.startswith("Output"):
            current = "output"
            continue
        if stripped.startswith("Explanation"):
            current = "explanation"
            continue
        if stripped.startswith("Constraints"):
            current = None
            continue

        if stripped == ":":
            continue

        if current == "input":
            input_part.append(stripped)
        elif current == "output":
            output_part.append(stripped)
        elif current == "explanation":
            explanation_part.append(stripped)

    return {
        "input": "\n".join(input_part).strip() or None,
        "output": "\n".join(output_part).strip() or None,
        "explanation": "\n".join(explanation_part).strip() or None
    }


@app.route('/api/v1/geeksforgeeks/problem/<path:problem_url>', methods=['GET'])
def fetch_problem(problem_url):

    load_dotenv()
    PROBLEM_CONTENT = os.getenv("PROBLEM_CONTENT")
    print(f"Problem URL: {problem_url}")

    # ---- Load page with JS support ----
    html = load_page_with_js(problem_url)

    soup = BeautifulSoup(html, "html.parser")

    # ---- Extract Title ----
    title = soup.find('title').get_text()
    print("Title:", title)

    # ---- Extract main content ----
    target = soup.find('div', class_=PROBLEM_CONTENT)

    final_json = {
        "title": title,
        "description": [],
        "examples": [],
        "problem_url": problem_url
    }

    # ---- DESCRIPTION ----
    paragraphs = target.find_all('p')
    for para in paragraphs:
        p = para.get_text().strip()
        if p.lower().startswith('constraint') or p.lower().startswith('example') or p == '':
            continue
        final_json["description"].append(p)

    # ---- EXAMPLES ----
    examples = target.find_all('pre')
    for example in examples:
        text = example.get_text("\n", strip=True)
        parsed = parse_example_block(text)

        images = [img["src"] for img in example.find_all("img")]

        final_json["examples"].append({
            "input": parsed["input"],
            "output": parsed["output"],
            "images": images,
            "explanation": parsed["explanation"]
        })


    response = json.dumps(final_json, indent=4, ensure_ascii=False)
    print(response)

    return response, 200, {'Content-Type': 'application/json'}


@app.route('/api/v1/geeksforgeeks/problem/potd', methods=['GET'])
def fetch_potd():
    load_dotenv()
    GFG_POTD_API = os.getenv("GFG_API")

    res = requests.get(GFG_POTD_API).json()
    potd_url = res['problem_url']

    response = requests.get(
        f"http://localhost:5000/api/v1/geeksforgeeks/problem/{potd_url}"
    )

    return response.content, response.status_code, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True)