# Bradford Agentic AI Hackathon — ML + Agent MVP

This is a runnable starter project for the Bradford Agentic AI Hackathon.

## What it demonstrates

User request → ML intent classification → agent planning → tool selection → data retrieval → analysis → final answer.

The demo uses a local product knowledge base so it works without an API key or internet connection.

## Run on Windows

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate it:

```bash
.venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Start the application:

```bash
streamlit run app.py
```

7. Open the local address shown by Streamlit, normally:

```text
http://localhost:8501
```

## Try this prompt

> What are the best entry-level laptops for computer science students under £800 in the UK?

## How the AI works

### Machine Learning
A TF-IDF + Logistic Regression model classifies the user's intent.

### Agent
The agent chooses a workflow based on that intent.

### Tools
The laptop workflow calls a local product knowledge-base tool and a scoring/analysis tool.

### Output
The UI shows the final recommendations and an expandable explanation of the agent workflow.

## Next hackathon upgrades

- Connect an LLM such as OpenAI, Gemini or Claude.
- Add web search.
- Add a vector database/RAG knowledge base.
- Add live retailer APIs.
- Add persistent chat history.
- Add a human approval step before actions.
- Add evaluation tests for accuracy.
- Deploy the application.
