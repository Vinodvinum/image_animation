from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time

# Load credentials from .env
load_dotenv()
EMAIL ="sanatanivinodmnayak@gmail.com"
PASSWORD ="wRqaC%5F7uJTGg8"

# Set up Chrome WebDriver
service = Service(r"E:\vin\Vinexperiments\runwayml_automation\backend\chromedriver-win64\chromedriver.exe")  # Update path if necessary
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def login_to_runwayml():
    # Open RunwayML login page
    driver.get("https://runwayml.com/login")

    # Wait for email input to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    # Enter credentials and log in
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()

    # Wait for login to complete
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Logged in successfully!")

def upload_images(image1_path, image2_path):
    # Navigate to the project or model page (replace with the specific URL)
    driver.get("https://runwayml.com/projects")

    # Wait for the file upload button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

    # Upload the first image
    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
    upload_input.send_keys(image1_path)
    time.sleep(2)  # Wait for upload

    # Upload the second image (if there's another file input for it)
    upload_input.send_keys(image2_path)
    time.sleep(2)  # Wait for upload

    print("Images uploaded successfully!")

def run_model_and_download_results():
    # Trigger the model execution (modify as per the model's specific UI)
    run_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Run')]")
    run_button.click()

    # Wait for results to be ready
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download')]")))

    # Download the results
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

# Example usage
if __name__ == "__main__":
    automate_runwayml("path/to/image1.jpg", "path/to/image2.jpg")