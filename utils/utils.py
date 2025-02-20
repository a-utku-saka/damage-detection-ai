import json
import yaml
from pathlib import Path


def _get_prompt(prompt_name):
    try:
        with open(Path(__file__).parent / "../constants/prompts.yaml", "r", encoding='utf8') as file:
            data = yaml.safe_load(file)
            for prompt in data["prompts"]:
                if prompt["prompt_name"] == prompt_name:
                    return prompt["prompt"]
    except (FileNotFoundError, yaml.YAMLError):
        return "Error loading prompt!"
    return "Prompt not found!"


def _load_config(api_name):
    try:
        with open(Path(__file__).parent / "../constants/gpt_config.json", "r") as file:
            config = json.load(file)
        return config.get(api_name, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    

def _get_response_format(response_type):
    try:
        with open(Path(__file__).parent / "../constants/response_formats.yaml", "r", encoding='utf8') as file:
            formats = yaml.safe_load(file)["response_formats"]
            for format in formats:
                if format["type"] == response_type:
                    return str(yaml.safe_load(format["format"]))
    except (FileNotFoundError, yaml.YAMLError):
        return "Error loading eesponse format!"
    return "Response format not found!" 