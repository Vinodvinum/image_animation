import streamlit as st
from PIL import Image
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import base64
import time

# Load credentials from .env
load_dotenv()
EMAIL = "vinodvinum08@gmail.com"
PASSWORD = "wRqaC%5F7uJTGg8"

# Set up Chrome WebDriver (adjust the path if necessary)
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Add implicit wait
driver.implicitly_wait(10)  # seconds

st.set_page_config(page_title="Image Blending & Animation App", layout="wide")

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)



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

# Function to log in to RunwayML, navigate to the page, and upload a file
def login_to_runwayml():
    driver.get("https://runwayml.com/login")

    # Wait for the email field and input the email
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input")
    ))
    driver.find_element(By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input").send_keys(
        EMAIL)

    # Wait for the password field and input the password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input[2]")
    ))
    driver.find_element(By.XPATH,
                        "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input[2]").send_keys(
        PASSWORD)

    # Click the login button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/button")
    ))
    driver.find_element(By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/button").click()

    # Wait for login to complete and the dashboard to load
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Logged in successfully!")

    # After login, navigate to the specific URL
    driver.get("https://app.runwayml.com/video-tools/teams/vinuvinodm/ai-tools/generate")

    # Wait for the page to load fully
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']")  # Adjust the locator based on elements on the target page
    ))

    print("Successfully navigated to the AI tools page!")

    # Wait for the file input element to be present
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    # Specify the file path (update with the correct file location)
    file_path = r"E:\vin\Vinexperiments\runwayml_automation\output.webp"

    # Send the file path to the file input element
    file_input.send_keys(file_path)
    print(f"File '{file_path}' uploaded successfully!")
    write_text_with_send_keys("hug each other and smile")
    time.sleep(5)
    click_generate_button()


def write_text_with_send_keys(text):
    try:
        # Wait for the contenteditable div to appear
        contenteditable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@aria-label='Text Prompt Input' and @contenteditable='true']")
            )
        )

        # Focus the element
        contenteditable_div.click()

        # Clear existing content if needed
        contenteditable_div.send_keys(Keys.CONTROL, 'a')  # Select all text
        contenteditable_div.send_keys(Keys.BACKSPACE)  # Clear the selected text

        # Type the desired text
        contenteditable_div.send_keys(text)
        print(f"Text '{text}' written to the contenteditable div successfully with send_keys!")
    except Exception as e:
        print(f"Error writing text to the contenteditable div with send_keys: {e}")




def click_generate_button():
    try:
        # Wait for 5 seconds before clicking "Generate"
        time.sleep(2)

        # Locate the "Generate" button and click it
        generate_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'Button__ChildrenContainer') and text()='Generate']")
            )
        )
        generate_button.click()
        print("Clicked the 'Generate' button successfully!")
    except Exception as e:
        print(f"Error clicking the 'Generate' button: {e}")

set_background(r"E:\vin\Vinexperiments\runwayml_automation\frontend\bg1.webp")
# Streamlit Frontend
st.title("🌟 Image Merger and RunwayML Automation App")

# Upload two images
image1 = st.file_uploader("💡Upload the first image", type=["jpg", "jpeg", "png", "webp"])
image2 = st.file_uploader("💡Upload the second image", type=["jpg", "jpeg", "png", "webp"])

if image1 and image2:
    # Display images
    st.image([image1, image2], caption=["First Image", "Second Image"], use_column_width=True)

    # Merge images and save as output.webp
    output_path = os.path.join(os.getcwd(), "output.webp")

    try:
        result = merge_images(image1, image2, output_path)
        st.success(f"Images merged and saved as {result}!")
        st.image(result, caption="Merged Image", use_column_width=True)

        # After merging, run login and upload to RunwayML
        login_to_runwayml()
        st.success("Logged in to RunwayML, navigated to the AI tools page, and uploaded the merged image!")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("🎨Please upload both images to merge.")