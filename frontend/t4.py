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
EMAIL = "vinodvinum08@gmail.com"
PASSWORD = "wRqaC%5F7uJTGg8"

# Set up Chrome WebDriver (adjust the path if necessary)
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Add implicit wait
driver.implicitly_wait(10)  # seconds


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


# Streamlit Frontend
st.title("RunwayML Automation App")

# Display login status
if st.button("Login to RunwayML"):
    try:
        login_to_runwayml()
        st.success("Logged in successfully, navigated to AI tools page, and uploaded the file!")
    except Exception as e:
        st.error(f"Login failed: {e}")

# Streamlit's status message for the user
st.write("Click 'Login to RunwayML' to start the login process.")