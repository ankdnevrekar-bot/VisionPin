import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
from transformers import BlipProcessor, BlipForConditionalGeneration
import numpy as np

# 1. AI Models & Setup
@st.cache_resource
def load_models():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_models()

st.set_page_config(page_title="VisionPin Studio", layout="wide")

# 2. The Aesthetic Engine
def get_dominant_color(pil_img):
    img = pil_img.convert("RGB").resize((1, 1), resample=Image.Resampling.BILINEAR)
    return img.getpixel((0, 0))

st.title("🎀 VisionPin Creative Studio")

# 3. Sidebar: Aesthetic Filters
st.sidebar.header("🎨 Aesthetic Filters")
filter_type = st.sidebar.selectbox("Choose a Vibe", ["None", "Soft Pink", "Retro Sepia", "High Contrast"])
brightness = st.sidebar.slider("Brightness", 0.5, 1.5, 1.0)

# 4. Main App Logic
uploaded_files = st.file_uploader("Upload your Pins", accept_multiple_files=True)

if uploaded_files:
    # Set the background based on the first image
    first_img = Image.open(uploaded_files[0])
    r, g, b = get_dominant_color(first_img)
    hex_color = '#%02x%02x%02x' % (r, g, b)
    st.markdown(f"<style>.stApp {{ background-color: {hex_color}33; }}</style>", unsafe_allow_html=True)

    cols = st.columns(3)
    
    for i, file in enumerate(uploaded_files):
        img = Image.open(file).convert('RGB')
        
        # --- FEATURE 1: AI Auto-Caption ---
        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        
        # --- FEATURE 2: Aesthetic Filters ---
        if filter_type == "Soft Pink":
            # Adding a pink tint layer
            pink_overlay = Image.new('RGB', img.size, (255, 182, 193))
            img = Image.blend(img, pink_overlay, 0.2)
        elif filter_type == "Retro Sepia":
            img = ImageOps.colorize(ImageOps.grayscale(img), "#704214", "#C0A080")
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)

        # --- FEATURE 3: Pinterest Display ---
        with cols[i % 3]:
            st.image(img, use_column_width=True)
            st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 0 0 15px 15px; margin-top: -10px; margin-bottom: 25px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
                    <p style="color: #D87093; font-family: 'Helvetica'; font-size: 0.85em; margin: 0; line-height: 1.2;">
                        <b>AI Caption:</b> {caption.capitalize()}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
    # --- BONUS: Download Logic ---
    st.sidebar.success("✅ Studio Mode Active")
    st.sidebar.write("Right-click any image to save your aesthetic pin!")

else:
    st.info("Upload some photos to see the AI magic!")
    
