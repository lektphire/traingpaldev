from src.utils.helpers import get_llm
from src.structures.state import State

def postmarket(state: State):
    print("---------Postmarket---------")
    return {"messages": [get_llm().invoke(state["messages"])]}