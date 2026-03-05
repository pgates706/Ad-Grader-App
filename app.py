import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup the "Brain"
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("AIzaSyA_Dl2niG8kAGk2v0lG6h7pngKhn-ccGgM", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash') # The Vision Model

def get_real_ai_grade(image):
    prompt = """
    Act as a Google Display Network (GDN) Ad Exchange AI. 
    Analyze this ad creative and provide:
    1. A Grade (A, B, C, D, or F).
    2. Assessment of Contrast, Text Density, and OCR Readability.
    3. Three specific, technical suggestions to improve its performance in an ad auction.
    Return the response in a clear, professional format.
    """
    # This sends the actual image to the AI
    response = model.generate_content([prompt, image])
    return response.text

# 2. Update your UI Logic
uploaded_file = st.file_uploader("Upload Ad", type=['png', 'jpg'])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    st.image(img, caption="Analyzing...")
    
    if st.button("Get Real AI Grade"):
        with st.spinner("AI is actually looking at your pixels now..."):
            report = get_real_ai_grade(img)
            st.markdown(report)
elif uploaded_file and not api_key:
    st.warning("Please enter an API Key in the sidebar to start real grading!")
