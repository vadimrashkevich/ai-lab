import boto3
import json
import logging
from llm_provider import LLMProvider

class BedrockProvider(LLMProvider):
    def extract_total_area(self, description: str) -> str:
        """
        Extract the total area from the property description using the Bedrock API.

        :param description: Property description.
        :return: Total area in square meters as a string.
        """
        prompt = self.load_prompt().format(description=description)
        session = boto3.session.Session()
        bedrock = session.client(service_name='bedrock-runtime', region_name='eu-west-2')

        try:
            model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'

            payload = {
                "prompt": prompt,
                "max_tokens_to_sample": 10,
                "temperature": 0,
                "stop_sequences": ["\n"]
            }

            response = bedrock.invoke_model(
                modelId=model_id,
                accept='application/json',
                contentType='application/json',
                body=json.dumps(payload)
            )

            response_body = response['body'].read()
            response_data = json.loads(response_body)

            generated_text = response_data.get('results')[0].get('outputText', '').strip()

            if generated_text.lower() == 'unknown':
                return 'unknown'
            else:
                try:
                    total_area_float = float(generated_text)
                    return str(total_area_float)
                except ValueError:
                    return 'unknown'

        except Exception as e:
            logging.info(f"An error occurred while connecting to the OpenAI API: {e}")
            return 'unknown'