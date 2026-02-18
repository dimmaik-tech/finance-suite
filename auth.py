import time
import streamlit as st

# ---- helpers ----
def _get_password() -> str:
    return str(st.secrets.get("APP_PASSWORD", "")).strip()

def _state_defaults():
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False
    if "auth_tries" not in st.session_state:
        st.session_state.auth_tries = 0
    if "auth_lock_until" not in st.session_state:
        st.session_state.auth_lock_until = 0

def logout():
    st.session_state.auth_ok = False

def show_logout(label="🚪 Logout"):
    # ΜΟΝΟ 1 φορά ανά page (όχι διπλά)
    if st.sidebar.button(label, key="logout_btn"):
        logout()
        st.rerun()

def require_login(app_name: str = "Private App", max_attempts: int = 6, lock_seconds: int = 120):
    """
    Βάλε το στην κορυφή ΚΑΘΕ file (Home.py και κάθε page).
    - 1 φορά login (κρατάει session)
    - Too many attempts protection (lockout)
    """
    _state_defaults()

    pw = _get_password()
    if not pw:
        st.error("❌ Missing APP_PASSWORD in Secrets (Streamlit → Manage app → Settings → Secrets)")
        st.stop()

    # lockout
    now = int(time.time())
    if st.session_state.auth_lock_until and now < st.session_state.auth_lock_until:
        remaining = st.session_state.auth_lock_until - now
        st.error(f"⛔ Too many attempts. Try again in {remaining}s.")
        st.stop()

    if st.session_state.auth_ok:
        return  # already logged in

    st.title(f"🔒 {app_name} – Private Access")
    st.caption("Enter password to continue.")
    entered = st.text_input("Password", type="password")

    c1, c2 = st.columns([1, 3])
    with c1:
        go = st.button("Login", type="primary")
    with c2:
        st.write("")

    if go:
        if entered == pw:
            st.session_state.auth_ok = True
            st.session_state.auth_tries = 0
            st.success("✅ Access granted")
            st.rerun()
        else:
            st.session_state.auth_tries += 1
            left = max_attempts - st.session_state.auth_tries
            st.error(f"❌ Wrong password. Attempts left: {left}")

            if st.session_state.auth_tries >= max_attempts:
                st.session_state.auth_lock_until = int(time.time()) + lock_seconds
                st.session_state.auth_tries = 0
                st.error(f"⛔ Locked for {lock_seconds}s")
        st.stop()
