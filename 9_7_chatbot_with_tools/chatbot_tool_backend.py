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

import requests
import random


load_dotenv()

# -------------
llm = ChatOpenAI()

#-------------- # tools ------------------

search_tool = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(region="us-en"))


# custom tools: need decorator @tool to start the definition of the tool
# for custom tool always use - doc string, LLM read it and understands what to use
@tool
def calculator(first_number:float, second_number: float, operation: str) -> dict:
    """
    Perform a basic arithmatic operation on two numbers. 
    Supported operations : add, sub, mul and div
    """

    try:
        if operation== "add":
            result = first_number+second_number
        elif operation == "sub":
            result = first_number - second_number
        elif operation == 'mul':
            result = first_number * second_number
        elif operation == "div":
            if second_number ==0:
                return {'error':"Division by zero is not supported"}
            else:
                result = first_number/second_number
        else:
            return {"error":f"Unsupported operation {operation}"}

        return {"first number": first_number, "second number": second_number, "operation": operation, "result": result}
                 
    except Exception as e:
        return {'error': e}

@tool
def get_stok_price(symbol:str)-> dict:
    """
    doc string : Fetch latest stock price for a given symbol (e.g. "AAP", "TSLA")
    using Alpha Vantage with API key in the URL
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=00TZNO30DHKMK3PJ"
    r = requests.get(url)

    return r.json()


tools = [search_tool, calculator, get_stok_price]
llm_with_tools = llm.bind_tools(tools)

# ---- State -----
class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chat_node(state: chat_state)-> chat_state:

    messages = state['messages']
    out = llm_with_tools.invoke(messages)
    return {'messages':out}

tool_node = ToolNode(tools)

conn = sqlite3.connect(database='./9_7_chatbot_with_tools/chatbot.db', check_same_thread = False)

checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(chat_state)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")

chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

