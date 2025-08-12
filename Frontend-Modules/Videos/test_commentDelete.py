import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "//button[@id='home-signin'] | (//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "Categories_tab": "//li[@id='header-Categories']",
    "categories_section": "//div[@class='card-image-container']",
    "video_tile": "//div[@class='homeListImage active']",
    "comment_tab": "//li[@id='Categories-tab-3']",
    "comment_input": "comment-textarea",
    "post_btn": "post-comment-button"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Categories Comment Post & Delete")
@allure.title("Post a Categories Comment & Delete via Detected Index")
class TestCategoriesPostDeleteComment:

    def wait_and_click(self, by, value, label, wait=25):
        try:
            WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((by, value)))
            elem = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located((by, value)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable((by, value)))
            time.sleep(1)
            elem.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            print(f"❌ Failed to click {label}: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Error", attachment_type=AttachmentType.PNG)
            raise

    def test_Categories_comment_post_and_delete(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            with allure.step("Step 1: Open and Login"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                self.wait_and_click(By.XPATH, xpaths["login_btn"], "Login Button")
                self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            with allure.step("Step 2: Navigate to Categories Category and Play First Video"):
                self.wait_and_click(By.XPATH, xpaths["Categories_tab"], "Categories Tab")
                view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
                wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()
                categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
                if not categories:
                    raise Exception("❌ No Categories categories found.")
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", categories[0])
                categories[0].click()
                time.sleep(3)

                videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tile"])))
                if not videos:
                    raise Exception("❌ No videos found in selected category.")
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[0])
                videos[0].click()
                time.sleep(4)

            with allure.step("Step 3: Post a Comment"):
                self.wait_and_click(By.XPATH, xpaths["comment_tab"], "Comment Tab")
                comment_box = wait.until(EC.presence_of_element_located((By.ID, xpaths["comment_input"])))
                comment_box.clear()
                comment_box.send_keys("🔥 Test comment by automation")
                self.driver.find_element(By.ID, xpaths["post_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Comment_Posted", attachment_type=AttachmentType.PNG)
                print("💬 Comment posted")
                time.sleep(3)

            with allure.step("Step 4: Detect & Delete Posted Comment"):
                containers = self.driver.find_elements(By.XPATH, "//div[starts-with(@id,'dropdown-container-')]")
                if not containers:
                    raise Exception("❌ No dropdown containers found for comment options.")

                comment_index = containers[0].get_attribute("id").split("-")[-1]
                print(f"🎯 Found Comment Index: {comment_index}")

                dropdown = wait.until(EC.element_to_be_clickable((By.ID, f"dropdown-toggle-{comment_index}")))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
                dropdown.click()
                time.sleep(1)

                delete_btn = wait.until(EC.element_to_be_clickable((By.ID, f"delete-button-{comment_index}")))
                delete_btn.click()
                print("🗑️ Clicked Delete")

            with allure.step("Step 5: Confirm Alert"):
                try:
                    WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    print("🔔 Alert Text:", alert.text)
                    alert.accept()
                    print("✅ Alert accepted")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Alert_Accepted", attachment_type=AttachmentType.PNG)
                except Exception:
                    raise AssertionError("❌ Alert confirmation not shown")

            with allure.step("Step 6: Toast Verification"):
                toast = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast")))
                print("✅ Toast appeared for deletion")
                allure.attach(self.driver.get_screenshot_as_png(), name="Toast_Appearance", attachment_type=AttachmentType.PNG)
                time.sleep(2)

        except Exception as e:
            print(f"❌ Test failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(str(e))

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
