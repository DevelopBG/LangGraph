from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START,END, add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver # to save information in the RAM
import sqlite3




load_dotenv()

llm  = ChatOpenAI()

class ChatState(TypedDict):

    messages : Annotated[list[BaseMessage], add_messages]  # it contains any types of messages



def chat_node(state: ChatState):

    message = state['messages']

    response = llm.invoke(message)

    return {'messages': [response]}


conn = sqlite3.connect(database='./9_5_chatbot_SQLite/chatbot.db', check_same_thread = False)

checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

graph.add_node("chat node", chat_node)

graph.add_edge(START, "chat node")
graph.add_edge("chat node", END)

chatbot = graph.compile(checkpointer=checkpointer)


# it gives a list of checkpoints
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
# print(list(all_threads))
# this is the streamming generator to print token by token
# response =  chatbot.invoke(
#     {'messages': [HumanMessage(content= "Who am I?")]},
#     config= {'configurable':{"thread_id":'1'}}
#     )


# print(response)