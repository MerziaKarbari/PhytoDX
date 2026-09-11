import streamlit as st

st.set_page_config(page_title="PhotoDx - Login", page_icon="🌿", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Hide Streamlit's default header bar */
    header[data-testid="stHeader"] {
        background-color: #eaf7e8;
        box-shadow: none;
    }

    .stApp {
        background-color: #eaf7e8;
    }

    /* Center the card vertically and horizontally */
    .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100vh;
        max-width: 460px;
        margin: 0 auto;
        background-color: #ffffff;
        border-radius: 16px;
        padding: 2.5rem 2rem !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        border: 1px solid #d8f0d4;
    }

    .app-title {
        text-align: center;
        color: #2d6a4f;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 1.8rem;
    }

    .stTextInput > div > div > input {
        background-color: #f8faf7;
        color: #1b1b1b;
        border: 1.5px solid #cfe8c9;
        border-radius: 10px;
    }

    .stTextInput > div > div > input:focus {
        border: 1.5px solid #52b788;
    }

    .stButton > button {
        width: 100%;
        background-color: #52b788;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem;
        font-weight: 700;
        font-size: 1rem;
        margin-top: 0.5rem;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #40916c;
        transform: scale(1.02);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        justify-content: center;
    }

    /* Fix low-contrast inactive tab text */
    .stTabs [data-baseweb="tab"] {
        color: #40916c;
        font-weight: 700;
        font-size: 1.05rem;
    }

    .stTabs [aria-selected="true"] {
        color: #2d6a4f !important;
    }

    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- PAGE CONTENT ----------------
st.markdown('<div class="app-title">🌿 PhotoDx</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Plant Disease Detection & Treatment Recommendation</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN TAB ----------------
with tab1:
    login_email = st.text_input("Email", key="login_email", placeholder="you@example.com")
    login_password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")

    if st.button("Login", key="login_button"):
        if login_email == "" or login_password == "":
            st.warning("Please fill in both email and password.")
        else:
            st.success(f"Login attempt received for: {login_email}")
            st.info("Backend authentication not connected yet.")

# ---------------- REGISTER TAB ----------------
with tab2:
    reg_name = st.text_input("Full Name", key="reg_name", placeholder="John Doe")
    reg_email = st.text_input("Email", key="reg_email", placeholder="you@example.com")
    reg_phone = st.text_input("Phone Number", key="reg_phone", placeholder="+91 XXXXX XXXXX")
    reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="••••••••")
    reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password", placeholder="••••••••")

    if st.button("Register", key="register_button"):
        if not reg_name or not reg_email or not reg_phone or not reg_password or not reg_confirm_password:
            st.warning("Please fill in all fields.")
        elif reg_password != reg_confirm_password:
            st.error("Passwords do not match.")
        else:
            st.success(f"Registration attempt received for: {reg_name}")
            st.info("Backend registration not connected yet.")