import streamlit as st

st.title("Test Title")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.write("This is tab 1")

with tab2:
    st.write("This is tab 2")