import sys
import os
import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# ✅ Import project-level config reader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# ✅ XPath dictionary
xpaths = {
    "email": "//input[@id='advertiseremail']",
    "password": "//input[@id='advertiserpassword']",
    "login_submit": "//button[@id='advertisersubmit']"
}


@pytest.mark.usefixtures("browser_setup")
class TestLoginAdvertisements:

    def test_login_and_click_all_sections(self, browser_setup):
        self.driver = browser_setup
        self.wait = WebDriverWait(self.driver, 20)

        try:
            # ✅ Step 1: Open website from config
            url = ReadConfig.getAdvertiserPageURL()
            self.driver.get(url)
            self.driver.maximize_window()
            print("🌐 Website opened")
            allure.attach(self.driver.get_screenshot_as_png(), name="Application_Opened", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Login using values from xpaths dictionary
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getAdverEmail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getAdverPassword())
            self.driver.find_element(By.XPATH, xpaths["login_submit"]).click()

            # ✅ Optional wait or post-login validation
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)
            print("✅ Logged in")

        except Exception as e:
            print("❌ General Error:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Failed", attachment_type=AttachmentType.PNG)
            with open("login_fail_or_error.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Driver not closed.")
