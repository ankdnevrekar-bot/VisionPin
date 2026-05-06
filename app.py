def get_dominant_color(pil_img):
    # 1. Convert to RGB and shrink for speed
    img = pil_img.convert("RGB").resize((1, 1), resample=Image.Resampling.BILINEAR)
    
    # 2. Get the single pixel color
    dominant_color = img.getpixel((0, 0))
    return dominant_color

# --- Rest of your code below ---
st.title("🎀 VisionPin AI")
uploaded_files = st.file_uploader("Upload an aesthetic photo", accept_multiple_files=True)

if uploaded_files:
    first_img = Image.open(uploaded_files[0])
    
    # Get the RGB values
    r, g, b = get_dominant_color(first_img)
    hex_color = '#%02x%02x%02x' % (r, g, b)
    
    # Apply the ML color to the background
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {hex_color}55; }} 
        </style>
        """, unsafe_allow_html=True)
    
    st.write(f"### 🤖 AI detected palette: {hex_color}")
    
    cols = st.columns(3)
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i % 3].image(img, use_column_width=True)
