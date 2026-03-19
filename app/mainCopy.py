import streamlit as st
import pandas as pd
from utils.commentary import generate_commentary
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("AI Investment Commentary Generator")

uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview Data", df.head())

    if st.button("Generate Commentary"):
        commentary = generate_commentary(df, client)
        st.subheader("Generated Commentary")
        st.write(commentary)
