import pandas as pd
import numpy as np

# NEW: Risk Metrics
def calculate_risk_metrics(df, risk_free_rate=0.02):
    returns = df['return'] / 100  # convert %

    volatility = np.std(returns)
    avg_return = np.mean(returns)

    sharpe_ratio = (avg_return - risk_free_rate) / volatility if volatility != 0 else 0

    return {
        "volatility": volatility * 100,
        "sharpe_ratio": sharpe_ratio
    }

#Calculate Metrics
def calculate_metrics(df: pd.DataFrame):
    """
    Calculates key portfolio performance metrics.

    Parameters:
    df (DataFrame): Portfolio data with columns ['stock', 'sector', 'return']

    Returns:
    dict: Dictionary containing calculated metrics
    """

    # Basic metrics
    avg_return = df['return'].mean()
    total_return = df['return'].sum()

    # Top and worst performers
    top = df.loc[df['return'].idxmax()]
    worst = df.loc[df['return'].idxmin()]

    # Sector-level performance
    sector_performance = df.groupby('sector')['return'].mean().to_dict()

    return {
        "avg_return": avg_return,
        "total_return": total_return,
        "top_stock": top['stock'],
        "top_return": top['return'],
        "worst_stock": worst['stock'],
        "worst_return": worst['return'],
        "sector_performance": sector_performance
    }


# NEW: Allocation
def calculate_allocation(df):
    df['weight'] = 1 / len(df)  # equal weight assumption
    allocation = df.groupby('sector')['weight'].sum()
    return allocation


def compare_with_benchmark(portfolio_return, benchmark_return=2.0):
    alpha = portfolio_return - benchmark_return
    return {
        "benchmark": benchmark_return,
        "alpha": alpha,
        "outperformance": alpha > 0
    }

def compare_portfolios(df1, df2):
    return {
        "portfolio_1_return": df1['return'].mean(),
        "portfolio_2_return": df2['return'].mean(),
        "difference": df1['return'].mean() - df2['return'].mean()
    }