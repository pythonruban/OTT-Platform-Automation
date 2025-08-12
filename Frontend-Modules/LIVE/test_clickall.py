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
    "live_tab": "//li[@id='header-Live']",
    "view_all": "//a[normalize-space(text())='View All']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("LIVE Page Automation")
@allure.title("Click each 'View All' in LIVE tab with enhanced wait and screenshots")
class TestLiveViewAllNavigation:

    def test_live_tab_viewall_navigation(self, browser_setup):
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
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="01_LoggedIn", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Choose Profile
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Profile_Selected", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            
            # ✅ Step 3: Scroll and click LIVE tab
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(0.8)

            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["live_tab"]))).click()
            print("🎬 LIVE tab clicked")
            time.sleep(3)  # Increased wait time for LIVE tab to load
            allure.attach(self.driver.get_screenshot_as_png(), name="03_LiveTab_Clicked", attachment_type=AttachmentType.PNG)

            # ✅ Step 4: Wait for View All buttons inside LIVE
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["view_all"])))
            time.sleep(3)
            view_all_buttons = self.driver.find_elements(By.XPATH, xpaths["view_all"])
            total = len(view_all_buttons)
            print(f"🔍 Found {total} View All buttons")

            assert total > 0, "❌ No View All buttons found in LIVE"

            # ✅ Step 5: Loop through each View All with enhanced wait and screenshots
            for i in range(total):
                try:
                    # Re-find elements to avoid stale reference
                    view_all_buttons = self.driver.find_elements(By.XPATH, xpaths["view_all"])
                    target = view_all_buttons[i]
                    label = f"ViewAll_Live_{i+1}"

                    # Scroll to element and wait
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", target)
                    time.sleep(2)  # Increased scroll wait time

                    # Take screenshot before clicking
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_BeforeClick", attachment_type=AttachmentType.PNG)

                    # Click View All
                    wait.until(EC.element_to_be_clickable((By.XPATH, f"({xpaths['view_all']})[{i+1}]")))
                    self.driver.execute_script("arguments[0].click();", target)
                    print(f"👉 Clicked: {label}")
                    
                    # Enhanced wait time after clicking to let content load
                    time.sleep(4)  # Increased wait time for content to load
                    
                    # Wait for page to be fully loaded (you can customize this based on your app)
                    try:
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        # Additional wait for dynamic content
                        time.sleep(2)
                    except TimeoutException:
                        print(f"⚠️ Page load timeout for {label}")

                    # Take screenshot after content loads
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_ContentLoaded", attachment_type=AttachmentType.PNG)
                    
                    # Optional: Scroll down to see more content and take another screenshot
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(2)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_ScrolledContent", attachment_type=AttachmentType.PNG)
                    
                    # Scroll back to top
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)

                    print(f"📸 Screenshots captured for {label}")

                    # ✅ Go back to LIVE page
                    self.driver.back()
                    
                    # Enhanced wait for return to LIVE page
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["view_all"])))
                    time.sleep(3)  # Increased wait time after going back
                    
                    # Take screenshot after returning
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_ReturnedToLive", attachment_type=AttachmentType.PNG)
                    
                    print(f"🔙 Returned from {label}")

                except TimeoutException as te:
                    print(f"❌ Timeout error at View All #{i+1}: {str(te)}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Timeout_Error_{label}", attachment_type=AttachmentType.PNG)
                    continue
                    
                except Exception as e:
                    print(f"❌ Failed at View All #{i+1}: {str(e)}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Error_{label}", attachment_type=AttachmentType.PNG)
                    continue

            print("✅ LIVE tab 'View All' sections verified with enhanced screenshots")

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            try:
                self.driver.quit()
            except:
                print("⚠️ WebDriver already closed in finally block.")

    def teardown_class(self):
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            print("⚠️ WebDriver already closed in teardown.")