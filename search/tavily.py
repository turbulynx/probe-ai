from typing import List
from langchain_community.tools import TavilySearchResults
from search import Search,SearchResult


class TavilySearch(Search):
    def supported_domain(self) -> list:
        return ["linkedin.com", "facebook.com"]

    def get_results(self, name: str, tags: list, domains: list = None, max_results: int=20) -> List[SearchResult]:
        super().get_results(name, tags, domains)
        """Search for a person and return URLs from specific domains with additional tags."""
        tags_str = ", ".join(tags) if tags else "No specific tags"
        query = f"""
                Find the exact URLs for {name}, search result should  have exact name of person and one or more the following tags: {tags_str}. 
                Exclude generic URLs like login pages or home pages, and focus on meaningful links.
            """
        search = TavilySearchResults(max_results=max_results, include_domains=domains)
        res = search.run(query)
        return res

