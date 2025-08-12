import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
    "select_field_id": "selectField",
    "smtp_option_id": "smtp",
    "host_email_id": "host_email",
    "email_port_id": "email_port",
    "select_field2_id": "false",
    "email_type_input": "//input[@type='email']",
    "email_password_name": "email_password",
    "forget_limit_id": "forget_password_limit",
    "forget_expiry_id": "forget_password_exists_after_minutes",
    "admin_email_id": "admin_email",
    # "file_upload_input": "//input[@type='file']",
    "toggle1": "(//span[@class='admin-slider position-absolute admin-round '])[1]",
    "toggle2": "(//span[@class='admin-slider position-absolute admin-round '])[2]",
    "test_mail_input_id": "test_mail",
    "submit_btn_id_1" : "(//button[@id='adminButton'])[3]",
    "submit_btn_id": "adminButton"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Admin Email Settings Flow")
@allure.title("Admin configures SMTP email settings and sends test mail")
class TestAdminSMTPSettingsInvalid:

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

    def test_email_settings_Invalid(self, browser_setup):
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

            # Navigate to Email Settings
            self.click(By.XPATH, xpaths["settings"], "04_Settings")
            self.click(By.XPATH, xpaths["email_settings"], "05_Email_Settings")

            # SMTP Selection
            self.click(By.ID, xpaths["select_field_id"], "06_Dropdown_1")
            self.click(By.ID, xpaths["smtp_option_id"], "07_Select_SMTP")

            # SMTP Configuration Fields
            self.enter_text(By.ID, xpaths["host_email_id"], "smtp.gmail.com", "08_Host_Email")
            self.enter_text(By.ID, xpaths["email_port_id"], "578", "09_Email_Port")
            self.click(By.ID, xpaths["select_field2_id"], "10_Dropdown_2")
            self.enter_text(By.XPATH, xpaths["email_type_input"], "test@test.com", "11_Sender_Email")
            self.enter_text(By.NAME, xpaths["email_password_name"], "hiqvjbxtelxfiubb", "12_Email_Password")
            self.enter_text(By.ID, xpaths["forget_limit_id"], "5", "13_Forget_Limit")
            self.enter_text(By.ID, xpaths["forget_expiry_id"], "00:10", "14_Forget_Expiry")
            self.enter_text(By.ID, xpaths["admin_email_id"], "vodflicknexs@gmail.com", "15_Admin_Email")

            # # Upload File
            # upload_path = r"C:/Users/Picnexs/Desktop/website/vodwebsite/tmp/email.jpg"
            # if not os.path.exists(upload_path):
            #     raise AssertionError(f"❌ Upload file not found: {upload_path}")
            # self.driver.find_element(By.XPATH, xpaths["file_upload_input"]).send_keys(upload_path)
            # print("✅ File uploaded")
            # allure.attach(self.driver.get_screenshot_as_png(), name="16_File_Uploaded", attachment_type=AttachmentType.PNG)

            # Toggle Options
            self.click(By.XPATH, xpaths["toggle1"], "17_Toggle_1")
            self.click(By.XPATH, xpaths["toggle2"], "18_Toggle_2")

           # Test Mail & Submit
            self.enter_text(By.ID, xpaths["test_mail_input_id"], "rubanbe2003@gmail.com", "19_Test_Email")
            self.click(By.XPATH, xpaths["submit_btn_id_1"], "20_Submit_Button")
            print("✅ Email settings updated and test email sent.")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="21_Form_Submitted", attachment_type=AttachmentType.PNG)
            time.sleep(7)
            self.click(By.ID, xpaths["submit_btn_id"], "21_Submit_Button")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="21_Form_Submitted", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
