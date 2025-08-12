import pytest
import allure
import os
import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "tv_playout": "//span[text()='TV Playout']",
    "create_button": "//button[@id='adminButton']",
    "name_input": "//input[@id='create-name']",
    "select_type": "//select[@id='create-select-type']",
    "option_schedule_stream": "//option[@id='Schedule stream']",
    "submit_btn": "(//button[@id='adminButton'])[2]",
    "input_title": "//input[@id='playout-title']",
    "playout_mode": "//select[@id='playout_types']",
    "playout_select": "//option[@id='schedule']",
    "select_live": "//select[@id='destination_title']",
    "live_select": "//option[@id='1']",
    "substitute_video": "//select[@id='substitute_title']",
    "substitute_select": "//option[@id='52']",
    "taggle_button": "//span[@class='admin-slider position-absolute admin-round ']",
    "thumbnail_image": "//input[@id='playout-thumbnail-image']",
    "player_image": "//input[@id='playout-plyer-image']",
    "submit_button": "(//button[@id='adminButton'])[1]"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("TV Playout - Create New Stream")
@allure.title("Create New Schedule Stream with File Uploads")
class TestCreatethumbnailinvalidsize:

    def click(self, by, locator, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            time.sleep(0.5)
            try:
                elem.click()
            except Exception as e:
                print(f"⚠️ Click intercepted, using JS click for: {label}")
                self.driver.execute_script("arguments[0].click();", elem)
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            elem.clear()
            elem.send_keys(value)
            print(f"✅ Entered: {label} = {value}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            raise AssertionError(f"❌ Failed to enter text in {label}: {e}")

    def test_create_thumbnail_invalid(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        # Step 1: Login
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))
        allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

        # Step 2: TV Playout → Create
        self.click(By.XPATH, xpaths["tv_playout"], "02_TV_Playout")
        self.click(By.XPATH, xpaths["create_button"], "03_Create_Button")

        # Step 3: Fill fields
        self.enter_text(By.XPATH, xpaths["name_input"], "Test Stream", "04_Stream_Name")
        self.click(By.XPATH, xpaths["select_type"], "05_Select_Type")
        self.click(By.XPATH, xpaths["option_schedule_stream"], "06_Option_Schedule")
        self.click(By.XPATH, xpaths["submit_btn"], "07_Submit_Intermediate")

        # Step 4: Wait for redirect
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["input_title"])))

        self.enter_text(By.XPATH, xpaths["input_title"], "Test Title", "08_Playout_Title")
        self.click(By.XPATH, xpaths["playout_mode"], "09_Playout_Mode")
        self.click(By.XPATH, xpaths["playout_select"], "10_Select_Schedule")
        self.click(By.XPATH, xpaths["select_live"], "11_Select_Live")
        self.click(By.XPATH, xpaths["live_select"], "12_Live_Option")
        self.click(By.XPATH, xpaths["substitute_video"], "13_Select_Substitute")
        self.click(By.XPATH, xpaths["substitute_select"], "14_Substitute_Option")

        # Toggle switches (click twice if required)
        self.click(By.XPATH, xpaths["taggle_button"], "15_Toggle_1")
        time.sleep(1)
        self.click(By.XPATH, xpaths["taggle_button"], "16_Toggle_2")

        # Step 5: Upload Files
        thumb_path = os.path.abspath(r"C:/Users/Picnexs/Desktop/website/vodwebsite/tmp/1080_10802.jpg")
        player_path = os.path.abspath(r"C:/Users/Picnexs/Desktop/website/vodwebsite/tmp/1280_720 px.png")

        if not os.path.exists(thumb_path) or not os.path.exists(player_path):
            raise AssertionError(f"❌ One or both image files not found:\n{thumb_path}\n{player_path}")

        self.driver.find_element(By.XPATH, xpaths["thumbnail_image"]).send_keys(thumb_path)
        print("✅ Uploaded Thumbnail")
        self.driver.find_element(By.XPATH, xpaths["player_image"]).send_keys(player_path)
        print("✅ Uploaded Player Image")
        allure.attach(self.driver.get_screenshot_as_png(), name="17_Images_Uploaded", attachment_type=AttachmentType.PNG)

        # Step 6: Final Submit
        try:
            self.click(By.XPATH, xpaths["submit_button"], "Invalid THumbnail")
            time.sleep(10)
            allure.attach(self.driver.get_screenshot_as_png(), name="19_Stream_Creation_Complete", attachment_type=AttachmentType.PNG)
            print("✅ Stream created successfully.")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="19_Submit_Click_Failed", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Final Submit button not clickable: {e}")
