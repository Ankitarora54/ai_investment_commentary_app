import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os
from utils.analytics import calculate_metrics, compare_with_benchmark
from utils.commentary import generate_commentary
from utils.pdf_generator import generate_pdf

load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("AI Investment Commentary Generator (Advanced)")

uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])

period = st.selectbox("Select Reporting Period", ["Monthly", "Quarterly"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Portfolio Data")
    st.dataframe(df)

    # Chart
    st.subheader("Sector Performance")
    sector_chart = df.groupby('sector')['return'].mean()
    st.bar_chart(sector_chart)

    if st.button("Generate AI Commentary"):
        metrics = calculate_metrics(df)
        benchmark_data = compare_with_benchmark(metrics['avg_return'])

        commentary = generate_commentary(metrics, benchmark_data, period,client)

        st.subheader("📄 Generated Commentary")
        st.write(commentary)

        # PDF download
        pdf_file = generate_pdf(commentary)
        with open(pdf_file, "rb") as f:
            st.download_button("Download Report", f, file_name="commentary.pdf")