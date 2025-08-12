import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from allure_commons.types import AttachmentType

# Config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# XPaths used
xpaths = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "tv_playout": "//span[text()='TV Playout']",
    "status_button": "//span[@id='status_btn']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("TV Playout - Status Toggle")
@allure.title("Toggle TV Playout Status and Confirm JS Alert")
class TestTVPlayoutStatus:

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                time.sleep(0.5)
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

    def test_toggle_status(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        try:
            # Step 1: Login
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
            self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
            self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

            # Step 2: Click TV Playout
            self.click(By.XPATH, xpaths["tv_playout"], "TV_Playout")

            # Step 3: Click Status Button (triggers JS confirm popup)
            self.click(By.XPATH, xpaths["status_button"], "Status_Button")

            # Step 4: Handle JS Alert (click OK)
            try:
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                print(f"⚠️ Alert text: {alert.text}")
                time.sleep(1)
                alert.accept()  # Click OK
                print("✅ Alert accepted successfully.")
                allure.attach(self.driver.get_screenshot_as_png(), name="Alert_Accepted", attachment_type=AttachmentType.PNG)
            except (NoAlertPresentException, UnexpectedAlertPresentException) as ex:
                raise AssertionError(f"❌ Failed to handle JS alert: {ex}")

            time.sleep(2)
            print("✅ Status toggle completed successfully.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
