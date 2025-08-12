import pytest
import allure
import time
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# Config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# All XPaths and IDs
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "series_tab": "//li[@id='header-Tv Show']",
    "view_all_3": "(//a[text()='View All'])[3]",
    "series_category_id": "series-genre-5",
    "filter_dropdown": "//div[@id='react-select-3-placeholder']",
    "filter_input": "//input[contains(@id,'react-select-3-input')]"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("PPV Guest Watch Flow")
@allure.title("User filters Tamil shows in series category")
class TestSeriesFilter:

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 25)
            elem = wait.until(EC.element_to_be_clickable((by, locator)))
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", elem)
                time.sleep(1)
            elem.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def test_tamil_filter_in_series(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        self.driver.get(ReadConfig.getHomePageURL())
        self.driver.maximize_window()

        try:
            # Step 1: Login
            self.click(By.XPATH, xpaths["login_icon"], "01_Login_Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Submitted", attachment_type=AttachmentType.PNG)

            # Step 2: Choose profile
            self.click(By.XPATH, xpaths["choose_profile"], "03_Profile_Chosen")

            # Step 3: Navigate to Series section
            self.click(By.XPATH, xpaths["series_tab"], "04_Series_Tab")
            self.click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")
            self.click(By.ID, xpaths["series_category_id"], "06_Series_Category")

            # Step 4: Apply Language Filter - Tamil
            self.click(By.XPATH, xpaths["filter_dropdown"], "07_Filter_Dropdown")
            try:
                filter_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["filter_input"])))
                filter_input.send_keys("Tamil")
                time.sleep(1)
                filter_input.send_keys(u'\ue007')  # Press Enter
                print("✅ Filter 'Tamil' applied")
                time.sleep(10)
                allure.attach(self.driver.get_screenshot_as_png(), name="08_Filter_Tamil_Selected", attachment_type=AttachmentType.PNG)
            except Exception as e:
                time.sleep(10)
                allure.attach(self.driver.get_screenshot_as_png(), name="08_Filter_Failed", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Filter application failed: {e}")

            print("✅ Test completed: Login, Filter Tamil, and Navigation successful.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")
