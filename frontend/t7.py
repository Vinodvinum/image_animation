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
EMAIL = "vinodm08"
PASSWORD = "wRqaC%5F7uJTGg8"

# Set up Chrome WebDriver (adjust the path if necessary)
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()

# Set up download directory for Selenium
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
})

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
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    img1 = img1.resize((384, 1280))  # Resize first image
    img2 = img2.resize((384, 1280))  # Resize second image

    merged_image = Image.new("RGB", (768, 1280))
    merged_image.paste(img1, (0, 0))  # Paste first image on the left
    merged_image.paste(img2, (384, 0))  # Paste second image on the right

    merged_image.save(output_path, "WEBP")
    return output_path


# Function to log in to RunwayML and upload a file
def login_to_runwayml():
    driver.get("https://runwayml.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input")
    )).send_keys(EMAIL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/div/input[2]")
    )).send_keys(PASSWORD)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='root']/div/div[4]/div/div/div[2]/div/div[2]/div/form/button")
    )).click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Logged in successfully!")

    driver.get("https://app.runwayml.com/video-tools/teams/vinodm08/ai-tools/generate")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']")))
    print("Successfully navigated to the AI tools page!")

    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_input.send_keys(r"E:\vin\Vinexperiments\runwayml_automation\output.webp")
    print("File uploaded successfully!")


def write_text_with_send_keys(text):
    contenteditable_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Text Prompt Input' and @contenteditable='true']"))
    )
    contenteditable_div.click()
    contenteditable_div.send_keys(Keys.CONTROL, 'a')
    contenteditable_div.send_keys(Keys.BACKSPACE)
    contenteditable_div.send_keys(text)
    print(f"Text '{text}' written to the input box.")


def download_result():
    try:
        download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//svg[contains(@class, 'lucide') and contains(@class, 'lucide-download')]/parent::*")
            )
        )
        download_button.click()
        print("Clicked the 'Download' button successfully!")

        # Wait for the file to appear in the download directory
        start_time = time.time()
        while time.time() - start_time < 60:
            files = os.listdir(DOWNLOAD_DIR)
            if files:
                return os.path.join(DOWNLOAD_DIR, files[0])
            time.sleep(1)

    except Exception as e:
        print(f"Error downloading the file: {e}")
        return None


def click_generate_button():
    try:
        time.sleep(5)
        generate_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'Button__ChildrenContainer') and text()='Generate']")
            )
        )
        generate_button.click()
        print("Clicked the 'Generate' button successfully!")
        downloaded_file = download_result()
        return downloaded_file
    except Exception as e:
        print(f"Error generating the result: {e}")
        return None


set_background(r"E:\vin\Vinexperiments\runwayml_automation\frontend\bg1.webp")

# Streamlit Frontend
st.title("🌟 Image Merger and RunwayML Automation App")

image1 = st.file_uploader("💡Upload the first image", type=["jpg", "jpeg", "png", "webp"])
image2 = st.file_uploader("💡Upload the second image", type=["jpg", "jpeg", "png", "webp"])

if image1 and image2:
    st.image([image1, image2], caption=["First Image", "Second Image"], use_column_width=True)

    output_path = os.path.join(os.getcwd(), "output.webp")
    try:
        result = merge_images(image1, image2, output_path)
        st.success(f"Images merged and saved as {result}!")
        st.image(result, caption="Merged Image", use_column_width=True)

        login_to_runwayml()
        st.success("Logged in to RunwayML, navigated to the AI tools page, and uploaded the merged image!")

        write_text_with_send_keys("hug each other and smile")
        downloaded_file = click_generate_button()

        if downloaded_file:
            st.success(f"File downloaded successfully: {os.path.basename(downloaded_file)}")
            if downloaded_file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                st.image(downloaded_file, caption="Generated Result", use_column_width=True)
            elif downloaded_file.endswith(('.mp4', '.webm')):
                st.video(downloaded_file)
        else:
            st.error("Failed to download the file.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("🎨 Please upload both images to merge.")