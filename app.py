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


@app.route('/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/<path:problem_url>', methods=['GET'])
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

        input_part = None
        output_part = None
        explanation_part = None

        input_match = re.search(r"Input:\s*(.*)", text)
        output_match = re.search(r"Output:\s*(.*)", text)
        explanation_match = re.search(r"Explanation:\s*(.*)", text)

        if input_match:
            input_part = input_match.group(1)

        if output_match:
            output_part = output_match.group(1)

        if explanation_match:
            explanation_part = explanation_match.group(1)

        images = [img["src"] for img in example.find_all("img")]

        final_json["examples"].append({
            "input": input_part,
            "output": output_part,
            "images": images,
            "explanation": explanation_part
        })

    response = json.dumps(final_json, indent=4)
    print(response)

    return response, 200, {'Content-Type': 'application/json'}


@app.route('/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/potd', methods=['GET'])
def fetch_potd():
    load_dotenv()
    GFG_POTD_API = os.getenv("GFG_API")

    res = requests.get(GFG_POTD_API).json()
    potd_url = res['problem_url']

    response = requests.get(
        f"http://127.0.0.1:5000/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/{potd_url}"
    )

    return response.content, response.status_code, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(debug=True)