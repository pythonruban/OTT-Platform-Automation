import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
import sys, os

# ✅ Add config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# ✅ All XPaths and IDs
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "series_tab": "//li[@id='header-Tv Show']",
    "view_all_3": "(//a[text()='View All'])[3]",
    "series_category_id": "series-genre-5",
    "video_block_id": "shows-5",
    "watch_now_btn": "watch-now-button",
    "watch_now_btn": "watch-now-button"

}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest Episode Watch")
@allure.title("Guest watches episode through series category flow")
class TestGuestUserEpisodeWatch:

    def test_guest_episode_watch(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        self.driver.get(ReadConfig.getHomePageURL())
        self.driver.maximize_window()
        time.sleep(2)

        def click(by, locator, label, js_scroll=True):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                if js_scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", elem)
                    time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)        
                time.sleep(2)
            except Exception as e:
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {str(e)}")

        try:
            # Step 1: Login
            click(By.XPATH, xpaths["login_icon"], "01_Login_Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Submitted", attachment_type=AttachmentType.PNG)

            # Step 2: Choose Profile
            click(By.XPATH, xpaths["choose_profile"], "03_Profile_Chosen")
            time.sleep(2)

            # Step 3: Series Tab
            click(By.XPATH, xpaths["series_tab"], "04_Series_Tab")
            time.sleep(2)

            # Step 4: View All (3rd)
            click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")
            time.sleep(2)

            # Step 5: Click Series Category
            click(By.ID, xpaths["series_category_id"], "06_Series_Category")
            time.sleep(3)

            # Step 6: Click show (no scroll, JS click)
            try:
                show_elem = wait.until(EC.presence_of_element_located((By.ID, xpaths["video_block_id"])))
                self.driver.execute_script("arguments[0].click();", show_elem)
                print("✅ Show clicked via JS click")
                time.sleep(5)
                allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Clicked", attachment_type=AttachmentType.PNG)

                # Optional: Switch to new tab if opened
                if len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    print("🆕 Switched to new tab")
                    time.sleep(5)
                    allure.attach(self.driver.get_screenshot_as_png(), name="07_Tab_Switched", attachment_type=AttachmentType.PNG)

            except Exception as e:
                time.sleep(5)
                allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Click_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click show via JS: {str(e)}")

            # Step 7: Watch Now
            click(By.ID, xpaths["watch_now_btn"], "08_WatchNow_1")

             # Step 8: Watch Now
            click(By.ID, xpaths["watch_now_btn"], "08_WatchNow_1")

            # Step 8: Optionally click second Watch Now
            try:
                second = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, xpaths["watch_now_btn"])))
                self.driver.execute_script("arguments[0].click();", second)
                time.sleep(5)
                allure.attach(self.driver.get_screenshot_as_png(), name="09_WatchNow_2", attachment_type=AttachmentType.PNG)
                print("⏭️ Second Watch Now clicked")
            except:
                print("ℹ️ Second Watch Now not available")

            print("✅ Guest episode watch flow completed")

        except Exception as e:
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test Failed: {str(e)}")

        finally:
            self.driver.quit()
