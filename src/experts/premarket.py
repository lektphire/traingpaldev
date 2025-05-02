from langchain_core.prompts import ChatPromptTemplate
from src.structures.state import State
from src.utils.helpers import get_llm
print("reached premarket)")
def premarket(state: State):

    system_template = '''Instruction: You are provided with a news article. Please provide a market level summary and predict the market trends for the next trading day. Your
    response should include your reasoning followed by key levels (ex. Fibonacci Key Levels), potential watchlist stocks, and initial risk assessment.
    Format your response as follows: 
    Summary: [Your summary and reasoning
    here] 
    Key Levels: [Statistics and key levels here] 
    Potential Watchlist: [List of stocks here ranked by importance]
    Initial Risk Assessment: [Your initial risk assessment here]
    '''

    user_template = '''News Article: {article}
    Question: Taking into account the information in the news article above, how
    has the market performed recently, and what are your predictions for the next trading day?'''
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", user_template)]
    )

    prompt = prompt_template.invoke({"article": '''Trump says he has no plans to fire Fed's Powell; market jumps
    WASHINGTON, April 22 (Reuters) - President Donald Trump on Tuesday backed off from threats to fire Federal Reserve Chair Jerome Powell after days of intensifying criticisms of the central bank chief for not cutting interest rates.
    "I have no intention of firing him," Trump told reporters in the Oval Office on Tuesday. "I would like to see him be a little more active in terms of his idea to lower interest rates," he added.
    The de-escalation drew an immediate thumbs up from Wall Street, as equity index futures jumped by nearly 2%% on the resumption of trading on Tuesday evening. Stocks, bonds and the U.S. dollar had all slumped on Monday after Trump over the Easter holiday weekend repeatedly attacked Powell for not cutting interest rates further since the president resumed office in January.
    “Whether this reflects Monday’s brutal foretaste of what would happen in markets if he did try to fire Powell, or was the plan all along, it is a clear positive," wrote Evercore ISI Vice Chairman Krishna Guha. “It materially reduces the likelihood of worst case outcomes including stagflation and the morphing of the tariff crisis into a sovereign debt crisis, though these risks remain.”
    Also during his question-and-answer volley with reporters on Tuesday, Trump expressed optimism that a trade deal with China could "substantially" cut tariffs, which also provided a boost for investors. He said a deal would result in "substantially" lower tariffs on Chinese goods, suggesting that a final deal will not "be anywhere near" current tariff rates. But "it won't be zero," he added.
                                    The combination of the rocky rollout of Trump's tariffs and, more recently, his repeated barbs at Powell and the Fed had rattled investors and intensified selling of U.S. assets including stocks, U.S. Treasuries and the dollar.
    Trump's broadsides were often accompanied by threatening remarks, such as last week's social media posting that Powell's termination as Fed chair "cannot come fast enough" and more personal jabs, such as calling Powell "a major loser." The threats spooked financial markets that view the Fed's independence as critical to underpinning its credibility as the world's most influential central bank and a cornerstone of global financial stability.
    But while Trump seems to have set aside those threats for now, his criticisms of Fed rate policy remain just as pointed.
    "We think that it's a perfect time to lower the rate, and we'd like to see our chairman be early or on time, as opposed to late," Trump said.
                                    Trump's sour grapes with Powell date back to the Republican's first term in the White House. Trump elevated Powell from a Fed Board of Governors member to the central bank's head but was soon irritated by ongoing rate increases under Powell's watch. Trump openly mused about firing Powell, but was ultimately dissuaded by his advisers.
    Whether Trump has the authority is unclear. Powell, for his part, insists that the Federal Reserve Act of 1913 that created the central bank will not allow it. Trump, meanwhile, has said that if he wanted Powell out, he would be gone "real fast."
    The law stipulates that the seven Fed governors, appointed by the president and confirmed by the Senate to staggered 14-year terms, can only be removed for "cause" - long thought to mean misconduct, not policy disagreement.
    That said, the law omits reference to limits on removal from its description of the four-year term of the Fed chair, who is one of the seven governors.
    Trump's harsh rhetoric came alongside court cases now proceeding over his firing of officials from other independent federal boards and agencies. Those are being watched closely in Fed circles as potential proxies for whether Trump has the authority to fire Fed officials long presumed to be able to pursue monetary policy free from political influence.
    The Fed lowered interest rates by a percentage point late last year to the current range of 4.25% to 4.50%, but has held them unchanged in the two policy meetings convened since Trump returned to the White House. The Fed's next rate-setting meeting is in two weeks.
    Fed policymakers are concerned that the aggressive tariffs rolled out by Trump since early February could rekindle inflation that they had already found harder than expected to return to their 2% target. At the same time, policymakers worry their job could be complicated further if tariffs slow growth and drive up unemployment while also pressuring up inflation.
    The result is a wait-and-see posture regarding further rate cuts, though most policymakers still see some rate reductions as likely later this year.
    Interest rate futures traders pared bets on Fed policy easing after Trump's remarks, and now are pricing three quarter-point interest-rate cuts by year's end, versus the four seen as earlier as more likely.
    So far, "hard data" measures of the U.S. economy such as employment and retail sales reports have shown resilience, but surveys of households and businesses have shown rapidly deteriorating confidence. The consensus now among economists is that risks are skewed broadly to the downside from here as the effects of tariffs begin to stack up.
    The International Monetary Fund on Tuesday slashed its outlook for both U.S. and global growth this year, with Trump's tariffs policy the central reason behind the downgrade.                                '''})

    prompt.to_messages()
    response = get_llm().invoke(prompt)
    print(response.content)