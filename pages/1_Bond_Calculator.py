import streamlit as st
from auth import require_login, show_logout
import streamlit.components.v1 as components

# ✅ Page config ΜΟΝΟ ΜΙΑ ΦΟΡΑ
st.set_page_config(
    page_title="Bond Calculator",
    layout="wide"
)

# 🔐 Login Protection
require_login("Finance Suite")
show_logout()

# ✅ Page Content
st.title("📊 Υπολογιστής Ομολόγων Pro")

with open("bond_calculator.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1000, scrolling=True)
