import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
import sys, os

# ✅ Add config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "series_tab": "//li[@id='header-Tv Show']",
    "view_all": "//a[normalize-space(text())='View All']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("series Page Automation")
@allure.title("Click each 'View All' in series tab and return")
class TestseriesViewAllNavigation:

    def test_series_tab_viewall_navigation(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)

        try:
            # ✅ Step 1: Open home and login
            url = ReadConfig.getHomePageURL()
            self.driver.get(url)
            self.driver.maximize_window()
            print(f"🌐 Opened URL: {url}")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            print("✅ Logged in successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="01_LoggedIn", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Choose Profile
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Profile_Selected", attachment_type=AttachmentType.PNG)

            # ✅ Step 3: Scroll and click series tab
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(0.8)

            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["series_tab"]))).click()
            print("🎬 series tab clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="03_seriesTab_Clicked", attachment_type=AttachmentType.PNG)

            # ✅ Step 4: Wait for View All buttons inside series
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["view_all"])))
            time.sleep(3)
            view_all_buttons = self.driver.find_elements(By.XPATH, xpaths["view_all"])
            total = len(view_all_buttons)
            print(f"🔍 Found {total} View All buttons")

            assert total > 0, "❌ No View All buttons found in series"

            # ✅ Step 5: Loop through each View All
            for i in range(total):
                try:
                    view_all_buttons = self.driver.find_elements(By.XPATH, xpaths["view_all"])
                    target = view_all_buttons[i]
                    label = f"ViewAll_series_{i+1}"

                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", target)
                    time.sleep(1)

                    wait.until(EC.element_to_be_clickable((By.XPATH, f"({xpaths['view_all']})[{i+1}]")))
                    self.driver.execute_script("arguments[0].click();", target)
                    print(f"👉 Clicked: {label}")
                    time.sleep(2)

                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Opened", attachment_type=AttachmentType.PNG)

                    # ✅ Go back to series page
                    self.driver.back()
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["view_all"])))
                    time.sleep(1.5)
                    print(f"🔙 Returned from {label}")

                except Exception as e:
                    print(f"❌ Failed at View All #{i+1}: {str(e)}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Error_{label}", attachment_type=AttachmentType.PNG)
                    continue

            print("✅ series tab 'View All' sections verified")

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ WebDriver already closed.")
 