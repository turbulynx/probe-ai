from typing import List
from search import Search, Summary
from serpapi import GoogleSearch


class SerpApiSearch(Search):
    def supported_domain(self) -> List[str]:
        return ["google.com"]

    def get_results(self, name: str, tags: list, domains: list = None, max_results: int = 20) -> List[Summary]:
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
            "api_key": "1d5e501242c00bcf6c37586823fec333cc5ab6cb0283875528ae400c1603166a"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        filtered_results = list()
        for result in results.get("organic_results", []):
            url = result.get("link", "")
            filtered_results.append(Summary(url=url, content=result.get("snippet", "")))

        return filtered_results
