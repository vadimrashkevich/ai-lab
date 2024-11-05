import os
import logging
from openai import OpenAI
from llm_provider import LLMProvider

class GPTAPIProvider(LLMProvider):
    def extract_total_area(self, description: str) -> str:
        """
        Extract the total area from the property description using the GPT API.

        :param description: Property description.
        :return: Total area in square meters as a string.
        """
        prompt = self.load_prompt().format(description=description)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts total area from property descriptions."},
            {"role": "user", "content": prompt}
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
