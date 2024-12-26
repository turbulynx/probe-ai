from typing import List

import os
from dotenv import load_dotenv
from search import Search, SearchResult
from serpapi import GoogleSearch

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")
if not api_key:
    raise ValueError("SERPAPI_KEY is not set in the environment variables.")


class SerpApiSearch(Search):
    def supported_domain(self) -> List[str]:
        return ["google.com"]

    def get_results(self, name: str, tags: list, domains: list = None, max_results: int = 20) -> List[SearchResult]:
        super().get_results(name, tags, domains)
        query = f"""
                {name} {", ".join(tags) if tags else ""}
        """
        params = {
            "q": query,
            "engine": "google",
            "num": max_results,
            "google_domain": "google.com",
            "gl": "sg",
            "hl": "en",
            "safe": "active",
            "api_key": api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        filtered_results = list()
        for result in results.get("organic_results", []):
            url = result.get("link", "")
            filtered_results.append(SearchResult(url=url, content=result.get("snippet", "")))

        return filtered_results
