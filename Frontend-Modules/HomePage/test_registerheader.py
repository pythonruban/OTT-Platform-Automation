import sys
import os
import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# ✅ Add root path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig


@allure.feature("Login and Header Menu Navigation")
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
            allure.attach(self.driver.get_screenshot_as_png(), name="01_Home_Loaded", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Perform Login
            login_icon_xpath = "(//button[@type='button'])[1]"
            email_xpath = "//input[@name='email']"
            password_xpath = "//input[@name='password']"
            login_btn_xpath = "//button[@id='signin-submit']"
            profile_xpath = "(//img[@alt='Avatar'])[1]"

            wait.until(EC.element_to_be_clickable((By.XPATH, login_icon_xpath))).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, email_xpath))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, password_xpath).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, login_btn_xpath).click()
            print("✅ Login submitted")
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Success", attachment_type=AttachmentType.PNG)

            # ✅ Step 3: Choose Profile
            wait.until(EC.element_to_be_clickable((By.XPATH, profile_xpath))).click()
            print("✅ Profile selected")
            allure.attach(self.driver.get_screenshot_as_png(), name="03_Profile_Selected", attachment_type=AttachmentType.PNG)

            # ✅ Step 4: Loop over header spans starting from index 1 (skip home)
            total_menu_items = 6  # [0] = Home, [1]-[5] = categories like Movies, Music, etc.
            for i in range(1, total_menu_items):  # Start from index 1 (skip Home)
                xpath = f"(//span[@class='theme-text-color'])[{i + 1}]"

                with allure.step(f"Clicking top menu index: {i}"):
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    menu_name = element.text.strip()
                    print(f"👉 Clicking index {i}: {menu_name}")
                    element.click()
                    time.sleep(2)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"04_Clicked_{menu_name}_Index{i}", attachment_type=AttachmentType.PNG)

                with allure.step(f"Return to home from index {i}"):
                    self.driver.back()
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(1)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"05_Back_From_{menu_name}_Index{i}", attachment_type=AttachmentType.PNG)

            print("✅ All header menu items clicked and verified.")

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver already closed")
