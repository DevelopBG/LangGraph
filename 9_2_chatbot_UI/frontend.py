import streamlit as st
from backend import chatbot
from langchain_core.messages import BaseMessage,HumanMessage



 
# with st.chat_message("user"):
#     st.text("Hi")

# with st.chat_message("assistant"):
#     st.text("What can I help you with?")

config = {'configurable':{'thread_id':'1'}}
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


    
    initial_messages ={'messages': [HumanMessage(content=userinput)]}
    response = chatbot.invoke(initial_messages,config=config)
    response = response['messages'][-1].content
    st.session_state['message_history'].append({'role':'assistant','content':response})
    with st.chat_message("assistant"):
        st.text(response)

