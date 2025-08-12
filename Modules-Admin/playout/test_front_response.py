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
    "live_select": "//option[@id='9']",
    "substitute_video": "//select[@id='substitute_title']",
    "substitute_select": "//option[@id='52']",
    "taggle_button": "//span[@class='admin-slider position-absolute admin-round ']",
    "thumbnail_image": "//input[@id='playout-thumbnail-image']",
    "player_image": "//input[@id='playout-plyer-image']",
    "submit_button": "(//button[@id='adminButton'])[2]",

    # Remaining flows:
    "tab_home": "//button[@id='pills-home-tab']",
    "search_input": "//input[@id='video-search-input col-3']",
    "search_result": "//td[@class='live-wrapper']",
    "cancel_video" : "//button[@class='bg-transparent ms-4 text-dark']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("TV Playout - Create New Stream with Thumbnail Valid")
@allure.title("Create Schedule Stream and Validate Search")
class TestCreatefront_end_show:

    def click(self, by, locator, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.element_to_be_clickable((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            time.sleep(0.5)
            try:
                elem.click()
            except Exception:
                print(f"⚠️ JS click fallback for {label}")
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

    def test_create_front_end_show(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        # Login
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))
        allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

        # Navigate to Create Stream
        self.click(By.XPATH, xpaths["tv_playout"], "02_TV_Playout")
        self.click(By.XPATH, "//a[@href='/edit/tv-playouts/2']", "33_Click_Edit_Stream")
        time.sleep(2)
        allure.attach(self.driver.get_screenshot_as_png(), name="34_Edit_Stream_Page", attachment_type=AttachmentType.PNG)
        
        self.click(By.XPATH, "//a[text()='Preview']", "35_Click_Preview")
        time.sleep(3)
        allure.attach(self.driver.get_screenshot_as_png(), name="36_Preview_Stream", attachment_type=AttachmentType.PNG)