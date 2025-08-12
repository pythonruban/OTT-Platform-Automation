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

# XPaths and IDs
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "live_tab": "//li[@id='header-Live']",
    "view_all_3": "(//a[text()='View All'])[2]",
    "live_category_id": "livecategories-0",
    "filter_dropdown": "//div[contains(text(),'Language') and contains(@class,'css')]",
    "filter_panel": "//div[contains(@class,'menu')]",
    "filter_option_tamil": "//div[text()='Tamil']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("PPV Guest Watch Flow")
@allure.title("User filters Tamil shows in live category")
class TestliveFilter:

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

    def test_tamil_filter_in_live(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        self.driver.get(ReadConfig.getHomePageURL())
        self.driver.maximize_window()

        try:
            # Login flow
            self.click(By.XPATH, xpaths["login_icon"], "01_Login_Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Submitted", attachment_type=AttachmentType.PNG)

            # Profile choose
            self.click(By.XPATH, xpaths["choose_profile"], "03_Profile_Chosen")

            # Navigate to Live
            self.click(By.XPATH, xpaths["live_tab"], "04_Live_Tab")
            self.click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")
            self.click(By.ID, xpaths["live_category_id"], "06_Live_Category")

            # Language Filter
            self.click(By.XPATH, xpaths["filter_dropdown"], "07_Filter_Dropdown")

            # Wait for dropdown panel to appear
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["filter_panel"])))
            tamil_option = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["filter_option_tamil"])))
            tamil_option.click()

            print("✅ Filter 'Tamil' applied successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="08_Filter_Tamil_Selected", attachment_type=AttachmentType.PNG)
            time.sleep(5)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {e}")
