import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os
from utils.analytics import calculate_metrics, compare_with_benchmark, compare_portfolios
from utils.commentary import generate_commentary
from utils.pdf_generator import generate_pdf
from utils.rag_engine import get_market_context
from utils.commentary import generate_comparison_commentary

def load_css():
    with open("app/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_sample_files():
    sample_path = "data/sample"
    files = [f for f in os.listdir(sample_path) if f.endswith(".csv")]
    return files, sample_path

load_css()

load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="Investment Commentary Generator", layout="wide")
st.title("Investment Commentary Generator")
st.markdown("AI-Powered Investment Reporting Tool")
st.caption("Generate portfolio insights, comparisons, and client-ready commentary using AI.")

mode = st.selectbox(
    "Select Mode",
    ["Generate Single Portfolio Summary","Compare 2 Portfolios"]
)

period = st.selectbox("Select Reporting Period", ["Monthly", "Quarterly"])
client_type = st.selectbox("Client Type", ["Retail", "Institutional"])

if mode == "Generate Single Portfolio Summary":
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
        # Chart
        st.subheader("Sector Performance")
        sector_chart = df.groupby('sector')['return'].mean()
        st.bar_chart(sector_chart)

    if st.button("Generate AI Commentary"):
        metrics = calculate_metrics(df)
        benchmark_data = compare_with_benchmark(metrics['avg_return'])
        with st.spinner("Generating AI commentary..."):
            commentary = generate_commentary(metrics,benchmark_data,period
                                        ,client_type,market_context="",client = client)

        st.subheader("Generated Commentary")
        st.write(commentary)

        # PDF download
        pdf_file = generate_pdf(commentary)
        with open(pdf_file, "rb") as f:
            st.download_button("Download Report", f, file_name="commentary.pdf")
    st.markdown('</div>', unsafe_allow_html=True)

elif mode == "Compare 2 Portfolios":
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
