from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from IPython.display import Image, display
from src.experts import premarket, intraday, postmarket, strategy
from src.components import chatbot, human_clarification, summary
from src.structures.state import State
from src.utils.helpers import get_llm

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.types import interrupt

classification_template = PromptTemplate.from_template(
    """You are an expert question classifier for a financial trading assistant. Classify the user's message into exactly one of the following categories: premarket, intraday, postmarket, strategy. 
    
    <PreMarket:Analyzes overnight news, economic releases, and global market trends.>
    <IntraDay: Focuses on real-time technical analysis, order book dynamics, and short-term predictions.>
    <PostMarket: Reviews trade performance, identifies patterns in execution, and suggests refinements.>
    <Strategy: Translates natural language trading ideas/plans into structured formats or code snippets.>
    
    User message: {input}
    Classification:
    """
)

llm=get_llm()

classification_chain = classification_template | llm | StrOutputParser()

def route_to_agent(user_input: str) -> str:
    response = classification_chain.invoke({"input": user_input}).strip().lower()
    print("Router LLM classified input as:", response)
    valid = {"premarket", "intraday", "postmarket", "strategy"}
    return response if response in valid else "chatbot"

def gating_mechanism(state: State):
    print("Reached gating")
    last_input = state["messages"][-1].content
    response = classification_chain.invoke({"input": last_input}).strip()
    valid = {"premarket", "intraday", "postmarket", "strategy"}

    if response.lower() in valid:
        return [response.lower()]
    else:
        # Interrupt to ask user directly using LangGraph-native interrupt function
        question = response if response else "Could you clarify your request?"
        clarification = interrupt(question)
        return {"messages": state["messages"] + [HumanMessage(content=clarification)]}


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
    # graph_builder.add_conditional_edges("chatbot", lambda state: [route_to_agent(state["messages"][-1].content)], ["human_clarification", "premarket", "intraday", "postmarket", "strategy"])

    graph_builder.add_conditional_edges(
        "chatbot",
        lambda state: ["human_clarification"] if "human_clarification" in state["messages"][-1].content else ["premarket", "intraday", "postmarket", "strategy"],
        [
            "chatbot",
            "human_clarification",
            "premarket",
            "intraday",
            "postmarket",
            "strategy"
        ]
    )
    # graph_builder.add_conditional_edges("chatbot", gating_mechanism, [
    #     "chatbot", "premarket", "intraday", "postmarket", "strategy"
    # ])
    graph_builder.add_node("summary", summary)
    graph_builder.add_edge("premarket", "summary")
    graph_builder.add_edge("intraday", "summary")
    graph_builder.add_edge("postmarket", "summary")
    graph_builder.add_edge("strategy", "summary")
    graph_builder.add_edge("summary", END)

    checkpointer = MemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)

if "__main__" == __name__:
    print("Point 4")
    graph = trading_pal()
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass

    # thread_config = {"configurable": {"thread_id": "paldemo"}}
    # for event in graph.stream({"messages": [HumanMessage("I have a strategy where I buy when price decreases")]}, config=thread_config, stream_mode="values"):
    #     print(event['messages'][-1])
    #
    # print(graph.get_state(thread_config).next)