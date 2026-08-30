Observability in LangGraph. 

Here we will add LangSmith for oservability purpose. It enables us to observe not only the output but also the intermediate states and internal feature tracking. Such as token usage, latency, different tools performance, etc. It is a very important aspect of any pipeline. 

Main setup is to be done in the .env file, as given below. 
    ```
    LANGSMITH_API_KEY = "**"
    LANGSMITH_TRACING = 'true'
    LANGSMITH_ENGPOINT = 'https://api.smith.langchain.com'
    LANGSMITH_PROJECT = 'chatbot-project'
    ```

And also modify config variable according to your need. 