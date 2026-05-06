import streamlit as st
from PIL import Image

# 1. Setup the Aesthetic (Pink/Pinterest Vibe)
st.set_page_config(page_title="VisionPin", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFF0F5; }
    h1 { color: #D87093; font-family: 'Helvetica'; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 VisionPin")
st.subheader("Your AI Aesthetic Moodboard")

# 2. Sidebar for Controls
st.sidebar.header("Board Settings")
bg_color = st.sidebar.color_picker("Pick a Background Color", "#FFF0F5")

# 3. File Uploader (The 'Pins')
uploaded_files = st.file_uploader("Upload photos to pin", accept_multiple_files=True)

if uploaded_files:
    # Create a Pinterest-style grid
    cols = st.columns(3) 
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        # Use the column logic to 'pin' them
        cols[i % 3].image(img, use_column_width=True, caption=f"Pin {i+1}")
        
st.write("---")
st.caption("Next step: Adding Machine Learning Color Analysis...")
