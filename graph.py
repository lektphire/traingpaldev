from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from IPython.display import Image, display
from src.experts import premarket, intraday, postmarket, strategy
from src.components import chatbot, human_clarification, summary
from src.structures.state import State

def trading_pal():
    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("human_clarification", human_clarification)
    graph_builder.add_node("premarket", premarket)
    graph_builder.add_node("intraday", intraday)
    graph_builder.add_node("postmarket", postmarket)
    graph_builder.add_node("strategy", strategy)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("human_clarification", "chatbot")
    # graph_builder.add_conditional_edges("chatbot", gating_mechanism, ["human_clarification", "premarket", "intraday", "postmarket", "strategy"])
    graph_builder.add_node("summary", summary)
    graph_builder.add_edge("premarket", "summary")
    graph_builder.add_edge("intraday", "summary")
    graph_builder.add_edge("postmarket", "summary")
    graph_builder.add_edge("strategy", "summary")
    graph_builder.add_edge("summary", END)

    checkpointer = MemorySaver()
    return graph_builder.compile(checkpointer=checkpointer, interrupt_before=["human_clarification"])

if "__main__" == __name__:
    graph = trading_pal()
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass

    thread_config = {"configurable": {"thread_id": "paldemo"}}
    for event in graph.stream({"messages": [HumanMessage("I have a strategy where I buy when price decreases")]}, config=thread_config, stream_mode="values"):
        print(event['messages'][-1])

    print(graph.get_state(thread_config).next)