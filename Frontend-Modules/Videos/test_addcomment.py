import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Assumes config import works

xpaths = {
    "login_icon": "//button[@id='home-signin'] | (//button[@type='button'])[1]",  # Fallback for login icon
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "Categories_tab": "//li[@id='header-Categories']",
    "categories_section": "//div[@class='card-image-container']",
    "video_tile": "//div[@class='homeListImage active']",
    "comment_tab": "//li[@id='video-tab-3']",
    "comment_input": "comment-textarea",
    "post_btn": "post-comment-button"
}

@pytest.mark.usefixtures("browser_setup")
class TestLiveCommentAutomation:

    def wait_and_click(self, by, value, label, wait=30):
        try:
            WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((by, value)))
            elem = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located((by, value)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable((by, value)))
            time.sleep(1)
            elem.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
            time.sleep(3)
        except Exception as e:
            print(f"❌ Failed: {label} - {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Error", attachment_type=AttachmentType.PNG)
            raise

    def test_live_comment_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            # ✅ Step 1: Open homepage
            with allure.step("Step 1: Open Website"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["login_icon"])))  # ensure loaded
                allure.attach(self.driver.get_screenshot_as_png(), name="01_Home_Loaded", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Login
            with allure.step("Step 2: Login Flow"):
                self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
                wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                self.wait_and_click(By.XPATH, xpaths["login_btn"], "Login Submit")

            # ✅ Step 3: Choose Profile
            with allure.step("Step 3: Choose Profile"):
                self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # ✅ Step 4: Click Live Tab
            with allure.step("Step 4: Click Live Tab"):
                self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab")

                view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
                wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

            # ✅ Step 5: Loop Live Categories
            categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
            print(f"📂 Found {len(categories)} Live Categories")

            for i in range(len(categories)):
                try:
                    print(f"\n➡️ Category {i+1}")
                    categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
                    category = categories[i]
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", category)
                    time.sleep(2)
                    category.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{i+1}_Clicked", attachment_type=AttachmentType.PNG)
                    time.sleep(4)

                    # ✅ Step 6: Click first video
                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tile"])))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[0])
                    time.sleep(2)
                    videos[0].click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_Category_{i+1}", attachment_type=AttachmentType.PNG)
                    time.sleep(4)

                    # ✅ Step 7: Click Comment Tab
                    self.wait_and_click(By.XPATH, xpaths["comment_tab"], "Comment Tab")

                    # ✅ Step 8: Post comment
                    comment_box = wait.until(EC.visibility_of_element_located((By.ID, xpaths["comment_input"])))
                    comment_box.clear()
                    comment_box.send_keys("Nice video from automation!")
                    time.sleep(1)
                    self.driver.find_element(By.ID, xpaths["post_btn"]).click()
                    print(f"💬 Comment posted in Category {i+1}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Comment_Posted_{i+1}", attachment_type=AttachmentType.PNG)
                    time.sleep(3)

                    # ✅ Step 9: Go back to Live
                    self.driver.back()
                    self.driver.back()
                    time.sleep(4)
                    self.wait_and_click(By.XPATH, xpaths["live_tab"], f"Reload Live Tab {i+1}")

                except TimeoutException as te:
                    print(f"⚠️ Timeout in Category {i+1}: {te}")
                    self.driver.get(ReadConfig.getHomePageURL())
                    self.wait_and_click(By.XPATH, xpaths["live_tab"], f"Live Tab Retry {i+1}")
                    continue
                except Exception as e:
                    print(f"❌ Error in category {i+1}: {e}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{i+1}_Error", attachment_type=AttachmentType.PNG)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
