from typing import Union, List
import json
from Extensions import Extensions

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    import sys
    import subprocess

    subprocess.check_call([sys.exewcutable, "-m", "pip", "install", "google-api-python-client==2.87.0"])
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

class google(Extensions):
    def __init__(self, GOOGLE_API_KEY: str = "", GOOGLE_SEARCH_ENGINE_ID: str = "", **kwargs):
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.GOOGLE_SEARCH_ENGINE_ID = GOOGLE_SEARCH_ENGINE_ID
        if self.GOOGLE_API_KEY:
            self.commands = {
                "Google Customer Search": self.google_costumer_search,
                "Google Search": self.google_official_search,
            }

    async def google_official_search(
            self, query: str, num_results: int = 8
    ) -> Union[str, List[str]]:

        try:
            # Get the Google API key and Custom Search Engine ID from the config file
            api_key = self.GOOGLE_API_KEY
            custom_search_engine_id = self.GOOGLE_SEARCH_ENGINE_ID

            # Initialize the Custom Search API service
            service = build("customsearch", "v1", developerKey=api_key)

            # Send the search query and retrieve the results
            result = (
                service.cse()
                    .list(q=query, cx=custom_search_engine_id, num=num_results)
                    .execute()
            )

            # Extract the search result items from the response
            search_results = result.get("items", [])

            # Create a list of only the URLs from the search results
            search_results_links = [item["link"] for item in search_results]

        except HttpError as e:
            # Handle errors in the API call
            error_details = json.loads(e.content.decode())

            # Check if the error is related to an invalid or missing API key
            if error_details.get("error", {}).get(
                    "code"
            ) == 403 and "invalid API key" in error_details.get("error", {}).get(
                "message", ""
            ):
                return "Error: The provided Google API key is invalid or missing."
            else:
                return f"Error: {e}"

        # Return the list of search result URLs
        return search_results_links

    async def google_costumer_search(
            self, query: str, num_results: int = 8
    ) -> Union[str, List[str]]:

        try:
            # Get the Google API key and Custom Search Engine ID from the config file
            api_key = self.GOOGLE_API_KEY
            custom_search_engine_id = self.GOOGLE_SEARCH_ENGINE_ID

            # Initialize the Custom Search API service
            service = build("customsearch", "v1", developerKey=api_key)

            # Send the search query and retrieve the results
            result = (
                service.cse()
                    .list(q=query, cx=custom_search_engine_id, num=num_results)
                    .execute()
            )

            # Extract the search result items from the response
            search_results = result.get("items", [])

            # Create a list of only the URLs from the search results
            search_results_links = [
                result["title"] + " - " + result["link"] for result in search_results
            ]
        except HttpError as e:
            # Handle errors in the API call
            error_details = json.loads(e.content.decode())

            # Check if the error is related to an invalid or missing API key
            if error_details.get("error", {}).get(
                    "code"
            ) == 403 and "invalid API key" in error_details.get("error", {}).get(
                "message", ""
            ):
                return "Error: The provided Google API key is invalid or missing."
            else:
                return f"Error: {e}"

        # Return the list of search result URLs
        return search_results_links
