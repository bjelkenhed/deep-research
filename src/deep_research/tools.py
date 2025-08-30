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


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"
