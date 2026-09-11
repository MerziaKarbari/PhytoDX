# frontend/app.py
# PhytoDx - Plant Disease Detection with AI

import streamlit as st
from PIL import Image
import requests
import os
import sys

# Add ai_model to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai_model'))
from predict import PlantDiseasePredictor

# ---------- API URL ----------
API_URL = "http://localhost:5000"

# ---------- SESSION STATE ----------
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PhytoDx - Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# ---------- LOAD AI MODEL ----------
@st.cache_resource
def load_model():
    """Load the trained AI model"""
    try:
        predictor = PlantDiseasePredictor()
        return predictor
    except Exception as e:
        st.error(f"❌ Failed to load AI model: {e}")
        return None

# Load model
predictor = load_model()

# Show model status in sidebar
if predictor is not None and predictor.model is not None:
    st.sidebar.success("✅ AI Model Loaded!")
else:
    st.sidebar.error("❌ AI Model Failed to Load!")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #c8ebc7;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full screen */
    .main {
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0 !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
    }
    
    /* ----- TITLE ----- */
    .title-container {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #1a3a1a, #2d5a2d);
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    
    .title {
        font-family: 'Georgia', 'Times New Roman', cursive;
        font-size: 4.5rem;
        color: #ffffff;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
        font-style: italic;
        font-weight: bold;
    }
    
    .subtitle {
        font-family: 'Georgia', 'Times New Roman', cursive;
        font-size: 1.8rem;
        color: #c8ebc7;
        margin-top: -0.3rem;
        font-style: italic;
    }
    
    /* ----- NAVIGATION BUTTONS ----- */
    .stButton > button {
        background: #3d6b3d !important;
        color: white !important;
        border: none !important;
        padding: 0.7rem 1.2rem !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s !important;
        width: 100% !important;
        min-width: 120px !important;
        height: 50px !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        background: #4d8a4d !important;
    }
    
    /* ----- WELCOME CARD ----- */
    .welcome-card {
        background: rgba(255,255,255,0.95);
        padding: 2.5rem 3rem;
        border-radius: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        max-width: 800px;
        margin: 1rem auto;
    }
    
    .welcome-card h1 {
        color: #1a3a1a;
        font-size: 3rem;
        margin: 0 0 0.5rem 0;
    }
    
    .welcome-card p {
        color: #2d4a2d;
        font-size: 1.4rem;
        opacity: 0.8;
        margin: 0.5rem 0 1.5rem 0;
    }
    
    /* ----- PAGE CARDS ----- */
    .page-card {
        background: rgba(255,255,255,0.95);
        padding: 2rem 2.5rem;
        border-radius: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 0.8rem 0;
    }
    
    .page-card h2 {
        color: #1a3a1a;
        margin-top: 0;
        font-size: 2.5rem;
    }
    
    .page-card p {
        color: #2d4a2d;
        font-size: 1.2rem;
    }
    
    .page-card li {
        color: #2d4a2d;
        font-size: 1.1rem;
        margin: 0.4rem 0;
    }
    
    .page-card h3 {
        color: #1a3a1a;
        font-size: 1.5rem;
    }
    
    /* ----- RESULT BOX ----- */
    .result-box {
        background: rgba(255,255,255,0.85);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        border-left: 5px solid #2d4a2d;
        margin: 0.8rem 0;
    }
    
    .result-box h3 {
        color: #1a3a1a;
        margin: 0 0 0.5rem 0;
        font-size: 1.8rem;
    }
    
    .result-box p {
        color: #2d4a2d;
        font-size: 1.2rem;
        margin: 0.3rem 0;
    }
    
    .result-box .confidence {
        color: #1a3a1a;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    /* ----- DISCLAIMER ----- */
    .disclaimer {
        background: rgba(255,248,225,0.95);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1rem auto;
        font-size: 1.1rem;
        color: #2d4a2d;
        max-width: 800px;
        text-align: center;
    }
    
    /* ----- FOOTER ----- */
    .footer {
        text-align: center;
        padding: 0.8rem;
        background: #2d4a2d;
        border-radius: 15px;
        color: #c8ebc7;
        font-size: 1.1rem;
        margin-top: 1rem;
    }
    
    .footer span {
        color: #ffffff;
    }
    
    /* ----- FORM INPUTS ----- */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.95);
        border: 2px solid #c8ebc7;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        color: #1a3a1a;
        font-size: 1.1rem;
        height: 50px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2d4a2d;
        box-shadow: 0 0 0 2px rgba(45, 74, 45, 0.2);
    }
    
    .stTextInput label {
        color: #1a3a1a !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* ----- FILE UPLOADER ----- */
    .stFileUploader {
        background: transparent;
        border-radius: 15px;
    }
    
    .stFileUploader label {
        color: #1a3a1a !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }
    
    .stFileUploader > div > div {
        background: rgba(255,255,255,0.9) !important;
        border: 2px dashed #2d4a2d !important;
        border-radius: 15px !important;
        color: #1a3a1a !important;
        padding: 2rem !important;
        font-size: 1.1rem !important;
    }
    
    /* ----- ALERT BOXES ----- */
    .stAlert {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        color: #1a3a1a !important;
        padding: 1rem 1.5rem !important;
    }
    
    .stAlert svg {
        color: #2d4a2d !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* ----- SCAN BUTTON ----- */
    .scan-btn > button {
        background: #1a3a1a !important;
        color: white !important;
        border: none !important;
        padding: 1rem 4rem !important;
        border-radius: 35px !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        transition: all 0.3s !important;
        width: 100% !important;
        height: 65px !important;
    }
    
    .scan-btn > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
        background: #2d5a2d !important;
    }
    
    /* ----- IMAGE ----- */
    .stImage {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .stImage figcaption {
        color: #1a3a1a !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* ----- LINKS ----- */
    a {
        color: #2d4a2d !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        font-size: 1.1rem !important;
    }
    
    a:hover {
        text-decoration: underline !important;
        color: #1a3a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("""
<div class="title-container">
    <div class="title">🌿 PhytoDx</div>
    <div class="subtitle">Plant Disease Detection</div>
</div>
""", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
def nav_button(label, page_name):
    if st.button(label, key=page_name):
        st.session_state.page = page_name
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "Home"
    st.rerun()

# Navigation - 7 equal columns
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    nav_button("🏠 Home", "Home")
with col2:
    nav_button("📷 Scan", "Scan")
with col3:
    nav_button("📊 History", "History")
with col4:
    nav_button("ℹ️ About", "About")

# Show Login/Register or Profile/Logout based on login status
if st.session_state.logged_in:
    with col5:
        nav_button("👤 Profile", "Profile")
    with col6:
        if st.button("🚪 Logout"):
            logout()
else:
    with col5:
        nav_button("🔐 Login", "Login")
    with col6:
        nav_button("📝 Register", "Register")

# ---------- PAGE CONTENT ----------

# ==================== HOME PAGE ====================
if st.session_state.page == "Home":
    st.markdown("""
    <div class="welcome-card">
        <h1>🌿 Welcome to PhytoDx</h1>
        <p>AI-powered plant disease detection and treatment recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
        if st.button("📷 Start New Scan", key="scan_btn", use_container_width=True):
            st.session_state.page = "Scan"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Disclaimer:</strong> This is an AI-based preliminary prediction tool. 
        Always consult a professional agricultural expert for accurate diagnosis.
    </div>
    """, unsafe_allow_html=True)

# ==================== SCAN PAGE ====================
elif st.session_state.page == "Scan":
    st.markdown("""
    <div class="page-card">
        <h2>📷 Scan Leaf</h2>
        <p>Upload or capture a photo of a plant leaf to detect diseases.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------- TWO OPTIONS: UPLOAD OR CAPTURE ----------
    option = st.radio(
        "Choose input method:",
        ["📁 Upload Image", "📸 Capture from Camera"],
        horizontal=True
    )
    
    image = None
    
    if option == "📁 Upload Image":
        uploaded_file = st.file_uploader(
            "Choose a leaf image...",
            type=["jpg", "jpeg", "png"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    
    else:  # Capture from Camera
        camera_image = st.camera_input("📸 Capture a leaf image")
        if camera_image is not None:
            image = Image.open(camera_image)
    
    # ---------- PROCESS IMAGE ----------
    if image is not None:
        st.image(image, caption="Uploaded Leaf", width=400)
        
        if st.button("🔍 Analyze", use_container_width=True):
            if predictor is not None and predictor.model is not None:
                with st.spinner("🧠 AI is analyzing the image..."):
                    try:
                        predicted_class, confidence = predictor.predict(image)
                        
                        # ----- GET DISEASE INFO FROM BACKEND -----
                        disease_info = None
                        try:
                            response = requests.get(
                                f"{API_URL}/api/disease/{predicted_class}"
                            )
                            result = response.json()
                            if result.get('success'):
                                disease_info = result.get('disease')
                        except:
                            pass
                        
                        # ----- DISPLAY RESULT WITH DISEASE INFO -----
                        if disease_info:
                            disease = disease_info.get('disease', {})
                            treatment = disease_info.get('treatment', {})
                            
                            st.markdown(f"""
                            <div class="result-box">
                                <h3>🌿 {predicted_class}</h3>
                                <p><span class="confidence">Confidence: {confidence:.2f}%</span></p>
                                <p><strong>Symptoms:</strong> {disease.get('symptoms', 'Information not available')}</p>
                                <p><strong>Cause:</strong> {disease.get('cause', 'Information not available')}</p>
                                <p><strong>Treatment:</strong> {treatment.get('treatment', 'Information not available') if treatment else 'Information not available'}</p>
                                <p><strong>Prevention:</strong> {treatment.get('prevention', 'Information not available') if treatment else 'Information not available'}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-box">
                                <h3>🌿 {predicted_class}</h3>
                                <p><span class="confidence">Confidence: {confidence:.2f}%</span></p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.info("ℹ️ Detailed disease information coming soon!")
                        
                        # ----- SAVE TO HISTORY -----
                        if st.session_state.logged_in:
                            try:
                                save_response = requests.post(
                                    f"{API_URL}/api/save_scan",
                                    json={
                                        "user_id": st.session_state.user['user_id'],
                                        "disease_name": predicted_class,
                                        "confidence": confidence,
                                        "image_path": "captured_image"
                                    }
                                )
                                if save_response.status_code == 200:
                                    st.success("✅ Scan saved to history!")
                            except Exception as e:
                                st.warning(f"⚠️ Could not save scan: {e}")
                        else:
                            st.info("💡 Login to save scan history!")
                        
                        if confidence < 60:
                            st.warning("⚠️ Low confidence prediction. Please upload a clearer image.")
                        
                    except Exception as e:
                        st.error(f"❌ Error during prediction: {e}")
            else:
                st.error("❌ AI model not loaded. Please check if model file exists.")

# ==================== HISTORY PAGE ====================
elif st.session_state.page == "History":
    st.markdown("""
    <div class="page-card">
        <h2>📊 Scan History</h2>
        <p>View your previous scans and results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        st.warning("🔐 Please login to view your scan history.")
    else:
        try:
            response = requests.get(
                f"{API_URL}/api/get_scans/{st.session_state.user['user_id']}"
            )
            result = response.json()
            
            if result.get("success") and result.get("scans"):
                scans = result["scans"]
                for scan in scans:
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>🌿 {scan.get('disease_name', 'Unknown Disease')}</h3>
                        <p><strong>Confidence:</strong> {scan.get('confidence_score', 'N/A')}%</p>
                        <p><strong>Date:</strong> {scan.get('scan_date', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📭 No scan history yet. Start your first scan from the Scan page!")
        except Exception as e:
            st.error(f"❌ Could not fetch scan history: {e}")

# ==================== ABOUT PAGE ====================
elif st.session_state.page == "About":
    st.markdown("""
    <div class="page-card">
        <h2>ℹ️ About PhytoDx</h2>
        <p><strong>PhytoDx</strong> is an AI-based plant disease detection application.</p>
        <p>It helps farmers, gardeners, and plant enthusiasts identify diseases from leaf images.</p>
        <br>
        <h3>🛠️ Technology Stack</h3>
        <ul>
            <li><strong>Frontend:</strong> Streamlit</li>
            <li><strong>Backend:</strong> Flask</li>
            <li><strong>Database:</strong> MySQL</li>
            <li><strong>AI:</strong> TensorFlow / Keras</li>
            <li><strong>Dataset:</strong> PlantDoc</li>
        </ul>
        <br>
        <h3>👥 Target Users</h3>
        <ul>
            <li>Farmers</li>
            <li>Gardeners</li>
            <li>Plant Growers</li>
            <li>Students & Learners</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== LOGIN PAGE ====================
elif st.session_state.page == "Login":
    st.markdown("""
    <div class="page-card" style="max-width: 500px; margin: 0 auto;">
        <h2>🔐 Login</h2>
        <p>Welcome back! Login to your account.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            if st.button("Login", use_container_width=True):
                if email and password:
                    try:
                        response = requests.post(
                            f"{API_URL}/api/login",
                            json={"email": email, "password": password}
                        )
                        result = response.json()
                        if result.get("success"):
                            st.success(f"✅ Welcome {result['user']['name']}!")
                            st.session_state.logged_in = True
                            st.session_state.user = result['user']
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('message', 'Login failed')}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please fill all fields")
            
            st.markdown("""
            <p style="text-align:center; color:#1a3a1a; margin-top:1rem; font-size:1.1rem;">
                Don't have an account? <a href="#" style="color:#2d4a2d; font-weight:600;">Register</a>
            </p>
            """, unsafe_allow_html=True)

# ==================== REGISTER PAGE ====================
elif st.session_state.page == "Register":
    st.markdown("""
    <div class="page-card" style="max-width: 500px; margin: 0 auto;">
        <h2>📝 Register</h2>
        <p>Create your account to get started.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            name = st.text_input("Full Name", placeholder="Your name")
            email = st.text_input("Email", placeholder="your@email.com")
            phone = st.text_input("Phone (optional)", placeholder="Phone number")
            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            
            if st.button("Register", use_container_width=True):
                if name and email and password and confirm:
                    if password != confirm:
                        st.warning("⚠️ Passwords do not match")
                    else:
                        try:
                            response = requests.post(
                                f"{API_URL}/api/register",
                                json={"name": name, "email": email, "password": password, "phone": phone}
                            )
                            result = response.json()
                            if result.get("success"):
                                st.success("✅ Registration successful! Please login.")
                                st.session_state.page = "Login"
                                st.rerun()
                            else:
                                st.error(f"❌ {result.get('message', 'Registration failed')}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please fill all required fields")
            
            st.markdown("""
            <p style="text-align:center; color:#1a3a1a; margin-top:1rem; font-size:1.1rem;">
                Already have an account? <a href="#" style="color:#2d4a2d; font-weight:600;">Login</a>
            </p>
            """, unsafe_allow_html=True)

# ==================== PROFILE PAGE ====================
elif st.session_state.page == "Profile":
    if not st.session_state.logged_in:
        st.warning("🔐 Please login to view your profile.")
        if st.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()
    else:
        user = st.session_state.user
        st.markdown("""
        <div class="page-card">
            <h2>👤 My Profile</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Name", value=user.get('name', ''), disabled=True)
            st.text_input("Email", value=user.get('email', ''), disabled=True)
        with col2:
            st.text_input("Phone", value=user.get('phone', 'Not provided'), disabled=True)
            st.text_input("Member Since", value=user.get('created_at', 'N/A'), disabled=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    🌿 <span>PhytoDx</span> - Plant Disease Detection | Made with ❤️
</div>
""", unsafe_allow_html=True)