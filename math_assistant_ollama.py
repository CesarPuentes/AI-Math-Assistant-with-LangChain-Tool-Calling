"""
AI Math Assistant with Ollama - LangChain 1.2.7 Compatible
A demonstration of tool calling with LangChain using Ollama (Llama 3.1)
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import re

# =============================================================================
# 1. SETUP: Initialize Ollama LLM
# =============================================================================
print("=" * 60)
print("SETUP: Initializing Ollama LLM")
print("=" * 60)

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

# Quick test
response = llm.invoke("What is 2+2? Reply with just the number.")
print(f"LLM Test Response: {response.content}")


# =============================================================================
# 2. TOOL DEFINITIONS: All tools handle both list and string inputs
# =============================================================================
print("\n" + "=" * 60)
print("DEFINING TOOLS")
print("=" * 60)


def extract_numbers(inputs):
    """Helper function to extract numbers from various input types."""
    if isinstance(inputs, list):
        return [float(n) for n in inputs]
    elif isinstance(inputs, str):
        matches = re.findall(r'-?\d+\.?\d*', inputs)
        return [float(n) for n in matches if n and n != '-']
    elif isinstance(inputs, (int, float)):
        return [float(inputs)]
    else:
        return []


@tool
def add_numbers(inputs) -> dict:
    """
    Adds a list of numbers.
    
    Parameters:
    - inputs: Either a string containing numbers or a list of numbers
    
    Returns:
    - dict: {"result": sum of numbers}
    
    Example: "Add 10, 20, 30" or [10, 20, 30] -> {"result": 60}
    """
    numbers = extract_numbers(inputs)
    return {"result": sum(numbers)}


@tool
def subtract_numbers(inputs) -> dict:
    """
    Subtracts numbers sequentially: first - second - third...
    
    Parameters:
    - inputs: Either a string containing numbers or a list of numbers
    
    Returns:
    - dict: {"result": difference}
    
    Example: "100, 20, 10" -> {"result": 70}
    """
    numbers = extract_numbers(inputs)
    if not numbers:
        return {"result": 0}
    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    return {"result": result}


@tool
def multiply_numbers(inputs) -> dict:
    """
    Multiplies a list of numbers.
    
    Parameters:
    - inputs: Either a string containing numbers or a list of numbers
    
    Returns:
    - dict: {"result": product}
    
    Example: "2, 3, 4" -> {"result": 24}
    """
    numbers = extract_numbers(inputs)
    if not numbers:
        return {"result": 1}
    result = 1
    for n in numbers:
        result *= n
    return {"result": result}


@tool
def divide_numbers(inputs) -> dict:
    """
    Divides numbers sequentially: first / second / third...
    
    Parameters:
    - inputs: Either a string containing numbers or a list of numbers
    
    Returns:
    - dict: {"result": quotient}
    
    Example: "100, 5, 2" -> {"result": 10.0}
    """
    numbers = extract_numbers(inputs)
    if not numbers:
        return {"result": 0}
    result = numbers[0]
    for n in numbers[1:]:
        if n != 0:
            result /= n
    return {"result": result}


# Test the tools directly (tools expect string input when called manually)
print("\nDirect Tool Tests:")
print(f"  add_numbers('10 20 30') = {add_numbers.invoke('10 20 30')}")
print(f"  subtract_numbers('100, 20, 10') = {subtract_numbers.invoke('100, 20, 10')}")
print(f"  multiply_numbers('2, 3, 4') = {multiply_numbers.invoke('2, 3, 4')}")
print(f"  divide_numbers('100, 5, 2') = {divide_numbers.invoke('100, 5, 2')}")


# =============================================================================
# 3. CREATE AGENT: Using LangGraph's create_react_agent
# =============================================================================
print("\n" + "=" * 60)
print("CREATING AGENT")
print("=" * 60)

tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
agent = create_react_agent(model=llm, tools=tools)
print("Agent created successfully!")


# =============================================================================
# 4. TEST THE AGENT
# =============================================================================
print("\n" + "=" * 60)
print("TESTING AGENT")
print("=" * 60)


def run_agent(query):
    """Helper to run agent and print response."""
    print(f"\nQuery: {query}")
    try:
        response = agent.invoke({"messages": [("human", query)]})
        answer = response["messages"][-1].content
        print(f"Answer: {answer}")
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None


# Test queries
run_agent("What is 10 + 20 + 30?")
run_agent("Subtract 100 minus 20 minus 10")
run_agent("Multiply 2 times 3 times 4")
run_agent("Divide 100 by 5 and then by 2")

print("\n" + "=" * 60)
print("GDP Question Test")
print("=" * 60)
run_agent("In 2023, the US GDP was approximately 27.72 trillion, Canada's was 2.14 trillion, and Mexico's was 1.79 trillion. What is the total?")

print("\n" + "=" * 60)
print("MATH Question Test")
print("=" * 60)
run_agent("963+369−65×6÷9")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE!")
print("=" * 60)
