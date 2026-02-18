from auth import require_login, show_logout
require_login("Finance Suite")
show_logout()

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bond Calculator", layout="wide")
st.title("📊 Υπολογιστής Ομολόγων Pro")

with open("bond_calculator.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1000, scrolling=True)
