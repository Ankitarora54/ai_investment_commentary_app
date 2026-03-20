import pandas as pd
from utils.personalization import get_client_prompt_modifier

def generate_commentary(metrics, benchmark_data, period="Monthly",client_type="Retail",market_context="", client= None):
    
    style_modifier = get_client_prompt_modifier(client_type)

    prompt = f"""
    You are a senior investment analyst preparing client commentary.

    {style_modifier}

    Market Environment:
    {market_context}

    Portfolio Highlights:
    - Avg Return: {metrics['avg_return']:.2f}%
    - Top Stock: {metrics['top_stock']}
    - Worst Stock: {metrics['worst_stock']}
    - Sector Performance: {metrics['sector_performance']}

    Benchmark Comparison:
    - Benchmark Return: {benchmark_data['benchmark']}%
    - Alpha: {benchmark_data['alpha']:.2f}%

    Instructions:
    - Explain performance drivers
    - Reference market conditions
    - Adjust tone based on client type
    - Provide 5–7 bullet points
    - Keep concise (8–10 lines)
    - Include forward outlook
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a CFA-level investment analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def generate_comparison_commentary(p1_metrics, p2_metrics, comparison, client_type, market_context, period, client= None):

    style_modifier = get_client_prompt_modifier(client_type)

    prompt = f"""
    You are a senior investment analyst preparing a comparative portfolio commentary.

    {style_modifier}

    Market Environment:
    {market_context}

    Portfolio 1:
    - Avg Return: {p1_metrics['avg_return']:.2f}%
    - Top Stock: {p1_metrics['top_stock']}
    - Sector Performance: {p1_metrics['sector_performance']}

    Portfolio 2:
    - Avg Return: {p2_metrics['avg_return']:.2f}%
    - Top Stock: {p2_metrics['top_stock']}
    - Sector Performance: {p2_metrics['sector_performance']}

    Comparison:
    - Return Difference: {comparison['difference']:.2f}%

    Instructions:
    - Compare performance drivers
    - Highlight sector allocation differences
    - Explain which portfolio outperformed and why
    - Reference market conditions
    - Provide 5–7 bullet points
    - Each bullet should be concise (1 line)
    - Keep concise (8–10 lines)
    - Include forward-looking insight

    Output:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a CFA-level investment analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# def generate_commentary(metrics, benchmark_data, period, client_type, market_context):

#     style_modifier = get_client_prompt_modifier(client_type)

#     prompt = f"""
#     You are a senior investment analyst.

#     {style_modifier}

#     Market Context:
#     {market_context}

#     Portfolio Metrics:
#     {metrics}

#     Benchmark:
#     {benchmark_data}

#     Generate {period} commentary.
#     """



# def generate_commentary(df: pd.DataFrame,client: OpenAI):
#     data_summary = df.head().to_string()
#     # Basic summaries
#     avg_return = df['return'].mean()
#     top_performer = df.loc[df['return'].idxmax()]
#     worst_performer = df.loc[df['return'].idxmin()]
#     sector_summary = df.groupby('sector')['return'].mean().to_dict()

#     # Build prompt
#     prompt = f"""
#     You are an investment analyst.

#     Generate a professional portfolio commentary.

#     Data:
#     - Average Return: {avg_return:.2f}%
#     - Top Performer: {top_performer['stock']} ({top_performer['return']}%)
#     - Worst Performer: {worst_performer['stock']} ({worst_performer['return']}%)
#     - Sector Performance: {sector_summary}

#     Instructions:
#     - Write in a professional tone
#     - Keep it concise (5-6 lines)
#     - Explain drivers of performance
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a financial analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     )

#     return response.choices[0].message.content

# def generate_commentary(df):
#     # Simple placeholder logic
#     avg_return = df['return'].mean()

#     if avg_return > 0:
#         sentiment = "positive performance"
#     else:
#         sentiment = "negative performance"

#     commentary = f"The portfolio delivered {sentiment} with an average return of {avg_return:.2f}%."

#     return commentary