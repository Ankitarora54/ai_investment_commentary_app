import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv
from openai import OpenAI
from utils.analytics import calculate_allocation, calculate_metrics, compare_with_benchmark, compare_portfolios
from utils.commentary import generate_commentary
from utils.pdf_generator import generate_pdf_report
from utils.rag_engine import get_market_context
from utils.commentary import generate_comparison_commentary
from utils.analytics import calculate_risk_metrics

def load_css():
    with open("app/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

def get_sample_files():
    sample_path = "data/sample"
    files = [f for f in os.listdir(sample_path) if f.endswith(".csv")]
    return files, sample_path

def display_kpis(metrics, benchmark_data=None, risk_metrics=None):

    # 🔹 Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Avg Return", f"{metrics['avg_return']:.2f}%")
        with st.expander("Details"):
            st.write("Average return across portfolio")

    with col2:
        st.metric("Total Return", f"{metrics['total_return']:.2f}%")
        with st.expander("Details"):
            st.write("Total portfolio return")

    st.markdown(" ")  # spacing

    # 🔹 Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.metric("Top Performer", metrics['top_stock'])
        with st.expander("Details"):
            st.write(f"{metrics['top_stock']} returned {metrics['top_return']:.2f}%")

    with col4:
        st.metric("Worst Performer", metrics['worst_stock'])
        with st.expander("Details"):
            st.write(f"{metrics['worst_stock']} returned {metrics['worst_return']:.2f}%")

    st.markdown(" ")  # spacing

    # 🔹 Row 3
    col5, col6 = st.columns(2)

    with col5:
        st.metric("Volatility", f"{risk_metrics['volatility']:.2f}%")
        with st.expander("Details"):
            st.write("Standard deviation of returns")

    with col6:
        st.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
        with st.expander("Details"):
            st.write("Risk-adjusted return (Sharpe Ratio)")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="Investment Commentary Generator", layout="wide")
st.title("Investment Commentary Generator")
st.markdown("AI-Powered Investment Reporting Tool")
st.caption("Generate portfolio insights, comparisons, and client-ready commentary using AI.")

# Sidebar
st.sidebar.title("Navigation")
mode = st.sidebar.radio(
    "Select Function",
    ["Single Portfolio Summary","Compare Portfolios"]
)
st.sidebar.markdown("---")

# Global controls
period = st.sidebar.selectbox("Reporting Period", ["Monthly", "Quarterly"])
client_type = st.sidebar.selectbox("Client Type", ["Retail", "Institutional"])

if mode == "Single Portfolio Summary":
    st.subheader("Generate Commentary for a Single Portfolio")
    #st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Select Data Source")
    data_source = st.radio("Choose input method:",["Use Sample File"
                                                   , "Upload Your Own File"])
    df = None
    uploaded_file = None
    selected_file = None
    if data_source == "Use Sample File":
        uploaded_file = None
        files, sample_path = get_sample_files()
        file_options = ["-- Select a file --"] + files
        selected_file = st.selectbox("Select Sample File", file_options,index=0)
        if selected_file != "-- Select a file --":
            file_path = os.path.join(sample_path, selected_file)
            df = pd.read_csv(file_path)
            st.success(f"Loaded sample file: {selected_file}")
    elif data_source == "Upload Your Own File":
        selected_file = None
        uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"])
        if uploaded_file:
            #selected_file = st.selectbox("Select Sample File", files)
            #uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])
            #period = st.selectbox("Select Reporting Period", ["Monthly", "Quarterly"])
            df = pd.read_csv(uploaded_file)
            st.subheader("Portfolio Data")
            st.dataframe(df)

    if selected_file is not None and selected_file != "-- Select a file --" or uploaded_file is not None:

        if st.button("Generate AI Commentary"):
            metrics = calculate_metrics(df)
            risk_metrics = calculate_risk_metrics(df)
            benchmark_data = compare_with_benchmark(metrics['avg_return'])
            #st.markdown('<div class="section-card">', unsafe_allow_html=True)
            
            #Potfolio Allocation Pie Chart
            col1, col2= st.columns([2, 2])
            #st.markdown('<div class="section-card-small">', unsafe_allow_html=True)
            with col2:
                st.subheader("Portfolio Allocation")
                allocation = calculate_allocation(df)
                fig, ax = plt.subplots()
                ax.pie(allocation, labels=allocation.index, autopct='%1.1f%%')
                ax.set_title("Sector Allocation")
                st.pyplot(fig)
            #st.markdown('</div>', unsafe_allow_html=True)

            # KPI SECTION
            with col1:
                #st.markdown('<div class="section-card-small">', unsafe_allow_html=True)
                st.subheader("Key Metrics")
                display_kpis(metrics, benchmark_data, risk_metrics)
                #st.markdown('</div>', unsafe_allow_html=True)

            #Risk Section
            # st.markdown('<div class="section-card-small">', unsafe_allow_html=True)
            # st.subheader("Risk Analysis")
            # col1, col2 = st.columns(2)
            # col1.metric("Volatility", f"{risk_metrics['volatility']:.2f}%")
            # col2.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
            # st.markdown('</div>', unsafe_allow_html=True)

            # Chart
            # col1, col2, col3 = st.columns([1, 4, 1])  # middle column controls width

            # with col2:
            #     st.subheader("Sector Performance")
            #     sector_chart = df.groupby('sector')['return'].mean()
            #     st.bar_chart(sector_chart)

            #Chart
            st.subheader("Sector Performance")
            sector_chart = df.groupby('sector')['return'].mean().reset_index()
            fig = px.bar(
                sector_chart,
                x='sector',
                y='return',
                title="",
            )
            # CONTROL HEIGHT HERE
            fig.update_layout(height=250)  # try 250–400
            st.plotly_chart(fig, use_container_width=True)            
            
            #Generate Commentary
            with st.spinner("Generating AI commentary..."):
                # commentary = generate_commentary(metrics,benchmark_data,period
                #                             ,client_type,market_context="",client = client)
                commentary="AA"
            st.subheader("Portfolio Insights & Market Outlook")
            st.markdown(f'<div class="commentary-box">{commentary}</div>', unsafe_allow_html=True)
            
            #Store PDF in session state for download
            pdf_file = generate_pdf_report(
                metrics,
                risk_metrics,
                allocation,
                df,
                commentary
                )
            st.session_state["pdf_file"] = pdf_file

            # PDF download
            #if st.button("Download Full Report"):
            if "pdf_file" in st.session_state:
                with open(st.session_state["pdf_file"], "rb") as f:
                    st.download_button(
                        label="Download Full Report",
                        data=f,
                        file_name="investment_report.pdf",
                        mime="application/pdf"
                    )
                #with open(pdf_file, "rb") as f:
                 #   st.download_button("Download PDF", f, file_name="investment_report.pdf")           

elif mode == "Compare Portfolios":
    st.write("This mode allows you to upload two different portfolios and compare their performance, generating a comprehensive commentary on the differences and insights.")
    st.subheader("Compare Two Portfolios")
    #client_type = st.selectbox("Client Type", ["Retail", "Institutional"])
    #market_context = get_market_context()
    file1 = st.file_uploader("Upload Portfolio 1", type=["csv"], key="p1")
    file2 = st.file_uploader("Upload Portfolio 2", type=["csv"], key="p2")

    if file1 and file2:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        p1_metrics = calculate_metrics(df1)
        p2_metrics = calculate_metrics(df2)

        comparison = compare_portfolios(df1, df2)
        st.write("Comparison Summary", comparison)

        if st.button("Generate Comparison Commentary"):
            with st.spinner("Generating AI commentary..."):
                from utils.rag_engine import get_market_context
                market_context = get_market_context()
                commentary = generate_comparison_commentary(p1_metrics,p2_metrics
                                                        ,comparison,client_type
                                                        ,market_context,period="Monthly"
                                                        ,client=client)
            st.subheader("Generated Comparison Commentary")
            st.write(commentary)
