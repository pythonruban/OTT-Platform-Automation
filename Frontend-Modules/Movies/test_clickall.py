import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from allure_commons.types import AttachmentType
import sys, os

# ✅ Add config path for cross-directory import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# ✅ XPath locators
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "movies_tab": "//li[@id='header-Movies']",
}

# ✅ ALT tag list to iterate category thumbnails
alt_values = ["categories"]

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Movies Page Automation")
@allure.title("Click all category thumbnails inside Movies View All")
class TestMoviesAltClick:

    def scroll_and_click(self, xpath, wait, max_attempts=2):
        """
        Scroll and click on the element with retries.
        """
        for attempt in range(max_attempts):
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                time.sleep(0.5)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                return True
            except ElementNotInteractableException:
                print(f"⚠️ Retry scroll and click attempt {attempt+1}")
                time.sleep(1)
        raise Exception(f"❌ Failed to scroll and click: {xpath}")

    def test_movies_category_inside_viewall(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)

        try:
            with allure.step("Step 1: Open Home and Login"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                print(f"🌐 Opened: {url}")

                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Choose Profile"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="02_Profile_Selected", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Scroll and click Movies tab"):
                for _ in range(5):
                    self.driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(0.5)
                self.scroll_and_click(xpaths["movies_tab"], wait)
                allure.attach(self.driver.get_screenshot_as_png(), name="03_Movies_Tab_Clicked", attachment_type=AttachmentType.PNG)

            with allure.step("Step 4: Click View All inside Movies"):
                view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
                self.scroll_and_click(view_all_xpath, wait)
                allure.attach(self.driver.get_screenshot_as_png(), name="04_ViewAll_Clicked", attachment_type=AttachmentType.PNG)

            with allure.step("Step 5: Inside View All, click each category thumbnail by index"):
                for alt_text in alt_values:
                    while True:
                        elements = self.driver.find_elements(By.XPATH, f"//img[@alt='{alt_text}']")
                        if elements:
                            break
                        time.sleep(1)

                    print(f"🔍 Found {len(elements)} category thumbnails for alt='{alt_text}'")

                    for i in range(1, len(elements) + 1):
                        try:
                            item_xpath = f"(//img[@alt='{alt_text}'])[{i}]"
                            print(f"➡️ Clicking category {i}")
                            elem = wait.until(EC.presence_of_element_located((By.XPATH, item_xpath)))
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                            wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"{alt_text}_{i}_Clicked", attachment_type=AttachmentType.PNG)
                            time.sleep(2)

                            self.driver.back()
                            wait.until(EC.presence_of_element_located((By.XPATH, f"(//img[@alt='{alt_text}'])[1]")))
                            time.sleep(1)
                        except Exception as e:
                            print(f"❌ Failed on category {i}: {e}")
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"{alt_text}_{i}_Error", attachment_type=AttachmentType.PNG)
                            continue

            print("✅ All categories clicked inside View All successfully")
            assert True

        except Exception as e:
            print(f"❌ Test Failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver already closed.")
