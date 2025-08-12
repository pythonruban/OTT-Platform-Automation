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
    "live_tab": "//li[@id='header-Live']",
    "categories_section": "//div[@class='card-image-container']",
    "video_tile": "//div[@class='homeListImage active']",
    "comment_tab": "//li[@id='live-tab-3']",
    "comment_input": "comment-textarea",
    "post_btn": "post-comment-button"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Live Module - Add & Edit Comment")
@allure.title("Post and Edit a Comment in Live Section")
class TestLiveCommentEdit:

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
            raise AssertionError(f"Failed to click {label}: {e}")

    def test_add_and_edit_comment(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            with allure.step("Step 1: Launch Site and Login"):
                self.driver.get(ReadConfig.getHomePageURL())
                self.driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
                self.wait_and_click(By.XPATH, xpaths["login_btn"], "Login Button")
                self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            with allure.step("Step 2: Go to Live → View All → Category → First Video"):
                self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab")
                view_all = "(//a[contains(text(), 'View All')])[2]"
                self.wait_and_click(By.XPATH, view_all, "View All Button")

            with allure.step("Step 3: Enter Live Category"):
                categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
                assert categories, "❌ No live categories found."
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", categories[0])
                categories[0].click()
                time.sleep(3)

            with allure.step("Step 4: Play First Video"):
                videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tile"])))
                assert videos, "❌ No videos found in category."
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[0])
                videos[0].click()
                time.sleep(3)

            with allure.step("Step 5: Add a Comment"):
                self.wait_and_click(By.XPATH, xpaths["comment_tab"], "Comment Tab")
                comment_box = wait.until(EC.presence_of_element_located((By.ID, xpaths["comment_input"])))
                comment_box.clear()
                comment_box.send_keys("Nice video 👍")
                self.driver.find_element(By.ID, xpaths["post_btn"]).click()
                print("💬 Comment posted.")
                allure.attach(self.driver.get_screenshot_as_png(), name="Comment_Posted", attachment_type=AttachmentType.PNG)
                time.sleep(3)

            with allure.step("Step 6: Edit Last Comment"):
                containers = self.driver.find_elements(By.XPATH, "//div[starts-with(@id,'dropdown-container-')]")
                assert containers, "❌ No dropdowns found for comment actions."
                comment_index = containers[-1].get_attribute("id").split("-")[-1]

                dropdown_id = f"dropdown-toggle-{comment_index}"
                edit_btn_id = f"edit-button-{comment_index}"
                edit_input_id = f"edit-comment-textarea-{comment_index}"
                update_btn_id = f"update-comment-button-{comment_index}"

                self.wait_and_click(By.ID, dropdown_id, "Dropdown Toggle")
                time.sleep(1)

                edit_btn = wait.until(EC.presence_of_element_located((By.ID, edit_btn_id)))
                self.driver.execute_script("arguments[0].click();", edit_btn)
                time.sleep(1)

                edit_input = wait.until(EC.presence_of_element_located((By.ID, edit_input_id)))
                edit_input.clear()
                edit_input.send_keys("🔥 Edited comment by automation")
                self.driver.find_element(By.ID, update_btn_id).click()
                print("✏️ Comment edited.")
                allure.attach(self.driver.get_screenshot_as_png(), name="Comment_Edited", attachment_type=AttachmentType.PNG)
                time.sleep(3)

            with allure.step("Step 7: Toast Confirmation"):
                toast = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast")))
                print("✅ Toast message appeared.")
                allure.attach(self.driver.get_screenshot_as_png(), name="Toast_Visible", attachment_type=AttachmentType.PNG)
                time.sleep(2)
                try:
                    toast.find_element(By.CLASS_NAME, "Toastify__close-button").click()
                    print("ℹ️ Toast closed manually.")
                except Exception as e:
                    print(f"⚠️ Toast auto-closed or no close button: {e}")

            assert "Edited comment by automation" in self.driver.page_source, "❌ Comment edit verification failed."

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"Test Failed: {e}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"⚠️ Driver already closed: {e}")
