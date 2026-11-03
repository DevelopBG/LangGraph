from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START,END, add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver # to save information in the RAM
import sqlite3
import requests
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
import requests
import random
import asyncio # this library for asynchronous mode of execution
import os
import sys



load_dotenv()

# -------------

llm = ChatOpenAI(model='gpt-5')

# mcp client for local FastMCP server
client= MultiServerMCPClient(
    {
        "arith":{
            'transport': "stdio",
            "command": sys.executable, # same python as this env ("python3" on Windows is the MS Store stub)
            "args": [os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_sserver.py")]
        },
        "tavily":{
            "transport": "streamable_http",
            "url": "https://mcp.tavily.com/mcp/",
            "headers": {"Authorization":f"Bearer {os.environ['TAVILY_API_KEY']}"}
  }
    }
)



# ---- State -----
class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]


# now the asyn modification starts.----
async def build_graph():

    tools = await client.get_tools()
    print([i.name for i in tools])

    # print(tools)

    llm_with_tools = llm.bind_tools(tools)

    async def chat_node(state: chat_state)-> chat_state:

        messages = state['messages']
        out = await llm_with_tools.ainvoke(messages)
        return {'messages':out}

    tool_node = ToolNode(tools) # this node implementation is internally asynchronous

    # conn = sqlite3.connect(database='./9_8_chatbot_with_mcp/chatbot.db', check_same_thread = False)

    # checkpointer = SqliteSaver(conn = conn)

    graph = StateGraph(chat_state)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge("tools","chat_node")

    # chatbot = graph.compile(checkpointer=checkpointer)
    chatbot = graph.compile()
    return chatbot

async def main():

    chatbot = await build_graph()


    ini_state = {"messages":HumanMessage(content=f"What is today's best news about AI?")}
    response = await chatbot.ainvoke(ini_state)

    print(response['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())