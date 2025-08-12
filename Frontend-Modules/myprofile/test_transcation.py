import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# ✅ Config values
base_url = ReadConfig.getHomePageURL()
user_email = ReadConfig.getTestingemail()
user_password = ReadConfig.getTestpassword()

# ✅ XPath dictionary
xpaths = {
    # Login
    "login_icon": "//button[@id='home-signin']",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    # Profile
    "profile_avatar": "//img[@alt='RK']",
    "my_profile": "//a[@id='my-profile']",
    "billing_tab": "//span[text()='Transaction History']"
}

# ✅ Click helper function
def click(driver, wait, by, locator, label, scroll=True):
    try:
        elem = wait.until(EC.presence_of_element_located((by, locator)))
        if scroll:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
            time.sleep(1)
        wait.until(EC.element_to_be_clickable((by, locator))).click()
        print(f"✅ Clicked: {label}")
        allure.attach(driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
        time.sleep(2)
    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
        raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

# ✅ Reusable login flow
def login_flow(driver, wait):
    # Open homepage
    driver.get(base_url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("🌐 Homepage loaded")
    allure.attach(driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

    # Click login
    click(driver, wait, By.XPATH, xpaths["login_icon"], "Login Icon")
    
    # Enter email/password and login
    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(user_email)
    driver.find_element(By.XPATH, xpaths["password"]).send_keys(user_password)
    driver.find_element(By.XPATH, xpaths["login_btn"]).click()
    print("✅ Logged in")
    allure.attach(driver.get_screenshot_as_png(), name="LoggedIn", attachment_type=AttachmentType.PNG)

    # Choose profile
    click(driver, wait, By.XPATH, xpaths["choose_profile"], "Choose Profile")

@pytest.mark.usefixtures("browser_setup")
@allure.feature("My Profile > Billing Tab")
@allure.title("Navigate to Billing Tab in My Profile Section")
class TestGoToBillingTab:

    def test_billing_navigation(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            # ✅ Step 1–4: Login and choose profile
            login_flow(self.driver, wait)

            # ✅ Step 5: Click avatar (TT or RK)
            click(self.driver, wait, By.XPATH, xpaths["profile_avatar"], "Profile Avatar")

            # ✅ Step 6: Click My Profile
            click(self.driver, wait, By.XPATH, xpaths["my_profile"], "My Profile")

            # ✅ Step 7: Click Billing Tab
            click(self.driver, wait, By.XPATH, xpaths["billing_tab"], "Billing Tab")

            print("✅ Billing tab opened successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="Billing_Page_Opened", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed: {str(e)}"

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
