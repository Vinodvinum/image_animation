import streamlit as st
from PIL import Image
import os


# Function to merge two images and save them
def merge_images(image1, image2, output_path):
    # Open the images using Pillow
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    # Resize images to fit into 768x1280 (either side by side or stacked)
    img1 = img1.resize((384, 1280))  # Resize first image to 384x1280
    img2 = img2.resize((384, 1280))  # Resize second image to 384x1280

    # Create a new image with dimensions (768x1280) and paste the resized images
    merged_image = Image.new("RGB", (768, 1280))
    merged_image.paste(img1, (0, 0))  # Paste the first image on the left
    merged_image.paste(img2, (384, 0))  # Paste the second image on the right

    # Save the merged image
    merged_image.save(output_path, "WEBP")
    return output_path


# Streamlit Frontend
st.title("Image Merger App")

# Upload two images
image1 = st.file_uploader("Upload the first image", type=["jpg", "jpeg", "png", "webp"])
image2 = st.file_uploader("Upload the second image", type=["jpg", "jpeg", "png", "webp"])

if image1 and image2:
    # Display images
    st.image([image1, image2], caption=["First Image", "Second Image"], use_column_width=True)

    # Merge images and save as output.webp
    output_path = os.path.join(os.getcwd(), "output.webp")

    try:
        result = merge_images(image1, image2, output_path)
        st.success(f"Images merged and saved as {result}!")
        st.image(result, caption="Merged Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("Please upload both images to merge.")