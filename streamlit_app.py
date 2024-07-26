import streamlit as st
from PIL import Image
import numpy as np
from enhancer.enhancer import Enhancer

st.header('Image Enhancer App')
st.divider()

image_path = st.file_uploader("Choose file: ", type=['.png', '.jpg', '.jpeg'])

# app settings
st.sidebar.header("App Settings:")
method = st.sidebar.selectbox("Method:", ["gfpgan", "RestoreFormer", "codeformer"])
background_enhancement = st.sidebar.selectbox("Background enhancement:", ["True", "False"])
background_enhancement = True if background_enhancement == "True" else False
upscale = st.sidebar.selectbox("Upscale enhancement:", [2, 4])
picture_width = st.sidebar.slider('Picture Width', min_value=100, max_value=500)

if image_path is not None:
     
    # Create enhancer
    enhancer = Enhancer(method=method, background_enhancement=background_enhancement, upscale=2)
    image = np.array(Image.open(image_path))
    restored_image = enhancer.enhance(image)
    
    # enhanced image
    final_image = Image.fromarray(restored_image)
    
    # display code: 2 column view
    col1, col2 = st.columns(2)

    with col1:
        st.header("Input Image")
        st.image(image_path, width=picture_width)
    with col2:
        st.header("Enhanced Image")
        st.image(final_image, width=picture_width)