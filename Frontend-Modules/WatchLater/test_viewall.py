import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Dynamic base URL

xpaths = {
    "login_icon": "//button[@id='home-signin']",
    "email": "//input[@id='signin-email']",
    "password": "//input[@id='signin-password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "profile_avatar": "//img[@alt='RK']",
    "watchlater_icon": "//a[@id='watchlater']",
    "view_all_shows": "//a[@href='/watchlater/shows' and contains(text(),'View All')]"
}

@pytest.mark.usefixtures("browser_setup")
@allure.title("Watch Later > View All Shows")
@allure.description("Login, go to Watch Later, and open all saved shows.")
class TestDirectWatchLaterAccess:

    def test_direct_watchlater_shows(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

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
            # Step 1: Load Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("🌐 Homepage loaded")
            allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Login
            click(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
            allure.attach(self.driver.get_screenshot_as_png(), name="Credentials_Entered", attachment_type=AttachmentType.PNG)
            click(By.XPATH, xpaths["login_btn"], "Login Button")

            # Step 3: Choose Profile
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 4: Open Watch Later
            click(By.XPATH, xpaths["profile_avatar"], "Profile Avatar")
            click(By.XPATH, xpaths["watchlater_icon"], "Watch Later Icon")

            # Step 5: Click "View All" for Shows
            click(By.XPATH, xpaths["view_all_shows"], "View All Shows in Watch Later")

            print("🎉 Test completed — Direct Watch Later 'Shows' accessed successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="WatchLaterShows_Completed", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            assert False, f"❌ Test failed: {str(e)}"

    def teardown_class(self):
        """Close the browser after test execution"""
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
