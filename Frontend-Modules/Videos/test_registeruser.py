import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Import config utility

xpaths = {
    "login_icon": "(//button[@id='home-signin'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "video_category_link": "//li[@id='header-Categories']",
    "genre_action": "//img[@alt='categories']",
    "episode_1": "//img[@alt='Leo Video Test']",
    "watch_now": "continue-watching-button"
}

@pytest.mark.usefixtures("browser_setup")
class TestWatchEpisode:

    def test_watch_episode_1(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()  # ✅ Get dynamic base URL

        def click_with_scroll(by, locator, label):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"fail_{label}", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Open Home Page
            self.driver.get(base_url)
            print("🌐 Waiting for login icon to appear...")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["login_icon"])))
            allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)
            time.sleep(2)

            # Step 2: Click login icon
            click_with_scroll(By.XPATH, xpaths["login_icon"], "Login Icon")

            # Step 3: Enter credentials and login
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
            allure.attach(self.driver.get_screenshot_as_png(), name="Credentials_Entered", attachment_type=AttachmentType.PNG)
            click_with_scroll(By.XPATH, xpaths["login_btn"], "Login Button")

            # Step 4: Choose Profile
            click_with_scroll(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 5: Navigate to Video Categories
            click_with_scroll(By.XPATH, xpaths["video_category_link"], "Video Categories")

            # Step 6: Click "Action" Genre
            click_with_scroll(By.XPATH, xpaths["genre_action"], "Action Genre")

            # Step 7: Click "Episode 1"
            click_with_scroll(By.XPATH, xpaths["episode_1"], "Episode 1")

            # Step 8: Click Watch Now
            print("🎬 Looking for 'Watch Now' button...")
            try:
                watch_btn = wait.until(EC.element_to_be_clickable((By.ID, xpaths["watch_now"])))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", watch_btn)
                time.sleep(2)
                watch_btn.click()
                print("▶️ Clicked: Watch Now")
                allure.attach(self.driver.get_screenshot_as_png(), name="WatchNow_Clicked", attachment_type=AttachmentType.PNG)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="fail_WatchNow", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click Watch Now — {str(e)}")

            # Step 9: Wait for video to play
            print("⏳ Waiting 5 seconds for video playback...")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="Video_Playing", attachment_type=AttachmentType.PNG)
            print("✅ Video played for 5 seconds.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test failed: {str(e)}"

        def teardown_class(self):
            try:
                self.driver.quit()
            except AttributeError:
                print("⚠️ Driver was not initialized.")
