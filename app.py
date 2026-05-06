import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. Load AI Models (This might take a minute the first time)
@st.cache_resource
def load_models():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_models()

# 2. Setup the "Aesthetic"
st.set_page_config(page_title="VisionPin Studio", layout="wide")

def get_dominant_color(pil_img):
    # This shrinks the image to 1 pixel to get the average RGB
    img = pil_img.convert("RGB").resize((1, 1), resample=Image.Resampling.BILINEAR)
    return img.getpixel((0, 0)) # Returns (R, G, B)

st.title("🎀 VisionPin Creative Studio")

# 3. Sidebar Design Controls
st.sidebar.header("🎨 Design Tools")
custom_text = st.sidebar.text_input("Add a Label to your Pins", "Aesthetic Vibe")
filter_type = st.sidebar.selectbox("Choose a Filter", ["None", "Soft Pink", "Retro Sepia"])
brightness = st.sidebar.slider("Brightness", 0.5, 1.5, 1.0)

# 4. The Main Engine
uploaded_files = st.file_uploader("Upload your photos", accept_multiple_files=True)

if uploaded_files:
    # Use first image to set the background
    first_img = Image.open(uploaded_files[0])
    r, g, b = get_dominant_color(first_img)
    hex_color = '#%02x%02x%02x' % (r, g, b)
    
    st.markdown(f"<style>.stApp {{ background-color: {hex_color}44; }}</style>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, file in enumerate(uploaded_files):
        img = Image.open(file).convert('RGB')
        
        # --- FEATURE: Text Overlay ---
        if custom_text:
            draw = ImageDraw.Draw(img)
            draw.text((15, 15), custom_text, fill="white")

        # --- FEATURE: AI Caption ---
        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        # --- FEATURE: Filters ---
        if filter_type == "Soft Pink":
            pink = Image.new('RGB', img.size, (255, 182, 193))
            img = Image.blend(img, pink, 0.2)
        elif filter_type == "Retro Sepia":
            img = ImageOps.colorize(ImageOps.grayscale(img), "#704214", "#C0A080")
        
        img = ImageEnhance.Brightness(img).enhance(brightness)

        with cols[i % 3]:
            st.image(img, use_column_width=True)
            st.markdown(f"""
                <div style="background-color: white; padding: 10px; border-radius: 0 0 10px 10px; margin-top: -10px; margin-bottom: 20px;">
                    <p style="color: #D87093; font-size: 0.8em; margin: 0;"><b>AI:</b> {caption}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Upload some photos to start your studio!")
    
