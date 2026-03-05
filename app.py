import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Agency Ad-Grader AI", layout="wide")
st.title("🎯 Agency Ad-Grader for GDN")

# 1. Setup the Sidebar for API Key
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # We use gemini-2.5-flash as it is the current industry standard for speed/vision
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.sidebar.success("API Connected!")
    except Exception as e:
        st.sidebar.error(f"Connection Error: {e}")

# 2. Main App Logic
uploaded_file = st.file_uploader("Upload your Display Ad (JPG/PNG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file and api_key:
    col1, col2 = st.columns(2)
    img = Image.open(uploaded_file)
    
    with col1:
        st.subheader("Original Creative")
        st.image(img, use_container_width=True)
        
    if st.button("🚀 Grade My Ad"):
        with st.spinner('AI is performing Vision Analysis...'):
            try:
                prompt = """
                Act as a Google Display Network (GDN) Ad Exchange AI. 
                Analyze this ad creative and provide:
                1. A Letter Grade (A, B, C, D, or F).
                2. Technical assessment: Contrast, Text Density, and OCR Readability.
                3. Three specific, technical suggestions to improve its performance in an ad auction.
                Format the response using Markdown with bold headers.
                """
                # This line sends the prompt AND the image to the AI
                response = model.generate_content([prompt, img])
                
                with col2:
                    st.subheader("AI Analysis Report")
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.info("Tip: Ensure your API key has 'Generative Language API' enabled in Google AI Studio.")

elif not api_key:
    st.warning("👈 Please enter your API Key in the sidebar to begin.")
