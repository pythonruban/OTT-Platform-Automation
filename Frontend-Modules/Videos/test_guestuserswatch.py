import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # Import config reader
xpaths = {
    "Categories_tab": "//li[@id='header-Categories']",
    "category_tiles": "//div[@class='card-image-container']",
    "video_tiles": "//div[@class='homeListImage active']",
    "watch_now": "//button[@id='watch-now-button']",
    "iframe": "//iframe",
    "play_button": '//button[@class="ytp-large-play-button ytp-button"]'
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest - Watch Categories Videos All Categories")
@allure.title("Guest user watches videos across all Categories categories")
class TestGuestCategoriesAllCategories:

    def test_guest_Categories_video_all_categories(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", elem)
                    elem.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"Failed to click {label} — {str(e)}")

        try:
            with allure.step("Load Homepage"):
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            click(By.XPATH, xpaths["Categories_tab"], "Categories Tab")
            view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
            wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

            categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["category_tiles"])))
            for cat_index in range(len(categories)):
                try:
                    self.driver.get(base_url)
                    click(By.XPATH, xpaths["Categories_tab"], f"Categories Tab - Category {cat_index + 1}")
                    categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["category_tiles"])))
                    categories[cat_index].click()

                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tiles"])))
                    for vid_index in range(len(videos)):
                        try:
                            videos = self.driver.find_elements(By.XPATH, xpaths["video_tiles"])
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", videos[vid_index])
                            videos[vid_index].click()

                            watch_btns = self.driver.find_elements(By.XPATH, xpaths["watch_now"])
                            if not watch_btns:
                                self.driver.back()
                                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["video_tiles"])))
                                continue

                            watch_btns[0].click()

                            iframe = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["iframe"])))
                            self.driver.switch_to.frame(iframe)
                            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["play_button"])))
                            play_btn.click()
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{cat_index}_{vid_index}_Playing", attachment_type=AttachmentType.PNG)
                            self.driver.switch_to.default_content()

                        except Exception as ve:
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{cat_index}_{vid_index}_Error", attachment_type=AttachmentType.PNG)
                            try:
                                self.driver.switch_to.default_content()
                            except:
                                pass
                            self.driver.get(base_url)
                            break  # Go to next category after failure

                        self.driver.get(base_url)  # Go back after each video

                except Exception as ce:
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{cat_index}_Error", attachment_type=AttachmentType.PNG)
                    self.driver.get(base_url)
                    continue

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"Test Failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            pass
