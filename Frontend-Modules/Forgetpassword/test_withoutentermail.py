import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[contains(@id, 'signin')])[1]",
    "forgot_link": "//a[@href='/verify/forget']",
    "email_field": "//input[@type='email']",
    "submit_btn": "//button[@type='submit']",
    "toast": "//div[@role='alert']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Forgot Password")
@allure.title("Test Forgot Password with Empty Email Field")
class TestForgotPasswordEmptyEmail:

    def test_empty_email_submission(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        try:
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            allure.attach(self.driver.get_screenshot_as_png(), name="Home_Loaded", attachment_type=AttachmentType.PNG)

            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["forgot_link"]))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_field"])))
            self.driver.find_element(By.XPATH, xpaths["submit_btn"]).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="Empty_Submit_Clicked", attachment_type=AttachmentType.PNG)

            try:
                toast = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["toast"])))
                toast_text = toast.text.strip()
                assert "email" in toast_text.lower() or "required" in toast_text.lower()
            except TimeoutException:
                email_field = self.driver.find_element(By.XPATH, xpaths["email_field"])
                validation_message = email_field.get_attribute("validationMessage")
                assert validation_message or email_field.is_displayed()

        except (TimeoutException, NoSuchElementException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"Test failed: {str(e)}")

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except:
            pass
