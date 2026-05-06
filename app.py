import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="VisionPin AI", layout="wide")

# --- ML FUNCTION: Find the dominant color ---
def get_dominant_color(pil_img):
    img = pil_img.copy().resize((50, 50)) # Resize for speed
    ar = np.asarray(img)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2])
    
    kmeans = KMeans(n_clusters=1).fit(ar) # Find 1 main cluster
    return kmeans.cluster_centers_[0]

st.title("🎀 VisionPin AI")
uploaded_files = st.file_uploader("Upload an aesthetic photo", accept_multiple_files=True)

if uploaded_files:
    # Use the first photo to set the mood
    first_img = Image.open(uploaded_files[0])
    dom_color = get_dominant_color(first_img)
    hex_color = '#%02x%02x%02x' % (int(dom_color[0]), int(dom_color[1]), int(dom_color[2]))
    
    # Apply the ML color to the background
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {hex_color}55; }} /* 55 is for transparency */
        </style>
        """, unsafe_allow_html=True)
    
    st.write(f"### 🤖 AI detected palette: {hex_color}")
    
    cols = st.columns(3)
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i % 3].image(img, use_column_width=True)

st.sidebar.info("The AI analyzes your image pixels to find the perfect background match.")
