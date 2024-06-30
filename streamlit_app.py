import streamlit as st

# Example with beta_expander in sidebar
with st.sidebar.beta_expander("View Charts"):
    st.write("Content inside the expander")
