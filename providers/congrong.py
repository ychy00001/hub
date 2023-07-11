import requests
import json
from log import logger


class CongrongProvider:
    def __init__(
            self,
            AI_PROVIDER_URI: str = "",
            AI_MODEL: str = "从容",
            MAX_TOKENS: int = 1024,
            AI_TEMPERATURE: float = 0.7,
            AI_TOP_K: float = 50,
            AI_TOP_P: float = 1,
            AI_DO_SAMPLE: bool = False,
            AI_REPETITION_PENALTY: float = 1.0,
            AI_TRUNCATE: int = 2000,
            **kwargs,
    ):
        self.requirements = []
        self.AI_PROVIDER_URI = AI_PROVIDER_URI
        self.AI_MODEL = AI_MODEL
        self.MAX_TOKENS = MAX_TOKENS
        self.AI_TEMPERATURE = AI_TEMPERATURE
        self.AI_TOP_K = AI_TOP_K
        self.AI_TOP_P = AI_TOP_P
        self.AI_DO_SAMPLE = AI_DO_SAMPLE
        self.AI_REPETITION_PENALTY = AI_REPETITION_PENALTY
        self.AI_TRUNCATE = AI_TRUNCATE

    def instruct(self, prompt, tokens: int = 0):
        print(f"congrong instruct")
        params = {
            "inputs": prompt,
            "parameters": {
                "temperature": float(self.AI_TEMPERATURE),
                "max_new_tokens": int(self.MAX_TOKENS),
                "top_k": int(self.AI_TOP_K),
                "top_p": float(self.AI_TOP_P),
                "do_sample": bool(self.AI_DO_SAMPLE),
                "repetition_penalty": float(self.AI_REPETITION_PENALTY),
                "truncate": int(self.AI_TRUNCATE),
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print(f"params:{json.dumps(params, ensure_ascii=False)}")
        response = requests.post(
            self.AI_PROVIDER_URI,
            json=params,
            timeout=600,
            headers=headers
        )
        # logger.info(f"response:{response.text}")
        result = response.json()["generated_text"]
        return result
