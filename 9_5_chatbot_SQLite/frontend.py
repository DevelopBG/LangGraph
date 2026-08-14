import streamlit as st
from langraph_database_backend import chatbot,retrieve_all_threads
from langchain_core.messages import BaseMessage,HumanMessage
import uuid # to generate random random id



 
#-----------------utility functions-------------

def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thred(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thred(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )
    return state.values.get("messages", [])
#----------------------------------------



# ---------------session setup---------
if 'message_history' not in st.session_state:
    st.session_state['message_history']= []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
add_thred(st.session_state['thread_id'])


#--------------- sidebar UI --------------------------
st.sidebar.title("LangGraph chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()
st.sidebar.header("My conversation")

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        # to change the retrieved messages format to our defined messages
        temp_message = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_message.append({'role':role,"content":msg.content})
        st.session_state['message_history'] = temp_message

#-----------------------------------------------------

for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.text(message['content'])


userinput  = st.chat_input("Type Here")

if userinput:

    st.session_state['message_history'].append({'role':'user','content':userinput})
    with st.chat_message('user'):
        st.text(userinput)

    config = {'configurable':{'thread_id': st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content= userinput)]},
                config= config,
                stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    

