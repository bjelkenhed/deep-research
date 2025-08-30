from langchain_core.tools import tool
from typing import Literal, List
from typing import Annotated
from langchain_core.tools import InjectedToolCallId
from pydantic import BaseModel, Field

from tavily import TavilyClient
from deep_research.prompts import WRITE_TODOS_DESCRIPTION
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class Todo(BaseModel):
    """Todo to track."""

    content: str = Field(description="The content/description of the todo item")
    status: Literal["pending", "in_progress", "completed"] = Field(
        description="Status of the todo item", default="pending"
    )


@tool
def internet_search(
    query: str,
    max_results: int = 5,
):
    """Run a web search"""
    search_docs = tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=False,
        topic="general",
    )
    return search_docs


@tool(description=WRITE_TODOS_DESCRIPTION)
def write_todos(todos: List[Todo]) -> str:
    print("-------------- Writing todos --------------")
    for todo in todos:
        print(f"- [{todo.status}] {todo.content}")
    return f"Updated todo list with {len(todos)} items"
