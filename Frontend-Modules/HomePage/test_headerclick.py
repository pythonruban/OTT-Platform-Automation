import sys
import os
import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# ✅ Add root path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig


@allure.feature("Guest Header Menu Navigation by Index")
class TestHeaderMenusByIndex:

    def test_click_menu_by_index(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)

        try:
            # ✅ Step 1: Open homepage
            url = ReadConfig.getHomePageURL()
            self.driver.get(url)
            self.driver.maximize_window()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"🌐 Opened Homepage: {url}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Home_Loaded", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Loop over header spans starting from index 1 (skip home)
            total_menu_items = 6  # [0] = Home, [1]-[5] = categories
            for i in range(1, total_menu_items):  # Start from index 1
                xpath = f"(//span[@class='theme-text-color'])[{i + 1}]"  # XPath is 1-based, index 0 = [1]

                with allure.step(f"Clicking top menu index: {i}"):
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    menu_name = element.text
                    print(f"👉 Clicking index {i}: {menu_name}")
                    element.click()
                    time.sleep(2)

                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Clicked_{menu_name}_Index{i}", attachment_type=AttachmentType.PNG)

                with allure.step(f"Return to home from index {i}"):
                    self.driver.back()
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(1)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Back_From_{menu_name}_Index{i}", attachment_type=AttachmentType.PNG)

            print("✅ All menu items clicked by index and verified")

        except Exception as e:
            print(f"❌ Test failed at menu index: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver already closed")
