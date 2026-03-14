import pandas as pd
from openai import OpenAI

client = OpenAI()

def generate_commentary(df):
    data_summary = df.describe().to_string()

    prompt = f"""
    Generate professional portfolio commentary based on this data:
    {data_summary}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
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