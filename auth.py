import time
import hmac
import streamlit as st

def _secret_str(key: str, default: str = "") -> str:
    return str(st.secrets.get(key, default)).strip()


def _secret_int(key: str, default: int) -> int:
    try:
        return int(st.secrets.get(key, default))
    except Exception:
        return default


def logout():
    st.session_state["auth_ok"] = False
    st.session_state["is_admin"] = False
    st.session_state.pop("auth_ok", None)
    st.session_state.pop("is_admin", None)
    st.rerun()


def show_logout_button(key: str = "logout_btn"):
    # key για να μην “σκάει” StreamlitDuplicateElementId σε διαφορετικά pages
    if st.sidebar.button("🚪 Logout", key=key):
        logout()


def require_login(app_name: str = "Private App"):
    """
    Call at the TOP of app.py/Home.py and at the TOP of every page in /pages.
    Remembers login across pages (same browser session).
    Has lockout after too many failed attempts.
    Sets admin mode if ADMIN_PASSWORD matches.
    """

    APP_PW = _secret_str("APP_PASSWORD", "")
    ADMIN_PW = _secret_str("ADMIN_PASSWORD", "")

    if not APP_PW:
        st.error("❌ Missing APP_PASSWORD in Secrets")
        st.stop()

    max_attempts = _secret_int("MAX_LOGIN_ATTEMPTS", 5)
    lock_minutes = _secret_int("LOCKOUT_MINUTES", 15)

    # Session defaults
    st.session_state.setdefault("auth_ok", False)
    st.session_state.setdefault("is_admin", False)
    st.session_state.setdefault("failed_attempts", 0)
    st.session_state.setdefault("lock_until", 0.0)

    # Already logged in
    if st.session_state["auth_ok"]:
        return

    # Lockout check
    now = time.time()
    if now < float(st.session_state["lock_until"]):
        remaining = int(st.session_state["lock_until"] - now)
        st.error(f"🔒 Too many attempts. Try again in {remaining} seconds.")
        st.stop()

    # Login UI
    st.title("🔒 Private Access")
    st.caption(f"{app_name} is password protected.")
    pw = st.text_input("Enter password", type="password")

    col1, col2 = st.columns([1, 2])
    with col1:
        login = st.button("Login", type="primary")
    with col2:
        st.write("")

    if login:
        # constant-time compare
        ok_user = hmac.compare_digest(pw, APP_PW)
        ok_admin = bool(ADMIN_PW) and hmac.compare_digest(pw, ADMIN_PW)

        if ok_user or ok_admin:
            st.session_state["auth_ok"] = True
            st.session_state["is_admin"] = bool(ok_admin)

            # reset security counters
            st.session_state["failed_attempts"] = 0
            st.session_state["lock_until"] = 0.0

            st.success("✅ Access granted")
            st.rerun()
        else:
            st.session_state["failed_attempts"] += 1
            left = max_attempts - st.session_state["failed_attempts"]

            if left <= 0:
                st.session_state["lock_until"] = time.time() + (lock_minutes * 60)
                st.session_state["failed_attempts"] = 0
                st.error(f"🔒 Locked for {lock_minutes} minutes.")
            else:
                st.error(f"❌ Wrong password. Attempts left: {left}")

    st.stop()


def admin_badge():
    if st.session_state.get("is_admin"):
        st.sidebar.success("🛡️ Admin mode")
    else:
        st.sidebar.info("👤 User mode")
