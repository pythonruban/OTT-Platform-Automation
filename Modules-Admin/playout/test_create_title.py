import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType

# Path config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

Xpath = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "tv_playout": "//span[text()='TV Playout']",
    "create_button": "//button[@id='adminButton']",
    "name_input": "//input[@id='create-name']",
    "select_type": "//select[@id='create-select-type']",
    "option_schedule_stream": "//option[@id='Schedule stream']",
    "submit_btn": "(//button[@id='adminButton'])[2]"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("TV Playout Module")
@allure.title("Create TV Playout Entry")
class TestTVPlayoutCreate:

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 30)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                time.sleep(1)
            wait.until(EC.element_to_be_clickable((by, locator)))
            try:
                elem.click()
            except:
                self.driver.execute_script("arguments[0].click();", elem)
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Timeout: Couldn't click {label}")
        except Exception as e:
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        try:
            wait = WebDriverWait(self.driver, 30)
            elem = wait.until(EC.element_to_be_clickable((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            elem.clear()
            elem.send_keys(value)
            print(f"✅ Entered: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            raise AssertionError(f"❌ Failed to enter {label}: {e}")

    def test_tv_playout_create(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        try:
            # Login
            wait.until(EC.presence_of_element_located((By.XPATH, Xpath["email_input"]))).send_keys(ReadConfig.getAdminId())
            self.driver.find_element(By.XPATH, Xpath["password_input"]).send_keys(ReadConfig.getPassword())
            self.driver.find_element(By.XPATH, Xpath["login_button"]).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, Xpath["dashboard_check"])))
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

            # Navigate to TV Playout
            self.click(By.XPATH, Xpath["tv_playout"], "TV_Playout")
            self.click(By.XPATH, Xpath["create_button"], "create button")
            # Enter name
            self.enter_text(By.XPATH, Xpath["name_input"], "testingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtestingtesting", "TV Name")
            
            # Select Schedule stream
            self.click(By.XPATH, Xpath["select_type"], "Select Type Dropdown")
            self.click(By.XPATH, Xpath["option_schedule_stream"], "Select Schedule Stream")

            # Submit
            self.click(By.XPATH, Xpath["submit_btn"], "Submit")
            time.sleep(10)

            print("✅ TV Playout created successfully.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
