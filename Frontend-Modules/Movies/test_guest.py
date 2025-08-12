import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Importing your config utility

# 🔍 Define all required XPaths
xpaths = {
    "live_tab": "//li[@id='header-Live']",
    "category_tiles": "//div[@class='card-image-container']",
    "video_tiles": "//div[@class='homeListImage active']",
    "watch_now": "//button[@id='watch-now-button']",
    "iframe": "//iframe",
    "play_button": '//button[@class="ytp-large-play-button ytp-button"]'
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest - Live Module")
@allure.title("Watch Live Videos - Guest Across All Categories")
class TestGuestLiveAllCategories:

    def click(self, by, locator, label, timeout=30):
        """Reusable click with screenshot logging and scrolling."""
        wait = WebDriverWait(self.driver, timeout)
        try:
            with allure.step(f"Click: {label}"):
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
                elem.click()
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label} — {e}")

    def test_guest_live_video_all_categories(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            # Step 1: Open Homepage
            with allure.step("Open Homepage"):
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Click Live Tab
            self.click(By.XPATH, xpaths["live_tab"], "Live Tab")

            # Step 3: Loop through each category
            categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["category_tiles"])))
            for cat_index in range(len(categories)):
                try:
                    self.driver.get(base_url)
                    self.click(By.XPATH, xpaths["live_tab"], f"Live Tab - Category {cat_index + 1}")
                    categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["category_tiles"])))
                    categories[cat_index].click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{cat_index+1}_Opened", attachment_type=AttachmentType.PNG)
                    time.sleep(2)

                    # Step 4: Loop through videos in that category
                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tiles"])))
                    for vid_index in range(len(videos)):
                        try:
                            videos = self.driver.find_elements(By.XPATH, xpaths["video_tiles"])
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", videos[vid_index])
                            videos[vid_index].click()
                            time.sleep(2)

                            # Check for Watch Now button
                            watch_now_btns = self.driver.find_elements(By.XPATH, xpaths["watch_now"])
                            if not watch_now_btns:
                                self.driver.back()
                                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["video_tiles"])))
                                continue

                            watch_now_btns[0].click()
                            time.sleep(3)

                            # Play the iframe video
                            iframe = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["iframe"])))
                            self.driver.switch_to.frame(iframe)
                            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["play_button"])))
                            play_btn.click()
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{cat_index}_{vid_index}_Playing", attachment_type=AttachmentType.PNG)
                            print(f"🎥 Playing video {vid_index+1} in category {cat_index+1}")
                            self.driver.switch_to.default_content()

                        except Exception as ve:
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{cat_index}_{vid_index}_Error", attachment_type=AttachmentType.PNG)
                            print(f"⚠️ Video play failed: Category {cat_index+1} → Video {vid_index+1} → {ve}")
                            self.driver.switch_to.default_content()
                            self.driver.get(base_url)
                            break

                        self.driver.get(base_url)

                except Exception as ce:
                    print(f"⚠️ Skipping Category {cat_index+1} due to error: {ce}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{cat_index+1}_Error", attachment_type=AttachmentType.PNG)
                    self.driver.get(base_url)
                    continue

        except Exception as e:
            print(f"❌ Test failed due to critical error: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Critical_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"Test Failed: {e}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
