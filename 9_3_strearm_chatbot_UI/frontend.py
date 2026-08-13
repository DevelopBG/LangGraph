import streamlit as st
from backend import chatbot
from langchain_core.messages import BaseMessage,HumanMessage



 
# with st.chat_message("user"):
#     st.text("Hi")

# with st.chat_message("assistant"):
#     st.text("What can I help you with?")

config = {'configurable':{'thread_id':'1'}}

# loading the coversation history-----
if 'message_history' not in st.session_state:
    st.session_state['message_history']= []

for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.text(message['content'])


userinput  = st.chat_input("Type Here")

if userinput:

    st.session_state['message_history'].append({'role':'user','content':userinput})
    with st.chat_message('user'):
        st.text(userinput)



    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content= userinput)]},
                config= {'configurable':{"thread_id":'1'}},
                stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    

