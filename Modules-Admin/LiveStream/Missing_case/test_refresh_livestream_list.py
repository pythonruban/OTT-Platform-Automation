import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestRefreshLivestreamList:
    refresh_button_xpath = "//button[contains(., 'Refresh') or contains(@aria-label, 'refresh') or contains(@title, 'Refresh') or contains(@class, 'refresh')]"
    list_table_xpath = "//table[contains(@id, 'livestream')]"  # Update as needed
    empty_message_xpath = "//*[contains(text(),'No streams found') or contains(text(),'No data found')]"

    def login_and_navigate(self, browser_setup):
        self.driver = browser_setup
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='email'])[2]"))).send_keys(ReadConfig.getAdminId())
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@name='password'])[1]"))).send_keys(ReadConfig.getPassword())
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit'])[2]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-bs-target='#Live-Stream']"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'All Live Streams')]"))).click()
        time.sleep(2)

    def test_refresh_button_creative(self, browser_setup):
        """Creative: Expecting new data after refresh if backend changes"""
        self.login_and_navigate(browser_setup)
        old_rows = self.driver.find_elements(By.XPATH, self.list_table_xpath + "//tbody/tr")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.refresh_button_xpath))).click()
        time.sleep(2)
        new_rows = self.driver.find_elements(By.XPATH, self.list_table_xpath + "//tbody/tr")
        # Creative: We allow the count to change if new data is added after refresh
        assert len(new_rows) >= len(old_rows)
        allure.attach(self.driver.get_screenshot_as_png(), name="Refresh_Creative", attachment_type=AttachmentType.PNG)

    def test_refresh_button_negative(self, browser_setup):
        """Negative: Empty list after deletion, refresh keeps it empty"""
        self.login_and_navigate(browser_setup)
        try:
            # Simulate: Ensure all live streams are deleted before this (assume setup, or do deletion here if access)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.refresh_button_xpath))).click()
            time.sleep(1)
            # Assert empty message
            assert self.driver.find_element(By.XPATH, self.empty_message_xpath).is_displayed(), 'List is not empty!'
            allure.attach(self.driver.get_screenshot_as_png(), name="Refresh_Empty_Negative", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Refresh_Empty_Negative_Fail", attachment_type=AttachmentType.PNG)
            pytest.fail(str(e))

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

