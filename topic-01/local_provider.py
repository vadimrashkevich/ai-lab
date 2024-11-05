import time
import pandas as pd
import requests
import json
import re
import os
import logging
from typing import Dict
from llm_provider import LLMProvider

API_URL = os.getenv('API_URL', 'http://127.0.0.1:1234/v1/completions')
EXCEL_FILE_PATH = 'AI Lab 1 - Data - Topic 1- Information Extraction 2.xlsx'
RESULTS_FILE_PATH = 'results2.json'

class LocalModelProvider(LLMProvider):
    def extract_total_area(self, description: str) -> str:
        """
        Extract the total area from the property description using a local model.

        :param description: Property description.
        :return: Total area in square meters as a string.
        """
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
        response_text = response_data['choices'][0].get('text', '').strip()
        match = re.search(r'(\d+(\.\d+)?)', response_text)
        return match.group(1) if match else 'unknown'
