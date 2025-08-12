import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.readProp import ReadConfig
import allure
from allure_commons.types import AttachmentType

@allure.feature("Guest - Music Track Redirect")
@allure.title("Guest clicks on /music and redirected to /music/track manually")
@pytest.mark.usefixtures("browser_setup")
class TestGuestMusicRedirect:

    def test_guest_music_track_redirect(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            with allure.step("Step 1: Open Home Page"):
                self.driver.get(ReadConfig.getHomePageURL())
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Click /music link"):
                music_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/music"]')))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", music_link)
                music_link.click()
                time.sleep(3)

                current_url = self.driver.current_url
                print(f"🔍 After click, current URL: {current_url}")
                assert current_url.endswith("/music"), f"❌ Test Failed: Expected to land on /music but got {current_url}"

            with allure.step("Step 3: Manually redirect to /music/track"):
                self.driver.get(ReadConfig.getHomePageURL() + "/music/track")
                time.sleep(3)
                final_url = self.driver.current_url
                expected_url = ReadConfig.getHomePageURL() + "/music/track"
                assert final_url == expected_url, f"❌ Test Failed: Expected: {expected_url}, but got: {final_url}"
                allure.attach(self.driver.get_screenshot_as_png(), name="Track_Redirected", attachment_type=AttachmentType.PNG)
                print("✅ Reached /music/track successfully.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test Failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Driver not initialized.")
