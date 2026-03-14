import pandas as pd

def generate_commentary(df):
    # Simple placeholder logic
    avg_return = df['return'].mean()

    if avg_return > 0:
        sentiment = "positive performance"
    else:
        sentiment = "negative performance"

    commentary = f"The portfolio delivered {sentiment} with an average return of {avg_return:.2f}%."

    return commentary
