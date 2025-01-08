from pydantic import BaseModel, Field
from typing import Optional
from app.base_llms import llm_4o
from langchain_core.prompts import ChatPromptTemplate


def trade_decision_operation(htf_info_structured, mtf_info_structured, ltf_df):

    class Schema(BaseModel):
        enter_market: bool = Field(description="This variable stores the trade decision.")
        trade_type: Optional[str] = Field(description="This variable stores the type of trade(long or short).")
        entry_price: Optional[float] = Field(description="This variable stores the entry price of the trade.")
        stop_loss: Optional[float] = Field(description="This variable stores the stop loss price of the trade.")
        take_profit: Optional[float] = Field(description="This variable stores the take profit price of the trade.")
        confident_level: Optional[int] = Field(description="This variable stores the confidence level of the trade.")
        explanation: str = Field(description="This variable stores the explanation of the trade and/or the decision.")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("user", """
You are the Head Trader at a Forex Hedge Fund, analyzing EURUSD using Smart Money Concepts. Your tasks:

Gather & Interpret HTF/MTF Analysis
Confirm HTF bias (bullish or bearish).
Check MTF alignment; if they conflict, only trade if RR is high.
             
Locate Key Price Levels
Identify order blocks, fair value gaps (FVG), liquidity pools, or strong S/R.
No trade if price sits in a choppy/ranging structure with no clear advantage.
Consider the strength of the zones/levels as indicated in () in MTF analysis. 
             
Candlestick Confirmation
Wait for strong displacement or clear reversal candle (e.g., engulfing, shooting star) confirming direction.
Don’t enter immediately upon a liquidity sweep; wait for price to shift structure and show momentum.
             
Stop Loss & Take Profit
Generally, target the key levels, however make sure to prepare room for movement but not too much.
Stop loss: Place safely outside the order block/FVG, giving room for typical wicks.
Take profit: Target next major liquidity zone or FVG boundary. Consider partials at intermediate levels to lock gains.
Keep a higher reward-to-risk ratio (≥2:1 ideally, if it is contradicing with the setup don't force the tp up).

Confidence Level (1-10)
Only pull the trigger when alignment is solid and the setup meets your strict criteria.
If HTF and MTF diverge, skip or only take the trade if everything else screams high probability. 

Remember: Profit is the objective—avoid forcing trades if conditions aren’t there.
Stay disciplined: No overtrading, no “hope trades,” , always protect capital, and think step by step.
No explanation is needed for the trade decision.
    """),
            ("user", "HTF Analysis"),
            ("user", "{htf_analysis}"),
            ("user", "MTF Analysis"),
            ("user", "{mtf_analysis}"),
            ("user", "Market data"),
            ("user", "{ltf_df}"),
            ("user", "Keep you responses concise and striaght to the point!")
        ]
    )
    
    trade_agent_chain = prompt | llm_4o().with_structured_output(Schema)

    trade_info = trade_agent_chain.invoke({"htf_analysis": htf_info_structured, 
                                        "mtf_analysis": mtf_info_structured, 
                                        "ltf_df": ltf_df[-75:].to_string()})

    return trade_info


# Explanation
# Provide a concise reasoning: HTF–MTF alignment, key levels, candlestick trigger, and your final R:R.