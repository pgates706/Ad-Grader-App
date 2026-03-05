import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pandas as pd
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Agency Ad-Grader AI", layout="wide")
st.title("🎯 Agency Ad-Grader for GDN")
st.sidebar.header("Creative History")

# Initialize Session State for history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- MOCK AI LOGIC (To be replaced with API calls) ---
def grade_creative(image):
    # In a live app, you'd send the image to Gemini/GPT-Vision here.
    # We are simulating the AI's "Thought Process":
    score_data = {
        "Grade": "B-",
        "Contrast": "Low (CTA blends with background)",
        "Text_Density": "15% (Optimal)",
        "OCR_Readability": "High",
        "Suggestions": [
            "Increase contrast on the 'Shop Now' button.",
            "Add a brand logo in the top-left corner for trust signals.",
            "The headline font is too thin for mobile users."
        ]
    }
    return score_data

def auto_fix_creative(image):
    # This would call an Inpainting/Generative AI API to modify the image.
    # For this demo, we'll simulate a 'Visual Pop' enhancement.
    enhancer = ImageEnhance.Contrast(image)
    fixed_img = enhancer.enhance(1.5)
    return fixed_img

# --- UI LAYOUT ---
uploaded_file = st.file_uploader("Upload your Display Ad (JPG/PNG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Creative")
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        if st.button("Grade My Ad"):
            with st.spinner('AI is analyzing GDN compliance...'):
                time.sleep(2) # Simulating API latency
                results = grade_creative(img)
                st.session_state['current_results'] = results
                # Save to history
                st.session_state['history'].append({"name": uploaded_file.name, "grade": results['Grade']})

    if 'current_results' in st.session_state:
        with col2:
            res = st.session_state['current_results']
            st.subheader(f"AI Grade: {res['Grade']}")
            
            # Display Metrics
            st.write(f"**Text Density:** {res['Text_Density']}")
            st.write(f"**Readability:** {res['OCR_Readability']}")
            
            st.info("**Improvement Suggestions:**")
            for sug in res['Suggestions']:
                st.write(f"- {sug}")

            if st.button("✨ Auto-Fix My Creative"):
                with st.spinner('Applying AI Improvements...'):
                    fixed_img = auto_fix_creative(img)
                    st.subheader("Optimized Creative")
                    st.image(fixed_img, use_container_width=True)
                    
                    # Download Link
                    st.download_button(label="Download Optimized Ad", 
                                       data=uploaded_file, # Replace with fixed_img bytes in production
                                       file_name="optimized_ad.png")

# --- SIDEBAR HISTORY ---
for item in st.session_state['history']:
    st.sidebar.write(f"📄 {item['name']} - **Grade: {item['grade']}**")
