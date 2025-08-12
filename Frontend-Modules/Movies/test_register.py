import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    "live_tab": "//li[@id='header-Live']",
    "category_tiles": "//div[@class='card-image-container']",
    "video_tiles": "//div[@class='homeListImage active']",
    "watch_now": "//button[@id='watch-now-button']",
    "iframe": "//iframe",
    "play_button": '//button[@class="ytp-large-play-button ytp-button"]'
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Live Video Playback")
@allure.title("Login → Click Live → Loop Categories → Watch Videos with Screenshot")
class TestLoginAndLiveVideo:

    def test_login_and_watch_all_live_videos(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        def click(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", elem)
                    time.sleep(1)
                    elem.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
                    print(f"✅ Clicked: {label}")
                    time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Homepage
            self.driver.get(ReadConfig.getHomePageURL())
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            allure.attach(self.driver.get_screenshot_as_png(), name="01_Homepage_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Login
            click(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            click(By.XPATH, xpaths["login_btn"], "Login Button")
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Go to Live Tab
            click(By.XPATH, xpaths["live_tab"], "Live Tab")

            categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["category_tiles"])))
            print(f"📁 Found {len(categories)} categories")

            for cat_index in range(len(categories)):
                with allure.step(f"Category {cat_index}"):
                    categories = self.driver.find_elements(By.XPATH, xpaths["category_tiles"])
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", categories[cat_index])
                    categories[cat_index].click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{cat_index}_Clicked", attachment_type=AttachmentType.PNG)
                    time.sleep(2)

                videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tiles"])))
                print(f"🎞 Found {len(videos)} videos in category {cat_index}")

                for vid_index in range(len(videos)):
                    with allure.step(f"Video {vid_index} in Category {cat_index}"):
                        try:
                            videos = self.driver.find_elements(By.XPATH, xpaths["video_tiles"])
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", videos[vid_index])
                            videos[vid_index].click()
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{vid_index}_Clicked", attachment_type=AttachmentType.PNG)
                            time.sleep(2)

                            # Watch Now
                            click(By.XPATH, xpaths["watch_now"], "Watch Now")

                            # Play in iframe
                            with allure.step("Switch to iframe and Play"):
                                iframe = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["iframe"])))
                                self.driver.switch_to.frame(iframe)
                                play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["play_button"])))
                                play_btn.click()
                                print("▶️ Video Played")
                                allure.attach(self.driver.get_screenshot_as_png(), name="Video_Playing", attachment_type=AttachmentType.PNG)
                                time.sleep(5)
                                self.driver.switch_to.default_content()

                        except Exception as e:
                            print(f"⚠️ Skipping video {vid_index} — {e}")
                            self.driver.get(ReadConfig.getHomePageURL())
                            click(By.XPATH, xpaths["live_tab"], "Return to Live Tab")
                            categories = self.driver.find_elements(By.XPATH, xpaths["category_tiles"])
                            categories[cat_index].click()
                            time.sleep(2)
                            continue

                # After each category, reload Live tab
                self.driver.get(ReadConfig.getHomePageURL())
                click(By.XPATH, xpaths["live_tab"], "Live Tab Reload")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test Failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Browser already closed.")
