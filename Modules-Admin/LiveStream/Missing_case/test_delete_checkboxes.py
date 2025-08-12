import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestDeleteWithCheckboxes:
    checkboxes_xpath = "//input[@class='table-checkbox']"
    delete_button_xpath = "//button[contains(., 'Delete') or contains(@aria-label, 'delete') or contains(@title, 'Delete') or contains(@class, 'delete')]"
    confirm_delete_button_xpath = "(//button[contains(., 'Delete') or contains(@aria-label, 'Delete') or contains(@title, 'Delete') or contains(@class, 'Delete')])[1]"
    list_table_xpath = "//table[contains(@id, 'livestream')]"

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

    def test_delete_random_checkboxes(self, browser_setup):
        """Select and delete three random checkboxes"""
        import random

        self.login_and_navigate(browser_setup)

        # Select random three checkboxes
        checkboxes = self.driver.find_elements(By.XPATH, self.checkboxes_xpath)
        random_checkboxes = random.sample(checkboxes, min(3, len(checkboxes)))
        for checkbox in random_checkboxes:
            if not checkbox.is_selected():
                checkbox.click()

        # Click delete button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.delete_button_xpath))).click()

        # Confirm deletion
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.confirm_delete_button_xpath))).click()

        # Verify that three items have been deleted
        time.sleep(2)
        remaining_checkboxes = len(self.driver.find_elements(By.XPATH, self.checkboxes_xpath))
        assert remaining_checkboxes == len(checkboxes) - len(random_checkboxes), "Not all selected items were deleted!"
        allure.attach(self.driver.get_screenshot_as_png(), name="Delete_Random_Checkboxes", attachment_type=AttachmentType.PNG)

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

