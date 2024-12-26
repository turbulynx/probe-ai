from typing import List
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    url: str = Field(description="URL")
    content: str = Field(description="Content description")

    def to_dict(self):
        return {"url": self.url, "content": self.content}

class Search:
    def __init__(self):
        self.sources = None

    def supported_domain(self) -> list:
        pass

    def get_results(self, name: str, tags: list, sources: list = None, max_results:int=20) -> List[SearchResult]:
        if not all(source in self.supported_domain() for source in sources):
            raise ValueError("All Domains not supported")
        self.sources = sources or self.supported_domain()
        pass