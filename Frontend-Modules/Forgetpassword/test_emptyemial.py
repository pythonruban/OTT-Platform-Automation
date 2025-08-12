import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.readProp import ReadConfig
from typing import Optional

class ForgotPasswordPage:
    """Page Object for Forgot Password functionality"""
    
    LOCATORS = {
        "login_icon": (By.XPATH, "(//button[contains(@id, 'signin')])[1]"),
        "forgot_link": (By.XPATH, "//a[@href='/verify/forget']"),
        "email_field": (By.XPATH, "//input[@type='email']"),
        "submit_btn": (By.XPATH, "//button[@type='submit']"),
        "toast": (By.XPATH, "//div[@role='alert']")
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def take_screenshot(self, name: str) -> None:
        """Capture and attach screenshot with Allure"""
        with allure.step(f"Taking screenshot: {name}"):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=AttachmentType.PNG
            )

    def navigate_to_forgot_password(self) -> None:
        """Navigate to forgot password page"""
        with allure.step("Navigating to forgot password page"):
            self.wait.until(EC.element_to_be_clickable(self.LOCATORS["login_icon"])).click()
            self.wait.until(EC.element_to_be_clickable(self.LOCATORS["forgot_link"])).click()
            self.wait.until(EC.presence_of_element_located(self.LOCATORS["email_field"]))

    def submit_empty_form(self) -> None:
        """Submit form without entering email"""
        with allure.step("Submitting empty form"):
            self.driver.find_element(*self.LOCATORS["submit_btn"]).click()

    def get_validation_message(self) -> Optional[str]:
        """Get validation message from either toast or field validation"""
        try:
            with allure.step("Checking for toast message"):
                toast = self.wait.until(EC.presence_of_element_located(self.LOCATORS["toast"]))
                return toast.text.strip()
        except TimeoutException:
            with allure.step("Checking for field validation message"):
                email_field = self.driver.find_element(*self.LOCATORS["email_field"])
                return email_field.get_attribute("validationMessage")
        return None

@pytest.mark.usefixtures("browser_setup")
@allure.epic("Authentication")
@allure.feature("Forgot Password")
@allure.story("Form Validation")
class TestForgotPasswordEmptyEmail:
    """Test cases for forgot password empty email validation"""
    
    def setup_method(self, method):
        """Setup method that runs before each test"""
        self.driver = None
        self.page = None

    @allure.title("Verify empty email field validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_email_submission(self, browser_setup):
        try:
            with allure.step("Initialize test"):
                self.driver = browser_setup
                self.page = ForgotPasswordPage(self.driver)
            
            with allure.step("Navigate to homepage"):
                self.driver.get(ReadConfig.getHomePageURL())
                self.page.take_screenshot("Home_Page_Loaded")

            with allure.step("Test empty email submission"):
                self.page.navigate_to_forgot_password()
                self.page.submit_empty_form()
                self.page.take_screenshot("Empty_Form_Submitted")

                validation_message = self.page.get_validation_message()
                assert validation_message, "No validation message displayed"
                
                with allure.step(f"Verify validation message: {validation_message}"):
                    assert any(keyword in validation_message.lower() for keyword in ["email", "required"]), \
                        f"Unexpected validation message: {validation_message}"

        except Exception as e:
            if hasattr(self, 'page') and self.page:
                self.page.take_screenshot("Test_Failure")
            pytest.fail(f"Test failed: {str(e)}")
        finally:
            self.teardown_method()

    def teardown_method(self):
        """Cleanup method that runs after each test"""
        with allure.step("Cleanup - Closing browser"):
            try:
                if hasattr(self, 'driver') and self.driver:
                    self.driver.quit()
            except Exception as e:
                allure.attach(str(e), "Browser cleanup error", attachment_type=allure.attachment_type.TEXT)
                print(f"Failed to close browser: {str(e)}")
            finally:
                self.driver = None
                self.page = None
