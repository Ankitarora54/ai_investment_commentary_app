import streamlit as st
import pandas as pd
from utils.commentary import generate_commentary

st.title("AI Investment Commentary Generator")

uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview Data", df.head())

    if st.button("Generate Commentary"):
        commentary = generate_commentary(df)
        st.subheader("Generated Commentary")
        st.write(commentary)
