import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "language_dropdown": "//button[contains(@class,'multiLanguage')]",
    "language_links": {
        "Tamil": "/languages/tamil",
        "Spanish": "/languages/spanish",
        "German": "/languages/German",
        "French": "/languages/french",
        "Arabic": "/languages/Arabic",
        "English": "/languages/english"
    }
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest - Language Dropdown Navigation")
@allure.title("Guest user clicks each language in dropdown and navigates back")
class TestGuestLanguageClickAndBack:

    def test_guest_language_link_clicks(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)

        def click(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
                    elem.click()
                    print(f"✅ Clicked: {label}")
                    time.sleep(1)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {e}")

        base_url = ReadConfig.getHomePageURL()

        try:
            with allure.step("Load Home Page"):
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print("🏠 Home page loaded")

            for lang_name, lang_href in xpaths["language_links"].items():
                print(f"\n🔁 Processing Language: {lang_name}")
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Re-open dropdown each time from home
                click(By.XPATH, xpaths["language_dropdown"], "Open Language Dropdown")

                full_xpath = f"//a[@href='{lang_href}']"
                click(By.XPATH, full_xpath, f"Language → {lang_name}")

                with allure.step(f"✅ Inside Language Page: {lang_name}"):
                    print(f"🌐 Navigated to: {lang_name}")
                    time.sleep(2)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{lang_name}_Page", attachment_type=AttachmentType.PNG)

                # Go back to homepage
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["language_dropdown"])))
                print(f"🔙 Returned from: {lang_name}")
                time.sleep(1)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test Failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver not properly closed.")
