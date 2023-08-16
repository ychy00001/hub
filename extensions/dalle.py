from base64 import b64decode
from Extensions import Extensions
import logging

try:
    import openai
except ImportError:
    import sys
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    import openai


class dalle(Extensions):
    def __init__(
        self,
        OPENAI_API_KEY: str = "",
        WORKING_DIRECTORY: str = "./WORKSPACE",
        **kwargs,
    ):
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.WORKING_DIRECTORY = WORKING_DIRECTORY
        if self.OPENAI_API_KEY:
            self.commands = {
                "Generate Image with DALLE": self.generate_image_with_dalle
            }

    async def generate_image_with_dalle(self, prompt: str, filename: str) -> str:
        openai.api_key = self.OPENAI_API_KEY

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256",
            response_format="b64_json",
        )

        logging.info(f"Image Generated for prompt:{prompt}")

        image_data = b64decode(response["data"][0]["b64_json"])

        with open(f"{self.WORKING_DIRECTORY}/{filename}", mode="wb") as png:
            png.write(image_data)

        return f"Saved to disk:{filename}"
