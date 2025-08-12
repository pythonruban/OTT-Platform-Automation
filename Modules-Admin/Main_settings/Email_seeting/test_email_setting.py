import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
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
    "edit_dropdown_btn": "(//span[@class='editdropdown-button'])[1]",
    "edit_option": "(//div[@class='editdropdown-menu theme-bg-color rounded-2'])[1]//span[text()='Edit']",
    "input_field_1": "(//input[@name='template_type'])[1]",
    "input_field_2": "(//input[@type='text'])[3]",
    "paragraph_3": "//div[@class='jodit-workplace']",
    "submit_btn": "//button[@id='adminButton']",
    "back_arrow": "//button[@id='backArrow']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("Edit Email Template")
@allure.title("Edit Single Email Template and Submit")
class TestEditTemplate:

    def click(self, by, locator, label, scroll=True):
        wait = WebDriverWait(self.driver, 30)
        try:
            print(f"🔎 Clicking: {label} → {locator}")
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            wait.until(EC.element_to_be_clickable((by, locator)))
            elem.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        wait = WebDriverWait(self.driver, 30)
        try:
            print(f"📝 Typing: {label} → {value}")
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            elem.clear()
            elem.send_keys(value)
            print(f"✅ Entered: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to enter text for {label}: {e}")

    def test_edit_one_template(self, browser_setup):
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
            print("✅ Login successful")
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

            # Navigate to Email Settings
            self.click(By.XPATH, xpaths["settings"], "Settings")
            self.click(By.XPATH, xpaths["email_settings"], "Email Settings")

            # Click Edit Dropdown and Edit
            self.click(By.XPATH, xpaths["edit_dropdown_btn"], "Edit Dropdown")
            self.click(By.XPATH, xpaths["edit_option"], "Edit Option")

            # Enter data
            self.enter_text(By.XPATH, xpaths["input_field_1"], "Welcome Email", "Template Type")
            self.enter_text(By.XPATH, xpaths["input_field_2"], "Welcome Email", "Title")

            # Paragraph using JavaScript
            js_script = """
                const editor = document.querySelector(arguments[0]);
                if (editor) {
                    editor.innerHTML = arguments[1];
                    editor.dispatchEvent(new Event('input'));
                }
            """
            self.driver.execute_script(js_script, xpaths["paragraph_3"], "Welcome All")
            print("✅ Entered Paragraph")
            allure.attach(self.driver.get_screenshot_as_png(), name="Paragraph", attachment_type=AttachmentType.PNG)

            # Submit and Go Back
            self.click(By.XPATH, xpaths["submit_btn"], "Submit")
            time.sleep(3)
            self.click(By.XPATH, xpaths["back_arrow"], "Back")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
