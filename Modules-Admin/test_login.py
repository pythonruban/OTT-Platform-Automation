import time
import pytest
import os
import sys
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# Add the project root to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.usefixtures("browser_setup")
class TestLoginPage:

    driver: webdriver.Firefox

    # Locators
    email_field = "(//input[@type='email'])[2]"
    password_field = "(//input[@name='password'])[1]"
    login_button = "(//button[@type='submit'])[2]"
    dashboard_element = "//span[normalize-space(text())='Dashboard']"
    # error_message no longer used

    def login(self, email, password):
        """Navigate to login page, enter credentials, click login, and attach screenshot."""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        # Enter email
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.email_field))
        )
        email_input = self.driver.find_element(By.XPATH, self.email_field)
        email_input.clear()
        email_input.send_keys(email)

        # Enter password
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.password_field))
        )
        password_input = self.driver.find_element(By.XPATH, self.password_field)
        password_input.clear()
        password_input.send_keys(password)

        # Click login
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.login_button))
        ).click()
        time.sleep(3)

        # Attach screenshot immediately after click
        allure.attach(
            self.driver.get_full_page_screenshot_as_png(),
            name=f"Clicked login with email='{email}' password='{password}'",
            attachment_type=AttachmentType.PNG
        )
        # small wait for page response
        time.sleep(3)

    @pytest.mark.order(1)
    def test_invalid_password_valid_email(self):
        """ Invalid password with valid email: dashboard should NOT appear."""
        try:
            self.login(ReadConfig.getAdminId(), "wrongpassword")

            # Wait briefly for dashboard; expect TimeoutException
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.dashboard_element))
                )
                time.sleep(3)
                # If dashboard appears, invalid login unexpectedly succeeded
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_password_unexpected_dashboard",
                    attachment_type=AttachmentType.PNG
                )
                pytest.fail("Invalid password test failed: dashboard appeared despite wrong password")
            except TimeoutException:
                # Expected path: dashboard did not appear
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_password_correctly_blocked",
                    attachment_type=AttachmentType.PNG
                )
                time.sleep(2)
                print(" Invalid password correctly prevented login.")
        except Exception as e:
            # Any unexpected exception
            print(f" Exception during invalid-password test: {e}")
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="invalid_password_exception",
                attachment_type=AttachmentType.PNG
            )
            pytest.fail(f"Invalid password test encountered exception: {e}")

    @pytest.mark.order(2)
    def test_invalid_email_valid_password(self):
        """ Invalid email with valid password: dashboard should NOT appear."""
        try:
            self.login("wronguser@example.com", ReadConfig.getPassword())

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.dashboard_element))
                )
                time.sleep(3)
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_email_unexpected_dashboard",
                    attachment_type=AttachmentType.PNG
                )
                time.sleep(2)
                pytest.fail("Invalid email test failed: dashboard appeared despite wrong email")
            except TimeoutException:
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_email_correctly_blocked",
                    attachment_type=AttachmentType.PNG
                )
                print(" Invalid email correctly prevented login.")
        except Exception as e:
            print(f" Exception during invalid-email test: {e}")
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="invalid_email_exception",
                attachment_type=AttachmentType.PNG
            )
            pytest.fail(f"Invalid email test encountered exception: {e}")

    @pytest.mark.order(3)
    def test_invalid_credentials(self):
        """ Invalid email and invalid password: dashboard should NOT appear."""
        try:
            self.login("invalid@example.com", "wrongpass")

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.dashboard_element))
                )
                time.sleep(3)
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_credentials_unexpected_dashboard",
                    attachment_type=AttachmentType.PNG
                )
                time.sleep(2)
                pytest.fail("Invalid credentials test failed: dashboard appeared despite wrong creds")
            except TimeoutException:
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="invalid_credentials_correctly_blocked",
                    attachment_type=AttachmentType.PNG
                )
                print(" Invalid credentials correctly prevented login.")
        except Exception as e:
            print(f" Exception during invalid-credentials test: {e}")
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="invalid_credentials_exception",
                attachment_type=AttachmentType.PNG
            )
            pytest.fail(f"Invalid credentials test encountered exception: {e}")

    @pytest.mark.order(4)
    def test_empty_credentials(self):
        """ Empty email and password: dashboard should NOT appear."""
        try:
            self.login("", "")

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.dashboard_element))
                )
                time.sleep(3)
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="empty_credentials_unexpected_dashboard",
                    attachment_type=AttachmentType.PNG
                )
                time.sleep(3)
                pytest.fail("Empty credentials test failed: dashboard appeared despite empty fields")
            except TimeoutException:
                allure.attach(
                    self.driver.get_full_page_screenshot_as_png(),
                    name="empty_credentials_correctly_blocked",
                    attachment_type=AttachmentType.PNG
                )
                print(" Empty credentials correctly prevented login.")
        except Exception as e:
            print(f" Exception during empty-credentials test: {e}")
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="empty_credentials_exception",
                attachment_type=AttachmentType.PNG
            )
            pytest.fail(f"Empty credentials test encountered exception: {e}")

    @pytest.mark.order(5)
    def test_valid_login(self):
        """ Valid login with correct credentials: dashboard should appear."""
        try:
            self.login(ReadConfig.getAdminId(), ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.dashboard_element))
            )
            time.sleep(3)
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="valid_login_dashboard",
                attachment_type=AttachmentType.PNG
            )
            time.sleep(3)
            print(" Valid login successful, dashboard appeared.")
        except Exception as e:
            print(f" Valid login test failed: {e}")
            allure.attach(
                self.driver.get_full_page_screenshot_as_png(),
                name="valid_login_failure",
                attachment_type=AttachmentType.PNG
            )
            pytest.fail(f"Valid login test failed: {e}")

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 