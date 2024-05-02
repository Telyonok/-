import asyncio

import httpx
import requests

from settings import settings


class J2ChatAI:
    def __init__(self):
        self.chat_url = "https://api.ai21.com/studio/v1/j2-ultra/chat"
        self.api_key = settings.chat_api_key

    def make_request_to_chat(self, messages: list[dict[str, str]], model_description: str):
        payload = {
            "numResults": 1,
            "temperature": 0.7,
            "messages": messages,
            "system": model_description
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        with httpx.Client() as client:
            result = client.post(self.chat_url, headers=headers, json=payload, timeout=20)
            return result.json()