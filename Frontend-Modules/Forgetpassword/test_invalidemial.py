import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Use centralized config

xpaths = {
    "login_icon": "(//button[contains(@id, 'signin')])[1]",
    "forgot_link": "//a[@href='/verify/forget']",
    "email_field": "//input[@type='email']",
    "submit_btn": "//button[@type='submit']",
    "toast": "//div[@role='alert']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Forgot Password")
@allure.title("Forgot Password with Invalid Email (Expecting Error Toast)")
class TestForgotPasswordInvalidEmail:

    def test_invalid_forgot_password_email(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            # Step 1: Load Homepage
            self.driver.get(base_url)
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
            allure.attach(self.driver.get_screenshot_as_png(), name="Home_Page_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Click Login icon
            login_btn = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["login_icon"])))
            login_btn.click()
            print("✅ Clicked Login Icon")

            # Step 3: Click Forgot Password link
            forgot_link = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["forgot_link"])))
            forgot_link.click()
            print("✅ Clicked Forgot Password Link")

            # Step 4: Enter invalid email
            email_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email_field"])))
            email_input.clear()
            email_input.send_keys("invaliduser@wrong.com")
            print("✅ Entered invalid email")

            # Step 5: Click Submit
            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
            submit_btn.click()
            print("✅ Clicked Submit")

            # Step 6: Wait for error toast
            toast = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["toast"])))
            toast_text = toast.text.strip()
            allure.attach(self.driver.get_screenshot_as_png(), name="Toast_Displayed", attachment_type=AttachmentType.PNG)
            print(f"⚠️ Toast Message: {toast_text}")

            # Step 7: Assert toast text is as expected
            assert "invalid" in toast_text.lower() or "not found" in toast_text.lower(), \
                f"Unexpected toast message: {toast_text}"

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except Exception as e:
            print("⚠️ Driver quit failed:", str(e))
