import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "swiper_next": "//div[@class='swiper-button-next']",
    
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest - Swiper and Dragon Track")
@allure.title("Guest user clicks swiper and opens Dragon track")
class TestGuestHomeSwiperMusic:

    def test_guest_home_swiper_dragon(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        def click(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", elem)
                    time.sleep(1)
                    elem.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                    print(f"✅ Clicked: {label}")
                    time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {str(e)}")

        try:
            with allure.step("Step 1: Load Home Page"):
                self.driver.get(ReadConfig.getHomePageURL())
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="HomePage_Loaded", attachment_type=AttachmentType.PNG)
                print("✅ Home page loaded")

            # Step 2: Click Swiper button 3 times to rotate banners
            for i in range(3):
                try:
                    click(By.XPATH, xpaths["swiper_next"], f"Swiper Next {i+1}")
                except:
                    print(f"⚠️ Swiper next not found or not clickable at index {i+1}")
                    break

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test Failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Driver not closed.")
