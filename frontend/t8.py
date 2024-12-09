from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import streamlit as st
import time
import os

# Credentials
EMAIL = "vinodm08"
PASSWORD = "wRqaC%5F7uJTGg8"

# Paths
CHROMEDRIVER_PATH = r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe"
DOWNLOAD_DIR = r"C:\path_to_download_folder"  # Replace with your download folder path

# Configure Chrome WebDriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": DOWNLOAD_DIR}
options.add_experimental_option("prefs", prefs)
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Login to RunwayML
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

    driver.get("https://app.runwayml.com/video-tools/teams/vinodm08/ai-tools/generate?sessionId=983cb0d0-9a20-485d-9b23-0a8eeb10736d")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']")))
    print("Successfully navigated to the AI tools page!")
    time.sleep(10)
    downloaded_file = download_result()
    return downloaded_file


# Test Download Function
def download_result():
    try:
        # Wait for 20 seconds to ensure results are ready (adjust as needed)
        time.sleep(20)

        # Locate the download button
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ShortcutTooltip___StyledRadixTooltipTrigger-sc-1bugq75-7') and contains(@class, 'icvmxJ') and contains(@class, 'task-header-module__mainButton__Yyjb7')]"))
        )
        download_button.click()
        time.sleep(30)
        print("Clicked the 'Download' button successfully!")

        # Wait for the file to appear in the download directory
        timeout = 60  # seconds
        start_time = time.time()
        while not any(file.endswith(".mp4") for file in os.listdir(DOWNLOAD_DIR)):
            if time.time() - start_time > timeout:
                raise Exception("Download timed out")
            time.sleep(1)

        print("File downloaded successfully!")
        files = os.listdir(DOWNLOAD_DIR)
        if files:
            return os.path.join(DOWNLOAD_DIR, files[0])
        time.sleep(1)
    except Exception as e:
        print(f"Error downloading the file: {e}")

# Main Execution
st.title("🌟 Image Merger and RunwayML Automation App")
if st.button("Login to RunwayML"):
    try:
        downloaded_file = login_to_runwayml()
        st.success("Logged in successfully, navigated to AI tools page, and uploaded the file!")
        if downloaded_file:
            st.success(f"File downloaded successfully: {os.path.basename(downloaded_file)}")
            if downloaded_file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                st.image(downloaded_file, caption="Generated Result", use_column_width=True)
            elif downloaded_file.endswith(('.mp4', '.webm')):
                st.video(downloaded_file)
                # Provide Streamlit download button
                with open(downloaded_file, "rb") as file:
                    file_bytes = file.read()
                    st.download_button(
                        label="📥 Download File Again",
                        data=file_bytes,
                        file_name=os.path.basename(downloaded_file),
                        mime="application/octet-stream",
                    )


        else:
            st.error("Failed to download the file.")

    except Exception as e:
        st.error(f"Login failed: {e}")




