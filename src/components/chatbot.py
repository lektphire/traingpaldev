from langchain_core.messages import SystemMessage
from langgraph.types import Command
from src.structures.state import State
from src.utils.helpers import get_llm
from langchain_core.messages import HumanMessage, AIMessage

chatbot_instructions = """
You are a routing assistant for a stock market chatbot. Your job is to analyze the user’s message and route it to one or more appropriate expert agents. Choose from the following five options:

- premarket: for questions about recent news or market trends.
- intraday: for questions about active or ongoing trades.
- postmarket: for reviewing trades or performance after the trading day.
- strategy: for proposed or hypothetical trading strategies.
- human_clarification: for questions that are not finance-related or require additional clarification

Instructions:

- Respond with one or more space-separated agent names. 
- Do not have duplicate names.
- If you include human_clarification, it must be the only agent selected. 
- If human_clarification is selected, include a follow-up question on the second line. If necessary, acknowledge what the user has said and gently remind the user that you're specifically designed as a trading assistant that can assist with premarket, intraday, postmarket, and strategy inquiries.
""".strip()

valid_experts = {"premarket", "intraday", "postmarket", "strategy"}

def chatbot(state: State):
    print("---------Chatbot---------")
    prompt = [SystemMessage(chatbot_instructions)] + state["messages"]
    ans = get_llm().invoke(prompt).content
    print(ans)
    # if "human_clarification" in ans:
    #     return Command(
    #         update={"messages": [ans.splitlines()[1]]},
    #         goto="human_clarification",
    #     )
    # else:
    #     expert_names = ans.strip().split()
    #     while(not all(expert in valid_experts for expert in expert_names)
    #           or len(expert_names) > len(set(expert_names))):
    #         ans = get_llm().invoke(prompt).content
    #     print(expert_names)
    #     return Command(
    #         goto=expert_names
    #     )



def human_clarification(state: State, config):
    print("---------Human Clarification---------")
    clarification = ""
    if "interrupts" in config and config["interrupts"]:
        clarification = config["interrupts"][0].get("value", "").strip()

    if clarification:
        return {
            "messages": state["messages"] + [HumanMessage(content=clarification)]
        }
    else:
        print("No clarification input received. Reusing existing messages.")
        return {
            "messages": state["messages"]
        }