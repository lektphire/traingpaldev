from src.utils.helpers import get_llm
from src.structures.state import State
import json
from langchain_core.messages import AIMessage

system_prompt = """
You are StrategyExpert, an AI trained to extract structured trading plans from natural language inputs.
Your job is to convert a user's free-form description of a trading strategy into a structured JSON object.

Output only a JSON object in the following format:
{
  "entry_condition": "...",
  "exit_condition": "...",
  "position_size": "...",
  "timeframe": "...",
  "stop_loss": "...",
  "take_profit": "..."
}
"""

few_shot_examples = [
    {
        "role": "user",
        "content": "Buy when RSI crosses below 30 and price is above 200 EMA. Sell when RSI crosses above 70. Use 10% of equity per trade on the 1h chart. Set a stop loss at 5% and a take profit at 15%."
    },
    {
        "role": "assistant",
        "content": """{
  "entry_condition": "RSI crosses below 30 and price is above 200 EMA",
  "exit_condition": "RSI crosses above 70",
  "position_size": "10% of account equity",
  "timeframe": "1h",
  "stop_loss": "5%",
  "take_profit": "15%"
}"""
    }
]

def extract_strategy(nl_input: str) -> dict:
    llm = get_llm()

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        *few_shot_examples,
        {"role": "user", "content": nl_input}
    ])

    message = response.content
    print("Raw structured output:\n", message)

    try:
        return json.loads(message)
    except json.JSONDecodeError:
        print("Structured parsing failed.")
        return {"error": "Failed to parse strategy into structured format."}

def generate_pine_direct(nl_input: str) -> str:
    prompt = [
        {"role": "system", "content": "Convert the following trading strategy into Pine Script. Output only the Pine Script code."},
        {"role": "user", "content": nl_input}
    ]
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content.strip()

def strategy(state: State):
    print("---------Strategy---------")
    user_message = next((msg.content for msg in state["messages"] if msg.type == "human"), "")
    pine_script = generate_pine_direct(user_message)
    print("Pine Script Output:\n", pine_script)

    return {
        "messages": state["messages"] + [AIMessage(content=pine_script)]
    }
