import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

    

@pytest.mark.usefixtures("browser_setup")
class TestAddSlider:
    driver = webdriver.Firefox


      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    #xpath for All Slider Management

    All_slider_element = "//a[span[text()='All Slider']]"
    add_new_slider_element = "//a[@id='navigationLinkForAddPage']"
    slider_title_element = "//input[@name='title']"
    target_link_element = "//input[@name='link']"
    trailer_link_element = "//input[@name='trailer_link']"
    status_setting_element = "(//span[contains(@class, 'admin-slider') and contains(@class, 'admin-round')])[1]"
    slider_image_element = "//input[@name='dark']"
    player_image_element = "//input[@name='light']"
    save_button_element = "//button[@type='submit']"


    def test_add_slider(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
        time.sleep(2)

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            slider = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.All_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)
            self.driver.execute_script("arguments[0].click();", slider)
            print("Navigated to 'All Slider Management'")
        except Exception as e:
            print(f"Failed to navigate to All Slider Page: {e}")

        time.sleep(3)

        try:
            add_slider_button = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.add_new_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_slider_button)
            self.driver.execute_script("arguments[0].click();", add_slider_button)
            print("Clicked on 'Add New Slider' button")
        except Exception as e:
            print(f"Failed to click on 'Add New Slider' button: {e}")
        time.sleep(3)

        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.slider_title_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slider_title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")

        except Exception as e:
            print(f" Failed to enter title: {e}")

        try:
            target_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.target_link_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_link)
            time.sleep(2)
            target_link.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            target_link.send_keys("https://www.facebook.com")
            time.sleep(2)
            print(" Target link entered in the target link field.")
        except Exception as e:
            print(f" Failed to enter target link: {e}")


        try:
            trailer_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.trailer_link_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trailer_link)
            time.sleep(2)
            trailer_link.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            trailer_link.send_keys("https://www.youtube.com")
            time.sleep(2)
            print(" Trailer link entered in the trailer link field.")
        except Exception as e:
            print(f" Failed to enter trailer link: {e}")

        try:

            toggle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.status_setting_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            is_enabled = toggle.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                toggle.click()
                print(" toggle already enabled.")
            else:
                toggle.click()
                print(" toggle enabled.")

        except Exception as e:
            print(f"Failed to interact with toggle control: {e}")
        time.sleep(2)

        try:
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.slider_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        time.sleep(2)

        # Upload the player image
        try:
            player_image = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.player_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", player_image)
            time.sleep(2)
            player_image.send_keys(self.imageFile1280_720_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

        time.sleep(2)

        try:
            save_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.save_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
            time.sleep(2)
            save_button.click()
            print("Clicked on 'Save' button")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Slider added successfully", attachment_type=AttachmentType.PNG)
        except Exception as e:
            print(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Slider addition failed", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Failed to click on 'Save' button: {e}")
        time.sleep(5)

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")