from langchain_core.prompts import ChatPromptTemplate
from app.base_llms import llm_llama

def htf_agent_operation(htf_df):
    # HTF agent for identifying the trend bias
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
    You are a specialized Forex Market Analyst focusing on higher-timeframe trends using Smart Money Concepts.
    Your job is to:
    1. Determine the overall trend (bullish, bearish, ranging) rate 1-10 how strong the trend is.
    2. Identify major swing points (highs/low, use the date to index).
    3. Summarize any significant daily order blocks or liquidity zones that are clearly visible (including swing high or low).

    Format your response as:
    - Overall HTF Bias: [bullish/bearish/ranging]
    - Key Swing Highs and Lows: ...
    - Any Notable Liquidity or Order Blocks: ...
    - Brief Explanation (1–2 sentences).

    Important:
    - Do not invent data. If uncertain, say “Not enough info.”
    - Be concise and to the point in your analysis.
    """),
            ("user", "Daily Data"),
            ("user", "{htf_df}"),
            ("user", "Please analyze this data to determine the 4h (HTF) directional bias, major swing points, and any relevant daily order blocks or liquidity pools.")
        ]
    )

    htf_agent_chain = prompt | llm_llama()

    htf_info = htf_agent_chain.invoke({"htf_df": htf_df.to_string()})

    htf_info_structured = htf_info.content

    return htf_info_structured