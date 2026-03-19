import pandas as pd

def generate_commentary(metrics, benchmark_data, period="Monthly", client= None):

    prompt = f"""
    You are a senior investment analyst writing {period} portfolio commentary.

    Portfolio Metrics:
    - Average Return: {metrics['avg_return']:.2f}%
    - Total Return: {metrics['total_return']:.2f}%
    - Top Performer: {metrics['top_stock']} ({metrics['top_return']}%)
    - Worst Performer: {metrics['worst_stock']} ({metrics['worst_return']}%)
    - Sector Performance: {metrics['sector_performance']}

    Benchmark:
    - Benchmark Return: {benchmark_data['benchmark']}%
    - Alpha: {benchmark_data['alpha']:.2f}%

    Instructions:
    - Professional institutional tone
    - Mention outperformance/underperformance
    - Highlight sectors
    - Keep concise (6–8 lines)
    - Add forward-looking insight

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