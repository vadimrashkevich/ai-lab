from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMProvider(ABC):
    def __init__(self, excel_file_path: str, results_file_path: str, prompt_file_path: str, correct_answers_file_path: str):
        """
        Initialize the LLMProvider with file paths.

        :param excel_file_path: Path to the Excel file.
        :param results_file_path: Path to the results file.
        :param prompt_file_path: Path to the prompt file.
        :param correct_answers_file_path: Path to the correct answers file.
        """
        self.excel_file_path = excel_file_path
        self.results_file_path = results_file_path
        self.prompt_file_path = prompt_file_path
        self.correct_answers_file_path = correct_answers_file_path

    @abstractmethod
    def extract_total_area(self, description: str) -> str:
        """
        Extract the total area from the property description.

        :param description: Property description.
        :return: Total area in square meters as a string.
        """
        pass

    def load_excel(self) -> pd.DataFrame:
        """
        Load data from an Excel file.

        :return: DataFrame containing the data.
        """
        try:
            return pd.read_excel(self.excel_file_path)
        except Exception as e:
            logging.error(f"Failed to load Excel file: {e}")
            raise

    def save_results(self, results: Dict) -> None:
        """
        Save the results to a JSON file.

        :param results: Dictionary containing the results.
        """
        try:
            with open(self.results_file_path, 'w') as f:
                json.dump(results, f)
            logging.info(f"Results saved to '{self.results_file_path}'.")
        except Exception as e:
            logging.error(f"Failed to save results: {e}")
            raise

    def load_prompt(self) -> str:
        """
        Load the prompt from a file.

        :return: Prompt as a string.
        """
        try:
            with open(self.prompt_file_path, 'r') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Failed to load prompt file: {e}")
            raise

    def compare_results(self, results: Dict) -> Dict:
        """
        Compare the results with the correct answers from a local file.

        :param results: Dictionary containing the results.
        :return: Dictionary containing the comparison results.
        """
        try:
            with open(self.correct_answers_file_path, 'r') as f:
                correct_answers = json.load(f)
            comparison = {key: (results[key] == correct_answers[key]) for key in results}
            return comparison
        except Exception as e:
            logging.error(f"Failed to compare results: {e}")
            raise
