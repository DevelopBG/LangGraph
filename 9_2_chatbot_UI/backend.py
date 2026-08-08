from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START,END, add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver # to save information in the RAM




load_dotenv()

llm  =ChatOpenAI()

class ChatState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]  # it contains any types of messages



def chat_node(state: ChatState):

    message = state['messages']

    response = llm.invoke(message)

    return {'messages': [response]}


checkpointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node("chat node", chat_node)

graph.add_edge(START, "chat node")
graph.add_edge("chat node", END)

chatbot = graph.compile(checkpointer=checkpointer)
