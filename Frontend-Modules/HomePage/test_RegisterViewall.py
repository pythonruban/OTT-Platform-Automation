import sys
import os
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from allure_commons.types import AttachmentType

# ✅ Import config reader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestLoginAndClickAllViewAll:

    def test_login_and_click_all_sections(self, browser_setup):
        self.driver = browser_setup
        self.wait = WebDriverWait(self.driver, 20)
        actions = ActionChains(self.driver)

        # XPaths
        signin_button = "//button[@id='home-signin']"
        email = "//input[@id='signin-email']"
        password = "//input[@id='signin-password']"
        login_submit = "//button[@id='signin-submit']"
        choose_profile = "(//img[@alt='Avatar'])[1]"
        view_all_xpath = "//a[.//span[normalize-space(text())='View All']]"

        try:
            # ✅ Step 1: Open website
            url = ReadConfig.getHomePageURL()
            self.driver.get(url)
            self.driver.maximize_window()
            print("🌐 Website opened")
            allure.attach(self.driver.get_screenshot_as_png(), name="01_Homepage_Opened", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Login
            self.wait.until(EC.element_to_be_clickable((By.XPATH, signin_button))).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, email))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, password).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, login_submit).click()
            print("✅ Logged in")
            allure.attach(self.driver.get_screenshot_as_png(), name="02_After_Login", attachment_type=AttachmentType.PNG)

            # ✅ Step 3: Choose profile if needed
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, choose_profile))).click()
                print("✅ Profile selected")
                allure.attach(self.driver.get_screenshot_as_png(), name="03_Profile_Selected", attachment_type=AttachmentType.PNG)
            except:
                print("⚠️ Profile selection skipped")

            # ✅ Step 4: Wait for homepage view all buttons
            print("⏳ Waiting for 'View All' elements...")
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, view_all_xpath)))
            view_all_elements = self.driver.find_elements(By.XPATH, view_all_xpath)
            print(f"🔎 Found {len(view_all_elements)} 'View All' buttons")
            allure.attach(self.driver.get_screenshot_as_png(), name="viewall_Inside_Page", attachment_type=AttachmentType.PNG)

            if not view_all_elements:
                raise Exception("❌ No 'View All' buttons found on the homepage.")

            # ✅ Step 5: Iterate through all View All buttons
            for index in range(len(view_all_elements)):
                section_text = f"ViewAll_{index + 1}"
                try:
                    # Re-fetch elements to avoid stale
                    view_all_elements = self.driver.find_elements(By.XPATH, view_all_xpath)
                    element = view_all_elements[index]

                    # Scroll into view and wait for visibility
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                    self.wait.until(EC.visibility_of(element))

                    print(f"👉 Clicking: {section_text}")
                    self.driver.execute_script("arguments[0].click();", element)

                    # ✅ Step 6: Wait inside view page
                    self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(5)  # Wait 5 seconds before going back
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"viewall_Inside_Page", attachment_type=AttachmentType.PNG)

                    # 🔙 Step 7: Go back
                    self.driver.back()

                    # ✅ Step 8: Wait for homepage to reload
                    self.wait.until(EC.presence_of_all_elements_located((By.XPATH, view_all_xpath)))
                    print(f"🔙 Returned from: {section_text}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"viewall_Inside_Page_Returned_Home", attachment_type=AttachmentType.PNG)

                    # Optional: scroll down a bit
                    self.driver.execute_script("window.scrollBy(0, 400);")

                except Exception as e:
                    print(f"❌ Failed at {section_text} | Error: {e}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{section_text}_Error", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print("❌ General Error:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="99_Fatal_Error", attachment_type=AttachmentType.PNG)
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver not initialized.")
