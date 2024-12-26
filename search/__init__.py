from .base import Search, Summary
from .tavily import TavilySearch
from .serpapi import SerpApiSearch

class SearchFactory:
    @staticmethod
    def get_search_instance(search_type: str) -> Search:
        """Returns an instance of SearchAPIiSeach or TavilySearch based on the search_type."""
        if search_type.lower() == "searchapi":
            return SerpApiSearch()
        elif search_type.lower() == "tavily":
            return TavilySearch()
        else:
            raise ValueError(f"Unknown search type: {search_type}")
