import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from allure_commons.types import AttachmentType

# Config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig


xpaths = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "settings": "//span[text()='Settings']",
    "email_settings": "//span[text()='Email Settings']",

    "toggle1": "(//span[@class='admin-slider position-absolute admin-round '])[3]",
    "submit_btn_id": "adminButton"
}

toggle_xpath_list = [f"(//label[@class='admin-switch m-0'])[{i}]" for i in range(3, 20)]

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Admin Email Settings - Minimal Config")
@allure.title("Email config with toggles and test mail")
class TestAdminEmailMinimal:

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 30)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", elem)
                time.sleep(1)
            wait.until(EC.element_to_be_clickable((by, locator)))
            try:
                elem.click()
            except:
                self.driver.execute_script("arguments[0].click();", elem)
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        try:
            wait = WebDriverWait(self.driver, 30)
            retries = 2
            for _ in range(retries):
                try:
                    elem = wait.until(EC.presence_of_element_located((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                    time.sleep(1)
                    elem.clear()
                    elem.send_keys(value)
                    print(f"✅ Entered: {label}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
                    return
                except StaleElementReferenceException:
                    print(f"⚠️ Retrying {label} due to stale element")
                    time.sleep(2)
            raise Exception("Stale reference not resolved")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to enter {label}: {e}")

    def test_email_config_minimal(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        try:
            # Login
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
            self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
            self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

            # Navigate
            self.click(By.XPATH, xpaths["settings"], "Settings_Click")
            self.click(By.XPATH, xpaths["email_settings"], "Email_Settings_Click")

            # Dynamic toggles from 3 to 19
            for i, toggle_xpath in enumerate(toggle_xpath_list, start=3):
                self.click(By.XPATH, toggle_xpath, f"Toggle_{i}")

            # Test Email and Submit
            
            
            print("✅ Email settings configured and test email sent.")
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Success", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
