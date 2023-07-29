import pytest
from typing import List, Callable

from langchain.tools import tool
from langchain.agents import Agent

from src.geo_ai.llm.agent import create_agent, create_agent_runtime

@tool
def get_word_length(word: str) -> int:
    """Returns the length of the given word."""
    return len(word)


@pytest.fixture
def fake_tools() -> List[Callable]:
    yield [get_word_length]

@pytest.fixture
def fake_system_message() -> str:
    yield "You are a very intelligent assistant, but bad at computing the length of words."

@pytest.fixture
def agent() -> Agent:
    yield create_agent(tools=fake_tools, system_message=fake_system_message)

def create_agent_test(fake_tools: List[Callable], fake_system_message: str):
    agent = create_agent(tools=fake_tools, system_message=fake_system_message)
    assert False


def create_agent_runtime_test(fake_tools: List[Callable], fake_system_message: str):
    runtime = create_agent_runtime(tools=fake_tools, system_message=fake_system_message)
    message = runtime.run("how many letters are in the word octopus?")

