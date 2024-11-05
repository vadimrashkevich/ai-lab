import time
import logging
from gpt_provider import GPTAPIProvider
from llm_provider import LLMProvider

EXCEL_FILE_PATH = 'AI Lab 1 - Data - Topic 1- Information Extraction 2.xlsx'
RESULTS_FILE_PATH = 'results3.json'
PROMPT_FILE_PATH = 'prompt.txt'
CORRECT_ANSWERS_FILE_PATH = 'correct_answers.json'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(provider: LLMProvider):
    """
    Main function to run the extraction process.

    :param provider: Instance of LLMProvider.
    """
    df = provider.load_excel()
    results = {}

    for idx, row in df.iterrows():
        property_id = row['property_id']
        description = row['property_description']
        total_area = provider.extract_total_area(description)
        results[property_id] = total_area

    provider.save_results(results)
    logging.info("Extraction complete.")

    # comparison = provider.compare_results(results)
    # logging.info(f"Comparison results: {comparison}")

if __name__ == "__main__":
    start_time = time.time()

    provider = GPTAPIProvider(EXCEL_FILE_PATH, RESULTS_FILE_PATH, PROMPT_FILE_PATH, CORRECT_ANSWERS_FILE_PATH)  # or GPTAPIProvider(), BedrockProvider()

    main(provider)
    execution_time = time.time() - start_time
    logging.info(f"Execution time: {execution_time:.2f} seconds.")
