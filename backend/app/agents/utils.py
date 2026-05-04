import re
import json
import os
from langchain_openai import ChatOpenAI


def get_llm(temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o"),
        temperature=temperature,
        base_url=os.getenv("OPENAI_BASE_URL") or None,
    )


def parse_json_response(text: str, model_cls):
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {text[:200]}")
    return model_cls(**json.loads(match.group()))
