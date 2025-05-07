from langgraph.types import Command, interrupt
from src.structures.state import State
from src.utils.helpers import get_llm
from langchain_core.messages import HumanMessage, AIMessage


def human_clarification(state: State, config):
    print("---------Human Clarification---------")

    # default
    clarification_message = "Could you please clarify your request? I can assist with premarket, intraday, postmarket, and strategy inquiries."

    # add custom configs somehow later

    user_input = interrupt(clarification_message)  # This pauses the graph execution to collect input

    user_input = user_input.strip()

    # If user provides clarification, add it to the messages
    if user_input:
        print(f"User provided clarification: {user_input}")
        return Command(
            update={"messages": state["messages"] + [HumanMessage(content=user_input)]},
            goto="chatbot"  # Route back to the chatbot to process gating logic
        )
    else:
        print("No clarification input received. Reusing existing messages.")
        return Command(
            update={"messages": state["messages"]},
            goto="chatbot"  # Route back to the chatbot even if no input is provided
        )