import pandas as pd
from openai import OpenAI
import os

client = OpenAI(api_key="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")

def generate_commentary(df: pd.DataFrame):

    # Basic summaries
    avg_return = df['return'].mean()
    top_performer = df.loc[df['return'].idxmax()]
    worst_performer = df.loc[df['return'].idxmin()]
    sector_summary = df.groupby('sector')['return'].mean().to_dict()

    # Build prompt
    prompt = f"""
    You are an investment analyst.

    Generate a professional portfolio commentary.

    Data:
    - Average Return: {avg_return:.2f}%
    - Top Performer: {top_performer['stock']} ({top_performer['return']}%)
    - Worst Performer: {worst_performer['stock']} ({worst_performer['return']}%)
    - Sector Performance: {sector_summary}

    Instructions:
    - Write in a professional tone
    - Keep it concise (5-6 lines)
    - Explain drivers of performance
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# def generate_commentary(df):
#     # Simple placeholder logic
#     avg_return = df['return'].mean()

#     if avg_return > 0:
#         sentiment = "positive performance"
#     else:
#         sentiment = "negative performance"

#     commentary = f"The portfolio delivered {sentiment} with an average return of {avg_return:.2f}%."

#     return commentary