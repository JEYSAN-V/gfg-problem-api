import re
import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv

load_dotenv()
PROBLEM_CONTENT = os.getenv("PROBLEM_CONTENT")
GFG_API = os.getenv("GFG_API")

res = requests.get(GFG_API).json()

problem_url = res['problem_url']
print(f'Problem url for Today : {problem_url}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(problem_url)
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title').text
print(f'Title : {title}')

target = soup.find('div', class_=PROBLEM_CONTENT)

final_json = {
    "title": title,
    "description": [],
    "examples": []
}

paragraphs = target.find_all('p')
for para in paragraphs:
    final_json["description"].append(para.text.strip())
    
    
if final_json["description"]:
    last = final_json["description"][-1].strip().lower()
    if "example" in last:
        final_json["description"].pop()


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

    images = [img["src"] for img in example.find_all('img')]

    final_json["examples"].append({
        "input": input_part,
        "output": output_part,
        "images": images,
        "explanation": explanation_part
    })

print(json.dumps(final_json, indent=4))
driver.quit()