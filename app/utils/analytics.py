import pandas as pd

def calculate_metrics(df):
    avg_return = df['return'].mean()
    total_return = df['return'].sum()

    top = df.loc[df['return'].idxmax()]
    worst = df.loc[df['return'].idxmin()]

    sector_perf = df.groupby('sector')['return'].mean().to_dict()

    return {
        "avg_return": avg_return,
        "total_return": total_return,
        "top_stock": top['stock'],
        "top_return": top['return'],
        "worst_stock": worst['stock'],
        "worst_return": worst['return'],
        "sector_performance": sector_perf
    }


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