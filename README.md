# GeeksforGeeks Problem Scraper API

This Flask application provides an API to scrape problem details from GeeksforGeeks, including the Problem of the Day (POTD). It leverages Playwright to handle JavaScript-rendered pages and BeautifulSoup for parsing HTML content.

## Features

*   Scrape problem title, description, examples, and associated images from any GeeksforGeeks problem URL.
*   Fetch the Problem of the Day (POTD) details automatically.
*   Returns data in a structured JSON format.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd web_scrapping
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
    GFG_API="https://practiceapi.geeksforgeeks.org/api/v1/problems/problem-of-the-day/details/" # The API endpoint for GeeksforGeeks Problem of the Day
    ```
    You will need to inspect the GeeksforGeeks website to find the correct `PROBLEM_CONTENT` class name.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will run on `http://127.0.0.1:5000/` by default.

## API Endpoints

### 1. Scrape a specific problem

*   **URL:** `/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/<problem_url>`
*   **Method:** `GET`
*   **Parameters:**
    *   `<problem_url>`: The full URL of the GeeksforGeeks problem you want to scrape.
*   **Example Request:**
    ```
    GET http://127.0.0.1:5000/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/https://www.geeksforgeeks.org/problems/minimize-connections/1
    ```
*   **Example Response:**
    ```json
    {
        "title": "Minimum Operations to Connect Hospitals | Practice | GeeksforGeeks ",
        "description": [
            "You are given an undirected network of V hospitals numbered from 0 to V - 1, represented as a 2D array edges[][], where each element edges[i] = [u, v] denotes a direct connection between hospital u and hospital v.In one operation, you are allowed to remove any existing link and reconnect it between two hospitals that are currently not directly or indirectly connected.",
            "Your task is to determine the minimum number of operations required to make sure that all hospitals become connected, either directly or indirectly, using the given links.",
            "Note: If it is impossible to connect all hospitals into a single network, return -1."
        ],
        "examples": [
            {
                "input": "V = 4, E = 3, edges[][] = [[0, 1], [0, 2], [1, 2]]",
                "output": "1",
                "images": [
                    "https://media.geeksforgeeks.org/img-practice/prod/addEditProblem/710261/Web/Other/blobid0_1763728384.png"
                ],
                "explanation": "Remove the connection between hospitals 1 and 2 and connect the hospitals 1 and 3."
            },
            {
                "input": "V = 5, E = 4, edges[][] = [[0, 1], [0, 2], [2, 3], [3, 4]]",
                "output": "0",
                "images": [
                    "https://media.geeksforgeeks.org/img-practice/prod/addEditProblem/710261/Web/Other/blobid1_1763728438.png"
                ],
                "explanation": "All hospitals are already connected directly or indirectly. No rearrangement of connections is required."
            }
        ],
        "problem_url": "https://www.geeksforgeeks.org/problems/minimize-connections/1"
    }
    ```

### 2. Fetch Problem of the Day (POTD)

*   **URL:** `/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/potd`
*   **Method:** `GET`
*   **Example Request:**
    ```
    GET http://127.0.0.1:5000/fetchdailyproblemapi.project/api/v1/geeksforgeeks/fetchproblem/potd
    ```
*   **Example Response:**
    (Same format as the specific problem scrape endpoint, but for the current POTD)

## Dependencies

The project uses the following libraries:

*   Flask
*   BeautifulSoup4
*   Playwright
*   python-dotenv
*   requests

These dependencies are listed in `requirements.txt`.
