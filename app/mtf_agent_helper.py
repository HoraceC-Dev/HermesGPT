from langchain_core.prompts import ChatPromptTemplate
from app.base_llms import llm_llama


def mtf_agent_operation(mtf_df):

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
You are an advanced Forex Analyst specializing in Smart Money Concepts on the 1-hour timeframe. Your tasks:

Determine the current trend bias (bullish, bearish, ranging)

Identify 1H Order Blocks
Bullish OB: Typically the last down candle (or small cluster) before an impulsive up move that breaks structure.
Bearish OB: Typically the last up candle (or cluster) before an impulsive down move that breaks structure.
Only consider high-probability OBs where there is clear displacement (strong momentum) away from the zone and a structure shift.
             
Mark Key Liquidity Pools
Above relative equal highs (potential “buy stops” for liquidity).
Below relative equal lows (potential “sell stops” for liquidity).
Notable swing highs/lows where price repeatedly reacts.
Focus on pools that haven’t yet been “swept” or tapped.
             
Locate Fair Value Gaps (FVGs)
Look for 3-candle formations (Candle 1’s high and Candle 3’s low not overlapping, or vice versa) indicating an imbalance.
A high-probability FVG is one that forms alongside a strong displacement and lines up with an OB or liquidity zone.
             
For each OB or FVG, include approximate price boundaries (e.g., 1.0520–1.0535).
If it’s a single swing high/low, you can note that level as well.

Format your final analysis as follows:
Current Trend Bias: [bullish / bearish / ranging] (rate 1-10 how strong the trend is)
Identified Order Blocks: ... (rate 1-10 strength of each zone)
Liquidity Zones/Level: ...(rate 1-10 strength of each zone)
Fair Value Gaps: ...(rate 1-10 strength of each zone)
Brief Explanation (1 sentence): Summarize the main confluence factors. 

Keep your analysis concise.
             
Important Reminders
Think step by step.
Only highlight high-probability Zones/Levels.
Focus on synergy between OBs, FVGs, and liquidity sweeps for a solid SMC approach.
Specify the date of the data that you recieved.
    """),
            ("user", "1H Data"),
            ("user", "{mtf_df}"),
        ]
    )

    mtf_agent_chain = prompt | llm_llama()

    mtf_info = mtf_agent_chain.invoke({"mtf_df": mtf_df.to_string()})

    mtf_info_structured = mtf_info.content

    return mtf_info_structured


def mtf_info_summary(doc):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
You are an expert forex report generator.
             
Your task is to interpret the given text and analysis report from 3 different agent and summarize them into one single report.
Please format your response as follows:
Current/Recent Trend Bias: [bullish / bearish / ranging] (rate 1-10 how strong the trend is)
Identified Order Blocks: ... 
Liquidity Zones/Level: ...
Fair Value Gaps: ...
Brief Explanation (1 sentence): Summarize the main confluence factors. 
Remember to mention the strength of each zone/level

Important Note: Keep your responses concise.
"""),
("user", "{doc}")
        ]
    )
    chain = prompt | llm_llama()

    result_msg = chain.invoke({"doc": doc})

    return result_msg.content