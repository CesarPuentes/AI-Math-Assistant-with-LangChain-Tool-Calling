# AI Math Assistant (Ollama Version)

This project is an AI-powered mathematical assistant that runs 100% locally using **Ollama** and **LangChain**.

Unlike a standard chatbot that guesses mathematical answers, this assistant uses **Tool Calling**: it identifies the problem and uses Python code tools (a calculator) to obtain precise answers, eliminating numerical hallucinations.

## 🚀 Prerequisites

1.  **Python 3.10+** installed.
2.  **Ollama** installed and running.

### Ollama Setup
Ensure you have Ollama installed and the `llama3.1` model downloaded (which is the default used by the script).

```bash
# Install Ollama (Linux/Mac)
curl -fsSL https://ollama.com/install.sh | sh

# Download the model
ollama pull llama3.1

# Start the server (if not already running)
ollama serve
```

## 🛠️ Installation

1.  Clone or download this repository.
2.  Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install langchain-ollama langchain-core langgraph
    ```

## 💻 Usage

Simply run the main script:

```bash
python math_assistant_ollama.py
```

The script will execute a series of automated tests demonstrating the agent's capabilities:
1.  **Unit Tests**: Addition, subtraction, multiplication, and division.
2.  **Reasoning Tests**: It will solve a complex GDP (Gross Domestic Product) problem by summing values extracted from a text.

## 🧠 How it Works

The `math_assistant_ollama.py` script defines several tools (`add_numbers`, `subtract_numbers`, etc.) and creates a ReAct agent.

1.  The agent receives a natural language query ("Add 10 and 20").
2.  The model (Llama 3.1) decides which tool to use.
3.  Python code executes the actual mathematical operation.
4.  The agent returns the precise final answer.

For more theoretical details, see the [Teoria.md](Teoria.md) file (in Spanish).
