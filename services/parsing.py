"""LLM response parsing utilities."""

import json
import re


def parse_json_response(text: str) -> dict:
    text = text.strip()

    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    return json.loads(text)
