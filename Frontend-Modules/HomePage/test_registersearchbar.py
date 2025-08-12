import sys
import os
import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "search_icon": "//a[@id='search-icon']",  # ✅ click this icon to open search
    "search_input_id": "scrollingPlaceholder-searchValue"  # ✅ final working input field
}

@allure.feature("Search")
@allure.title("Login → Click Search → Type and Submit Search Queries")
class TestSearchFlowFinal:

    def test_search_icon_and_input_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)

        try:
            with allure.step("Step 1: Open Home Page and Login"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()

                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Choose Profile"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="02_Profile_Selected", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Click Search Icon and Wait for Input"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["search_icon"]))).click()
                wait.until(EC.visibility_of_element_located((By.ID, xpaths["search_input_id"])))
                allure.attach(self.driver.get_screenshot_as_png(), name="03_Search_Opened", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Search for 'leo'"):
                search_box = self.driver.find_element(By.ID, xpaths["search_input_id"])
                search_box.clear()
                search_box.send_keys("leo")
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="04_Search_Leo", attachment_type=AttachmentType.PNG)

            with allure.step("Step 5: Search for 'ruban'"):
                search_box.clear()
                search_box.send_keys("ruban")
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="05_Search_Ruban", attachment_type=AttachmentType.PNG)

            print("✅ Search flow completed successfully.")
            assert True

        except Exception as e:
            print(f"❌ Test failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver already closed.")
