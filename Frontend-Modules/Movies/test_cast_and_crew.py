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
    "video_tab": "//li[@id='header-Movies']",
    "view_all_3": "(//a[text()='View All'])[1]",
    "video_category_id": "videocategories-1",
    "video_block_id": "videos-0",
    "cast_and_crew": "//li[@id='video-tab-2']",
    "cast_and_crew_details": "//a[@id='artist-0']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("cast and crew")
@allure.title("User views Cast and Crew details from episode")
class TestCastAndCrew:

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

    def test_cast_and_crew_flow(self, browser_setup):
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

            # Step 3: Navigate to video > View All > Category > Show
            self.click(By.XPATH, xpaths["video_tab"], "04_video_Tab")
            self.click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")
            self.click(By.ID, xpaths["video_category_id"], "06_video_Category")

            # Step 4: Click on Video Block
            show_elem = wait.until(EC.element_to_be_clickable((By.ID, xpaths["video_block_id"])))
            self.driver.execute_script("arguments[0].click();", show_elem)
            print("✅ Show Clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Clicked", attachment_type=AttachmentType.PNG)

            # Step 5: Cast and Crew Tab
            self.click(By.XPATH, xpaths["cast_and_crew"], "08_Cast_And_Crew_Tab")
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="08_Cast_And_Crew_Tab_Clicked", attachment_type=AttachmentType.PNG)

            # Step 6: Click Cast and Crew Detail (Artist)
            self.click(By.XPATH, xpaths["cast_and_crew_details"], "09_Cast_And_Crew_Details")
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="09_Cast_And_Crew_Details_Clicked", attachment_type=AttachmentType.PNG)

            print("✅ Test completed: Cast & Crew flow")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")
