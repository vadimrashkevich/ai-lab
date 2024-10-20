import time
import pandas as pd
import requests
import json
import re
import os
import logging
from typing import Dict

API_URL = os.getenv('API_URL', 'http://127.0.0.1:1234/v1/completions')
EXCEL_FILE_PATH = 'AI Lab 1 - Data - Topic 1- Information Extraction 2.xlsx'
RESULTS_FILE_PATH = 'results2.json'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_excel(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        logging.error(f"Failed to load Excel file: {e}")
        raise

def save_results(results: Dict, file_path: str) -> None:
    try:
        with open(file_path, 'w') as f:
            json.dump(results, f)
        logging.info(f"Results saved to '{file_path}'.")
    except Exception as e:
        logging.error(f"Failed to save results: {e}")
        raise

def extract_total_area(description: str) -> str:
    prompt = f"""From the following property description, extract and return only the total area in square meters as a number. Do not include any additional text, units, or calculations. If the area is not specified, return 'unknown'.

Property description: "{description}"

Total area in square meters as a number:"""

    payload = {
        "prompt": prompt,
        # "max_tokens": 100,
        "stop": ["\n"]
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while connecting to the API: {e}")
        return 'unknown'

    response_data = response.json()
    print(response_data)
    response_text = response_data['choices'][0].get('text', '').strip()
    match = re.search(r'(\d+(\.\d+)?)', response_text)
    return match.group(1) if match else 'unknown'

def main():
    df = load_excel(EXCEL_FILE_PATH)
    results = {}

    for idx, row in df.iterrows():
        property_id = row['property_id']
        description = row['property_description']
        total_area = extract_total_area(description)
        results[property_id] = total_area

    save_results(results, RESULTS_FILE_PATH)
    logging.info("Extraction complete.")

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds.")
