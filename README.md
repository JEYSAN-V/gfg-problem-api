**Web Scrapping — Problem of the Day Fetcher**

Short, focused script that fetches a programming "Problem of the Day" page (currently GeeksforGeeks), extracts the title, description and examples, and prints a JSON summary to the console.

**Features:**
- **Scrapes** problem pages using Selenium + BeautifulSoup.
- **Parses** description paragraphs and example blocks into a JSON object.
- **Pluggable** source via an API endpoint that returns the problem URL.

**Requirements:**
- **Python 3.8+**
- `selenium`, `webdriver_manager`, `requests`, `beautifulsoup4`, `python-dotenv` (see `requirements.txt`)
- Google Chrome installed (ChromeDriver is managed automatically by `webdriver_manager`).

**Quick Start (Windows, cmd.exe)**
1. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the required variables (example below).

4. Run the script:

```
python app.py
```

**Example `.env`**
Place this file at the project root as `.env` (no surrounding quotes):

```
# URL or API that returns a JSON with key `problem_url`
GFG_API=https://your-service.example.com/today

# CSS class or DIV identifier that contains the problem content on the page
# Example: PROBLEM_CONTENT=problem-content
PROBLEM_CONTENT=your-problem-container-class
```

Notes on `.env` values:
- `GFG_API` should return a JSON object with a `problem_url` field, for example `{ "problem_url": "https://www.geeksforgeeks.org/...." }`.
- `PROBLEM_CONTENT` should match the container element on the target site that holds the problem text (inspect the page in Chrome and use the element's class or id).

**How it works**
- `app.py` requests the `GFG_API` to get today's problem URL.
- Selenium (via `webdriver_manager`) opens the page and retrieves the HTML.
- BeautifulSoup finds the element matching `PROBLEM_CONTENT` and extracts paragraphs and example blocks.
- The script prints a JSON object with `title`, `description` (list of paragraphs), and `examples` (list of {input, output, explanation, images}).

**Sample output**
```
Problem url for Today : https://www.geeksforgeeks.org/problems/shortest-path-using-atmost-one-curved-edge--170647/1
{
    "title": "Shortest Path Using Atmost One Curved Edge | Practice | GeeksforGeeks",
    "description": [
        "Given an undirected, connected graph ...",
        "You are given two vertices a and b ..."
    ],
    "examples": [
        {
            "input": "V = 4, E = 4, a = 1, b = 3, ...",
            "output": "2",
            "images": [ "https://...jpg" ],
            "explanation": "We can follow the path 1 -> 0 -> 3"
        }
    ]
}
```

**Troubleshooting & Tips**
- If Selenium fails to open Chrome, ensure Chrome is installed and up-to-date. `webdriver_manager` downloads a matching driver automatically.
- If the script finds no content, verify `PROBLEM_CONTENT` by inspecting the target page and adjusting the selector.
- Increase the `time.sleep(5)` in `app.py` if the page needs more time to load, or replace it with an explicit Selenium wait for better reliability.
- To run Chrome headless, modify `app.py` to configure Chrome options (I can add a headless option if you want).

**Contributing**
Open an issue or send a pull request. If you'd like, I can:
- add a `--headless` option
- add better error handling for network and parsing failures
- include a small test harness
