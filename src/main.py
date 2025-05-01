import os
import getpass
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langgraph.types import Command

print("We have reached here")
from graph import trading_pal
print("Point 2")
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

    follow_up = input("\nEnter response to follow-up (if needed): ").strip()
    if follow_up:
        print("\n--- Continuing Conversation ---")
        for event in graph.stream(Command(resume=follow_up), config=thread_config, stream_mode="values"):
            for message in event['messages']:
                print(message)

if __name__ == "__main__":
    main()