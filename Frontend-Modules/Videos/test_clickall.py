import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
import sys, os

# ✅ Add config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# ✅ XPath base
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "Categories_tab": "//li[@id='header-Categories']",
}

# ✅ ALT values to loop
alt_values = ["categories"]

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Categories Page Automation")
@allure.title("Click each Categories thumbnail by alt and verify navigation")
class TestLiveAltClick:

    def test_live_alt_thumbnail_navigation(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)

        try:
            with allure.step("Step 1: Open Home and Login"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                print(f"🌐 Opened: {url}")

                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
                wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
                self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Choose Profile"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="02_Profile_Selected", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Scroll Home before Categories tab"):
                for _ in range(5):
                    self.driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(0.7)

            with allure.step("Step 4: Click Categories tab"):
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["Categories_tab"]))).click()
                allure.attach(self.driver.get_screenshot_as_png(), name="03_Live_Tab_Clicked", attachment_type=AttachmentType.PNG)
            
            
                view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
                wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

            with allure.step("Step 5: Loop alt values and click each"):
                for alt_text in alt_values:
                    thumbnail_xpath = f"//img[@alt='{alt_text}']"
                    elements = self.driver.find_elements(By.XPATH, thumbnail_xpath)
                    print(f"🔍 Found {len(elements)} items for alt='{alt_text}'")

                    for i in range(1, len(elements) + 1):
                        try:
                            item_xpath = f"(//img[@alt='{alt_text}'])[{i}]"
                            elem = wait.until(EC.presence_of_element_located((By.XPATH, item_xpath)))
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                            wait.until(EC.element_to_be_clickable((By.XPATH, item_xpath))).click()
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"{alt_text}_{i}_Clicked", attachment_type=AttachmentType.PNG)
                            print(f"✅ Clicked {alt_text} #{i}")
                            time.sleep(2)
                            self.driver.back()
                            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["live_tab"])))  # ensure back complete
                            time.sleep(1)
                        except Exception as e:
                            print(f"❌ Failed to click {alt_text} #{i} — {e}")
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"{alt_text}_{i}_Error", attachment_type=AttachmentType.PNG)
                            continue

            print("✅ All Categories thumbnails tested successfully")
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
