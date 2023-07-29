from typing import Callable, List

from langchain.agents import Agent, OpenAIFunctionsAgent, AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage

# TODO if more than one chat is available, alter this
MEMORY_KEY = "chat_history"

def create_agent(tools: List[Callable], system_message: str, temperature: int = 0) -> Agent:
    # TODO: factory design pattern for these
    # TODO: what if we want a different type of agent
    system_message = SystemMessage(content=system_message)
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]

        )
    llm = ChatOpenAI(temperature=temperature)

    return OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)


def create_agent_runtime(tools: List[Callable], system_message: str, temperature: int = 0, verbose: bool = False) -> AgentExecutor: 
    agent = create_agent(tools, system_message, temperature=temperature)
    memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)
    return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=verbose)

