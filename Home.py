import streamlit as st
from auth import require_login, show_logout_button, admin_badge
st.set_page_config(page_title="Finance Suite Pro", layout="wide")
require_login("Finance Suite")
admin_badge()
show_logout_button(key="logout_home")

st.title("💼 Finance Suite")
st.markdown("""
Καλώς ήρθες στο προσωπικό σου Finance Hub.

### Διαθέσιμα εργαλεία:
✅ Bond Calculator Pro  
✅ Leasing Buyout Analyzer  
✅ Leasing vs Buy (με Δάνειο)

➡️ Επίλεξε εργαλείο από το menu αριστερά.
""")




