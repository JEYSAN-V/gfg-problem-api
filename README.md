# GeeksforGeeks Problem API

This Flask application provides an API to scrape problem details from GeeksforGeeks, including the Problem of the Day (POTD). It leverages Playwright to handle JavaScript-rendered pages and BeautifulSoup for parsing HTML content.

## Features

*   Scrape problem title, description, examples, and associated images from any GeeksforGeeks problem URL.
*   Fetch the Problem of the Day (POTD) details automatically.
*   Returns data in a structured JSON format.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jeysan-v/gfg-problem-api
    cd gfg-problem-api
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    ./venv/Scripts/activate # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root directory of the project and add the following environment variables:

    ```
    PROBLEM_CONTENT="problem-content-class-name" # The HTML class name of the div containing problem content on GeeksforGeeks
    GFG_API="https://practiceapi.geeksforgeeks.org/api/v1/problems-of-day/problem/today/" # The API endpoint for GeeksforGeeks Problem of the Day
    ```
    You will need to inspect the GeeksforGeeks website to find the correct `PROBLEM_CONTENT` class name.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will run on `http://127.0.0.1:5000/` by default.

## API Endpoints

### 1. Scrape a specific problem

*   **URL:** `/api/v1/geeksforgeeks/problem/<problem_url>`
*   **Method:** `GET`
    ```
    GET http://127.0.0.1:5000/api/v1/geeksforgeeks/problem/https://www.geeksforgeeks.org/problems/minimize-connections/1
    ```
### 2. Fetch Problem of the Day (POTD)

*   **URL:** `/api/v1/geeksforgeeks/problem/potd`