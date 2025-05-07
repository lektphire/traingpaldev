from langchain_core.prompts import ChatPromptTemplate
from src.structures.state import State
from src.utils.helpers import get_llm

print("Reached postmarket")


def postmarket(state: State):
    system_template = '''Instruction: You are an expert in analyzing post-market trading data. Your job is to review the performance of individual trades, 
    identify patterns in the execution, and suggest potential refinements.
    Format your response as follows:
    Summary: [Your summary and reasoning here] 
    Key Patterns: [Any patterns identified in the user's trades]
    Suggested Refinements: [Your suggestions for improving the trading strategy]
    '''

    user_template = '''User's Trade Performance: {performance_data}
    Question: Based on the user's trade data, what are your suggestions for improving their trading strategy?'''

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", user_template)]
    )

    performance_data = '''
    User's Trade History:
    - Buy: 100 shares of AAPL at $150, sell at $160
    - Buy: 50 shares of MSFT at $200, sell at $190
    - ...
    '''

    prompt = prompt_template.invoke({"performance_data": performance_data})

    response = get_llm().invoke(prompt)
    print(response.content)