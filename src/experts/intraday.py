from src.utils.helpers import get_llm
from src.structures.state import State
def intraday(state: State):
    print("---------Intraday---------")
    return {"messages": [get_llm().invoke(state["messages"])]}