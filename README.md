# AI LangGraph Workflows

A hands-on collection of [LangGraph](https://langchain-ai.github.io/langgraph/) examples that build up, notebook by notebook, from a plain non-LLM state machine to a persistent, tool-aware chatbot with a Streamlit UI. Each notebook is self-contained, pairs a diagram with runnable code, and focuses on one core LangGraph concept — sequential graphs, parallel fan-out/fan-in, conditional routing, iterative loops, and persistence/memory.

## What's inside

| # | Notebook | Concept | Description |
|---|----------|---------|-------------|
| 1 | [1_bmi_workflow.ipynb](1_bmi_workflow.ipynb) | Sequential | BMI calculator with no LLM involved — a minimal intro to defining state, nodes, and edges in LangGraph. |
| 2 | [2_llm_workflow.ipynb](2_llm_workflow.ipynb) | Sequential + LLM | Simplest possible LLM call wired into a graph. |
| 3 | [3._prompt_chain_workflow.ipynb](3._prompt_chain_workflow.ipynb) | Sequential chain | Chains multiple prompts together, passing output from one step as input to the next. |
| 4 | [4_parallel_workflow.ipynb](4_parallel_workflow.ipynb) | Parallel | Cricket-stats example (strike rate, boundary %, balls per boundary) computed concurrently; demonstrates why concurrent state updates require **partial state** returns instead of rewriting the whole state. |
| 5 | [5_essay_eval_workflow.ipynb](5_essay_eval_workflow.ipynb) | Parallel + structured output | Evaluates an essay on language, analysis, and clarity of thought in parallel using Pydantic structured output, then reduces the individual scores into a final average via a custom **reducer function**. |
| 6 | [6_conditional_workflow.ipynb](6_conditional_workflow.ipynb) | Conditional | Solves a quadratic equation, branching the graph based on the discriminant. |
| 7 | [7_conditional_llm_chat.ipynb](7_conditional_llm_chat.ipynb) | Conditional + LLM | Classifies customer review sentiment, then routes to a different response-generation node depending on the sentiment. |
| 8 | [8_iterative_workflow.ipynb](8_iterative_workflow.ipynb) | Iterative | Auto-generates a social media post, evaluates its quality, and loops back to improve it until the evaluation passes. |
| 9 | [9_0_chatbot_.ipynb](9_0_chatbot_.ipynb) | Chatbot | Builds a conversational chatbot from scratch, introducing LangChain message types (`HumanMessage`, `AIMessage`, `SystemMessage`, `ToolMessage`) and short-term memory via accumulated message state. |
| 9.1 | [9_1_persistence.ipynb](9_1_persistence.ipynb) | Persistence | Adds a checkpointer for cross-session memory, human-in-the-loop, fault tolerance, and **time travel** — replaying or editing state at any prior checkpoint and re-running the graph from there. |
| 9.2 | [9_2_chatbot_UI/](9_2_chatbot_UI/) | UI | A [Streamlit](https://streamlit.io/) front end (`frontend.py`) wired to a persisted LangGraph chatbot (`backend.py`), giving the chatbot a real chat interface backed by `MemorySaver`. |

The planned scope for the chatbot track (see `9_0_chatbot_.ipynb`) also covers RAG, tool calling, and LangSmith logging, which later notebooks in this series will build on.

## Tech stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph orchestration for stateful LLM workflows
- [LangChain](https://github.com/langchain-ai/langchain) / `langchain-openai` — LLM integration
- OpenAI models (e.g. `gpt-4o-mini`) via `ChatOpenAI`
- [Pydantic](https://docs.pydantic.dev/) — structured output schemas
- [Streamlit](https://streamlit.io/) — chatbot UI
- `python-dotenv` — environment variable loading

## Getting started

### Prerequisites
- Python 3.12+
- An OpenAI API key

### Setup

```bash
git clone <this-repo>
cd AI-langgraph-workflows
pip install langgraph langchain langchain-openai pydantic python-dotenv streamlit
```

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

### Running the notebooks

Open any notebook (1–9.1) in Jupyter or VS Code and run the cells in order:

```bash
jupyter notebook
```

### Running the chatbot UI

```bash
cd 9_2_chatbot_UI
streamlit run frontend.py
```

## License

MIT — see [LICENSE](LICENSE).
