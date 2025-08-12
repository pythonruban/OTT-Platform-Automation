import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Config Reader

# ✅ Base URL from config
base_url = ReadConfig.getHomePageURL()

# ✅ XPaths
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

    # Active Device Tab
    "active_device_tab": "//a[@href='/myprofile/activedevice']"
}

# ✅ Reusable click helper
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
    driver.get(base_url)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("🌐 Homepage loaded")
    allure.attach(driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

    click(driver, wait, By.XPATH, xpaths["login_icon"], "Login Icon")

    wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
    driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
    allure.attach(driver.get_screenshot_as_png(), name="Credentials_Entered", attachment_type=AttachmentType.PNG)

    click(driver, wait, By.XPATH, xpaths["login_btn"], "Login Button")
    click(driver, wait, By.XPATH, xpaths["choose_profile"], "Choose Profile")

@pytest.mark.usefixtures("browser_setup")
@allure.feature("My Profile - Active Devices")
@allure.title("Navigate to Active Devices Tab from My Profile")
class TestGoToActiveDeviceTab:

    def test_active_device_tab(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            # ✅ Step 1–4: Login flow
            login_flow(self.driver, wait)

            # ✅ Step 5: Go to My Profile → Active Devices
            click(self.driver, wait, By.XPATH, xpaths["profile_avatar"], "Profile Avatar")
            click(self.driver, wait, By.XPATH, xpaths["my_profile"], "My Profile")
            click(self.driver, wait, By.XPATH, xpaths["active_device_tab"], "Active Device Tab")

            # ✅ Step 6: Scroll in Active Devices Page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Scrolled_Active_Device_Page", attachment_type=AttachmentType.PNG)
            print("🖱️ Scrolled to bottom of Active Device page")

            print("✅ Test completed successfully.")
            assert True

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test failed: {str(e)}"

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
