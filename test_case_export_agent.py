from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor

#tool to be used by AI

@tool
def save_to_file(content: str) -> str:
    """Save the given content to a text file on disk.
    Returns a confirmation message after saving."""
    with open("sample_output/output.txt", "w", encoding="utf-8") as file:
        file.write(content)
    return "File saved successfully"


# ReAct agent - Reason(think) + Act
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
TOOLS = [save_to_file]  # list of tools which AI can use

from langchain.prompts import ChatPromptTemplate

# Diff between ChatPromptTemplate and PromptTemplate?

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a QA assistant.

You MUST use the following format:

Thought: describe what you will do
Action: the tool name from [{tool_names}]
Action Input: the content to pass to the tool
Observation: the result of the tool
Final Answer: a short confirmation to the user

Available tools:
{tools}
"""
    ),
    ("human", "{input}"),
    ("assistant", "{agent_scratchpad}")
])


agent = create_react_agent(llm, TOOLS, prompt)
agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)
agent_executor.invoke({
    "input": "Write test cases for login functionality and save them"
})





