# GeeksforGeeks Problem API

This Flask application provides an API to fetch problem details from GeeksforGeeks, including the Problem of the Day (POTD). It extracts structured problem data directly from GeeksforGeeks’ embedded __NEXT_DATA__ JSON, making it fast and reliable without full browser automation.

## Features

*   Fetch problem title, HTML description, difficulty, problem URL, and article URL from any GeeksforGeeks Problem.
*   Fetch the GeeksforGeeks Problem of the Day (POTD).
*   Returns clean, structured JSON responses(title, html_description, difficulty, problem_url, article_url).


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
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root directory of the project and add the following environment variables:

    ```
    GFG_API="https://practiceapi.geeksforgeeks.org/api/v1/problems-of-day/problem/today/" # The API endpoint for GeeksforGeeks Problem of the Day
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will run on `http://127.0.0.1:5000/` by default.

## API Endpoints

### 1. Scrape a specific problem

*   **URL:** `/api/v1/problem/<problem_url>`
*   **Method:** `GET`
    ```
    GET http://127.0.0.1:5000/api/v1/problem/https://www.geeksforgeeks.org/problems/minimize-connections/1
    ```
### 2. Fetch Problem of the Day (POTD)

*   **URL:** `/api/v1/problem/potd`