import time
import streamlit as st


# =========================
# 🔐 CONFIG (Secrets)
# =========================
def _get_secret(name: str) -> str:
    return str(st.secrets.get(name, "")).strip()


APP_PASSWORD = _get_secret("APP_PASSWORD")          # required
ADMIN_PASSWORD = _get_secret("ADMIN_PASSWORD")      # optional (admin mode)

# Brute-force protection
MAX_ATTEMPTS = int(st.secrets.get("MAX_ATTEMPTS", 5))
LOCK_SECONDS = int(st.secrets.get("LOCK_SECONDS", 300))  # 5 minutes


# =========================
# 🧠 SESSION KEYS
# =========================
AUTH_OK_KEY = "auth_ok"
IS_ADMIN_KEY = "is_admin"
ATTEMPTS_KEY = "auth_attempts"
LOCK_UNTIL_KEY = "auth_lock_until"


def _init_auth_state():
    if AUTH_OK_KEY not in st.session_state:
        st.session_state[AUTH_OK_KEY] = False
    if IS_ADMIN_KEY not in st.session_state:
        st.session_state[IS_ADMIN_KEY] = False
    if ATTEMPTS_KEY not in st.session_state:
        st.session_state[ATTEMPTS_KEY] = 0
    if LOCK_UNTIL_KEY not in st.session_state:
        st.session_state[LOCK_UNTIL_KEY] = 0.0


def logout():
    st.session_state[AUTH_OK_KEY] = False
    st.session_state[IS_ADMIN_KEY] = False
    st.session_state[ATTEMPTS_KEY] = 0
    st.session_state[LOCK_UNTIL_KEY] = 0.0
    st.rerun()


def admin_badge():
    if st.session_state.get(IS_ADMIN_KEY, False):
        st.sidebar.success("🛡️ Admin mode")


def show_logout_button(key: str = "logout_btn"):
    # Μόνο αν είναι logged-in
    if st.session_state.get(AUTH_OK_KEY, False):
        if st.sidebar.button("🚪 Logout", key=key):
            logout()


# Backwards-compatible alias (αν κάπου έχεις `show_logout()`)
def show_logout(key: str = "logout_btn"):
    show_logout_button(key=key)


def require_login(app_name: str = "Private App", *, attempts_key_suffix: str = ""):
    """
    Call this near the TOP of every page (Home/app + each pages/*).
    - 1 φορά login (κρατάει session όσο είναι ανοιχτό το tab)
    - Too many attempts lock
    - Admin mode (optional)
    """

    _init_auth_state()

    if not APP_PASSWORD:
        st.error("❌ Missing APP_PASSWORD in Streamlit Secrets")
        st.stop()

    # If already logged in → allow
    if st.session_state.get(AUTH_OK_KEY, False):
        return

    now = time.time()
    locked_until = float(st.session_state.get(LOCK_UNTIL_KEY, 0.0))
    if now < locked_until:
        remaining = int(locked_until - now)
        st.title(f"🔒 {app_name} – Private Access")
        st.error(f"Too many attempts. Try again in {remaining} seconds.")
        st.stop()

    # Login UI
    st.title(f"🔒 {app_name} – Private Access")
    st.caption("This app is private. Please enter the password to continue.")

    pw = st.text_input("Password", type="password", key=f"pw_input{attempts_key_suffix}")
    col1, col2 = st.columns([1, 2])
    with col1:
        login_clicked = st.button("Login", type="primary", key=f"login_btn{attempts_key_suffix}")
    with col2:
        st.write("")

    if login_clicked:
        ok_user = (pw == APP_PASSWORD)
        ok_admin = (ADMIN_PASSWORD and pw == ADMIN_PASSWORD)

        if ok_user or ok_admin:
            st.session_state[AUTH_OK_KEY] = True
            st.session_state[IS_ADMIN_KEY] = bool(ok_admin)
            st.session_state[ATTEMPTS_KEY] = 0
            st.session_state[LOCK_UNTIL_KEY] = 0.0
            st.success("✅ Access granted")
            st.rerun()
        else:
            st.session_state[ATTEMPTS_KEY] += 1
            left = MAX_ATTEMPTS - st.session_state[ATTEMPTS_KEY]
            st.error("❌ Wrong password")

            if left <= 0:
                st.session_state[LOCK_UNTIL_KEY] = time.time() + LOCK_SECONDS
                st.session_state[ATTEMPTS_KEY] = 0
                st.warning(f"Locked for {LOCK_SECONDS} seconds.")
                st.stop()
            else:
                st.warning(f"Attempts left: {left}")

    st.stop()
