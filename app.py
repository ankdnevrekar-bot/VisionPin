import streamlit as st
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="VisionPin AI", layout="wide")

# 2. ML Function: Resampling Method
def get_dominant_color(pil_img):
    # This shrinks the whole image into 1 pixel to get the average color
    img = pil_img.convert("RGB").resize((1, 1), resample=Image.Resampling.BILINEAR)
    return img.getpixel((0, 0))

# 3. UI Header
st.title("🎀 VisionPin AI")
st.write("Upload a photo and let the AI match the vibe.")

# 4. App Logic
uploaded_files = st.file_uploader("Upload your Pins", accept_multiple_files=True)

if uploaded_files:
    # Analyze the first photo
    first_img = Image.open(uploaded_files[0])
    r, g, b = get_dominant_color(first_img)
    hex_color = '#%02x%02x%02x' % (r, g, b)
    
    # Change the background color dynamically
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {hex_color}55; }} 
        </style>
        """, unsafe_allow_html=True)
    
    st.info(f"✨ AI Aesthetic Match: {hex_color}")
    
    # Show the grid
    cols = st.columns(3)
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i % 3].image(img, use_column_width=True)
else:
    st.write("Waiting for your first pin...")
    
