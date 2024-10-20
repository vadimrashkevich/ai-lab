import time
import pandas as pd
from openai import OpenAI
import json
import os
import logging
from typing import Dict

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

def extract_total_area(description):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts total area from property descriptions."},
        {"role": "user", "content": f"""Extract and return only the total area in square meters as a number from the following property description. Do not include any additional text or units. If the area is not specified, return 'unknown'.

Property description: "{description}"

Total area in square meters:"""}
    ]


    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
        )
        message_content = chat_completion.choices[0].message.content
        return message_content

    except Exception as e:
        logging.info(f"An error occurred while connecting to the OpenAI API: {e}")
        return 'unknown'


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