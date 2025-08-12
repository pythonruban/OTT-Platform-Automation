import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # 🛠️ Config for URL, email, password

# XPath mappings
xpaths = {
    # Login
    "login_icon": "//button[@id='home-signin']",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    # Profile Navigation
    "profile_avatar": "//img[@alt='RK']",
    "my_profile_link": "//a[@id='my-profile']",

    # Form Fields
    "name": "//input[@id='nameprofile']",
    "last_name": "//input[@name='last_name']",
    "update_btn": "//button[@id='handleUpdate-profile']"
}

base_url = ReadConfig.getHomePageURL()

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Profile Management")
@allure.title("Update Personal Information in My Profile")
class TestUpdateMyProfile:

    def test_my_profile_update(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        def click(by, locator, label, scroll=True):
            try:
                elem = wait.until(EC.presence_of_element_located((by, locator)))
                if scroll:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                    time.sleep(1)
                wait.until(EC.element_to_be_clickable((by, locator))).click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Open Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)
            print("🏠 Homepage loaded")

            # Step 2: Login with Config
            click(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            allure.attach(self.driver.get_screenshot_as_png(), name="Credentials_Entered", attachment_type=AttachmentType.PNG)
            click(By.XPATH, xpaths["login_btn"], "Login Button")

            # Step 3: Choose Profile
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 4: Go to My Profile
            click(By.XPATH, xpaths["profile_avatar"], "Profile Avatar (TT)")
            click(By.XPATH, xpaths["my_profile_link"], "My Profile Link")

            # Step 5: Fill Form
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["name"]))).clear()
            self.driver.find_element(By.XPATH, xpaths["name"]).send_keys("ruban")

            self.driver.find_element(By.XPATH, xpaths["last_name"]).clear()
            self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("k")
            time.sleep(1)

            allure.attach(self.driver.get_screenshot_as_png(), name="Form_Filled", attachment_type=AttachmentType.PNG)

            # Step 6: Click Update
            click(By.XPATH, xpaths["update_btn"], "Update Button")

            # Step 7: Final Check
            print("✅ Profile updated successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="Profile_Updated", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, str(e)

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
