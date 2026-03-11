import streamlit as st
import streamlit.components.v1 as components

# Configura a página do Streamlit para ocupar a tela toda
st.set_page_config(page_title="Creche da Vi", layout="wide")

# Lê o seu HTML e exibe ele dentro do Streamlit
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_data = f.read()
    components.html(html_data, height=1500, scrolling=True)
except FileNotFoundError:
    st.error("Arquivo index.html não encontrado!")
