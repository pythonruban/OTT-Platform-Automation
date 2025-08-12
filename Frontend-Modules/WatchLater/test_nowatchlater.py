import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ For dynamic URL

xpaths = {
    # Login
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    # Profile > Watch Later flow
    "profile_avatar": "//img[@alt='RK']",
    "watchlater_tab": "//a[@id='watchlater']",
    "view_all": "//a[@href='/watchlater/videos']"
}
watchlater_btn_id = "video-watchlater-button"

@pytest.mark.usefixtures("browser_setup")
@allure.title("Watch Later via Direct Video Page")
@allure.description("Login, visit video directly, click 'Watch Later', then verify via profile.")
class TestWatchLaterShortcutFlow:

    def test_watchlater_from_direct_video(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, locator, label, scroll=True):
            try:
                elem = wait.until(EC.presence_of_element_located((by, locator)))
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                    time.sleep(1)
                wait.until(EC.element_to_be_clickable((by, locator))).click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Load Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("🌐 Homepage loaded")
            allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Login
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            allure.attach(self.driver.get_screenshot_as_png(), name="Credentials_Entered", attachment_type=AttachmentType.PNG)

            click(self.driver, wait, By.XPATH, xpaths["login_btn"], "Login Button")
            click(self.driver, wait, By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Choose Profile
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            
            # Step 5: Click "Watch Later"
            click(By.ID, watchlater_btn_id, "Watch Later Button")

            # Step 6: Go to profile > Watch Later section
            click(By.XPATH, xpaths["profile_avatar"], "Profile Avatar (RK)")
            click(By.XPATH, xpaths["watchlater_tab"], "Watch Later Tab")
            click(By.XPATH, xpaths["view_all"], "View All Watch Later")

            print("✅ Watch Later flow completed successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="WatchLater_Finished", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test failed: {str(e)}"

        def teardown_class(self):
            try:
                self.driver.quit()
            except AttributeError:
                print("⚠️ Driver was not initialized.")
