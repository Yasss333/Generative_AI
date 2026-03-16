import streamlit as st

st.title("Test App")

name = st.text_input("Enter name")

if st.button("Say Hello"):
    st.write("Hello", name)