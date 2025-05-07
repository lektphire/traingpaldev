import os
import getpass
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import trading_pal
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

def main():
    graph = trading_pal()

    thread_config = {"configurable": {"thread_id": "paldemo"}}

    user_input = input("What can TradingPal help you with today? ")
    print("\n--- LangGraph Response ---")
    for event in graph.stream({"messages": [HumanMessage(user_input)]}, config=thread_config, stream_mode="values"):
        print(event['messages'][-1])

if __name__ == "__main__":
    main()