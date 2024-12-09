import streamlit as st
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("RUNWAYML_EMAIL")
PASSWORD = os.getenv("RUNWAYML_PASSWORD")

# Set up Chrome WebDriver (adjust the path if necessary)
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Function to log in to RunwayML
def login_to_runwayml():
    driver.get("https://runwayml.com/login")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Logged in successfully!")

# Function to upload images to RunwayML
def upload_images(image1_path, image2_path):
    driver.get("https://runwayml.com/projects")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
    upload_input.send_keys(image1_path)
    time.sleep(2)

    upload_input.send_keys(image2_path)
    time.sleep(2)

    print("Images uploaded successfully!")

# Function to run the model and download results
def run_model_and_download_results():
    run_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Run')]")
    run_button.click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download')]")))

    download_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
    download_button.click()
    print("Results downloaded successfully!")

# Main function to integrate all steps
def automate_runwayml(image1_path, image2_path):
    try:
        login_to_runwayml()
        upload_images(image1_path, image2_path)
        run_model_and_download_results()
    finally:
        driver.quit()

# Streamlit Frontend
st.title("RunwayML Automation App")

st.header("Upload Two Images")
uploaded_image1 = st.file_uploader("Choose the first image", type=["jpg", "jpeg", "png"])
uploaded_image2 = st.file_uploader("Choose the second image", type=["jpg", "jpeg", "png"])

if uploaded_image1 and uploaded_image2:
    image1 = Image.open(uploaded_image1)
    image2 = Image.open(uploaded_image2)

    st.image(image1, caption="First Image", use_column_width=True)
    st.image(image2, caption="Second Image", use_column_width=True)

    st.success("Images uploaded successfully!")

    if st.button("Proceed to Automation"):
        with open("image1.jpg", "wb") as f:
            f.write(uploaded_image1.getbuffer())
        with open("image2.jpg", "wb") as f:
            f.write(uploaded_image2.getbuffer())

        automate_runwayml("image1.jpg", "image2.jpg")
        st.success("Automation completed! Check the results.")
else:
    st.warning("Please upload two images to proceed.")