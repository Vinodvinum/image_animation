import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL ="vinodvinum08@gmail.com"
PASSWORD ="wRqaC%5F7uJTGg8"

# Set up Chrome WebDriver (adjust the path if necessary)
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


# Function to log in to RunwayML
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
    start_new_session()  # Navigate to "Start a new session" after login


# Function to navigate and click "Start a new session"
def start_new_session():
    # Wait for the "Start a new session" element to appear
    new_session_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='root']/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div[2]/a"))
    )
    new_session_button.click()
    print("Navigated to 'Start a new session' successfully!")

    # Full process after clicking "Open file picker"
    upload_file(r"C:\Users\HP\Downloads\internshalaProject\brothers.webp")


# Function to upload a file
def upload_file(file_path):
    try:
        # Wait for the file input element to be present
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        # Send the file path to the input element
        file_input.send_keys(file_path)
        print(f"File '{file_path}' uploaded successfully!")

        # Wait for 15 seconds after file upload
        time.sleep(5)
        write_text_with_send_keys("Hug each other, and smile ")
        time.sleep(2)
        click_generate_button()
        time.sleep(15)
        play_video_and_download()




    except Exception as e:
        print(f"Error while uploading file: {e}")


# Function to write text into a contenteditable div
# Function to write text into a contenteditable div
from selenium.webdriver.common.keys import Keys


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
        generate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'Button__ChildrenContainer') and text()='Generate']")
            )
        )
        generate_button.click()
        print("Clicked the 'Generate' button successfully!")
    except Exception as e:
        print(f"Error clicking the 'Generate' button: {e}")

def play_video_and_download():
    try:
        # Locate the video element and play it
        video_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='magic-tool-main-container']/div/div/div[3]/div[2]/div/div/div/div/div[2]/div/div/div[2]/video")
            )
        )
        driver.execute_script("arguments[0].play();", video_element)
        print("Video is now playing!")

        # Locate the download button and click it
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='magic-tool-main-container']/div/div/div[3]/div[2]/div/div/div/div/div[2]/div/div/div/div[4]/button/svg")
            )
        )
        download_button.click()
        print("Download button clicked successfully!")

    except Exception as e:
        print(f"Error during play video and download actions: {e}")

# Streamlit Frontend
st.title("RunwayML Automation App")

# Display login status
if st.button("Login to RunwayML"):
    try:
        login_to_runwayml()
        st.success("Logged in successfully!")
    except Exception as e:
        st.error(f"Login failed: {e}")

# Streamlit's status message for the user
st.write("Click 'Login to RunwayML' to start the login process.")