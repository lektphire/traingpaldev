from src.utils.helpers import get_llm
from src.structures.state import State

def strategy(state: State):
    print("---------Strategy---------")
    return {"messages": [get_llm().invoke(state["messages"])]}