import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()


app = Flask(__name__)

# --------------------------------------------------
# Fetch POTD URL
# --------------------------------------------------

def fetch_potd():
    GFG_POTD_API = os.getenv("GFG_API")

    res = requests.get(GFG_POTD_API, timeout=10)
    res.raise_for_status()

    data = res.json()

    return {
        "problem_url": data.get("problem_url")
    }
    
# --------------------------------------------------
# Extract Slug from URL
# --------------------------------------------------
def extract_slug_from_url(url):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")

    if len(parts) >= 2 and parts[0] == "problems":
        return parts[1]

    return None


# --------------------------------------------------
# Fetch Problem by Slug
# --------------------------------------------------

def fetch_problem(slug):
    problem_url = f"https://www.geeksforgeeks.org/problems/{slug}/1"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    res = requests.get(problem_url, headers=headers, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")

    if not script or not script.string:
        raise Exception("__NEXT_DATA__ not found")

    next_data = json.loads(script.string)

    problem_api = (
        next_data["props"]["pageProps"]
        ["initialState"]["problemApi"]["queries"]
    )

    dynamic_key = list(problem_api.keys())[0]
    problem = problem_api[dynamic_key]["data"]

    articles = problem.get("article_list", [])

    return {
        "content_title": problem.get("problem_name"),
        "html_description": problem.get("problem_question"),
        "difficulty": problem.get("difficulty"),
        "problem_url": next_data["props"]["pageProps"].get(
            "canonicalUrlWithOutQueryParams"
        ),
        "article_url": articles[0] if articles else None
    }



# --------------------------------------------------
# API: Fetch GFG Problem by URL
# --------------------------------------------------
@app.route("/api/v1/problem/<path:problem_url>", methods=["GET"])
def gfg_problem(problem_url):
    try:
        slug = extract_slug_from_url(problem_url)
        if not slug:
            return jsonify({"error": "Invalid GFG problem URL"}), 400

        problem = fetch_problem(slug)
        return jsonify(problem), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# API: GFG POTD
# --------------------------------------------------
@app.route("/api/v1/problem/potd", methods=["GET"])
def gfg_potd():
    try:
        potd = fetch_potd()
        problem_url = potd.get("problem_url")

        slug = extract_slug_from_url(problem_url)
        if not slug:
            return jsonify({"error": "Invalid GFG POTD URL"}), 400

        problem = fetch_problem(slug)
        return jsonify(problem), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --------------------------------------------------
# Run App
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
