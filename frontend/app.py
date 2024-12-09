import streamlit as st
from PIL import Image

# App Title
st.title("RunwayML Automation App")

# Image Upload Section
st.header("Upload Two Images")
uploaded_image1 = st.file_uploader("Choose the first image", type=["jpg", "jpeg", "png"])
uploaded_image2 = st.file_uploader("Choose the second image", type=["jpg", "jpeg", "png"])

# Display uploaded images
if uploaded_image1 and uploaded_image2:
    image1 = Image.open(uploaded_image1)
    image2 = Image.open(uploaded_image2)

    st.image(image1, caption="First Image", use_column_width=True)
    st.image(image2, caption="Second Image", use_column_width=True)

    st.success("Images uploaded successfully!")

    # Proceed Button
    from backend.selenium_automation import automate_runwayml

    if st.button("Proceed to Automation"):
        # Save uploaded images locally
        with open("image1.jpg", "wb") as f:
            f.write(uploaded_image1.getbuffer())
        with open("image2.jpg", "wb") as f:
            f.write(uploaded_image2.getbuffer())

        # Run automation
        automate_runwayml("image1.jpg", "image2.jpg")
        st.success("Automation completed! Check the results.")
else:
    st.warning("Please upload two images to proceed.")
