import streamlit as st

def require_login(app_name="Finance Suite"):
    PASSWORD = st.secrets.get("APP_PASSWORD", "")

    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False

    if st.session_state.auth_ok:
        return

    st.title("🔒 Private Access")
    st.caption(f"{app_name} is password protected.")

    pw = st.text_input("Enter password", type="password")

    if st.button("Login"):
        if pw == PASSWORD:
            st.session_state.auth_ok = True
            st.success("✅ Access granted")
            st.rerun()
        else:
            st.error("❌ Wrong password")

    st.stop()


def show_logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.auth_ok = False
        st.rerun()
