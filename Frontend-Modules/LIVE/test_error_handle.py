import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestErrorHandling:

    def test_error_handling(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        
        try:
            # Open the homepage
            with allure.step("Open Homepage"):
                self.driver.get(ReadConfig.getHomePageURL())
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)
            
            # Try to find a non-existing element to simulate an error
            with allure.step("Locate non-existing element"):
                try:
                    wait.until(EC.presence_of_element_located((By.ID, "non_existing_id")))
                except TimeoutException as e:
                    allure.attach(self.driver.get_screenshot_as_png(), name="Timeout_Error", attachment_type=AttachmentType.PNG)
                    allure.attach(str(e), name="Error Message", attachment_type=AttachmentType.TEXT)
                    pytest.fail("Element with ID 'non_existing_id' not found.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="General_Error", attachment_type=AttachmentType.PNG)
            allure.attach(str(e), name="Error Message", attachment_type=AttachmentType.TEXT)
            pytest.fail(f"Test failed due to unexpected error: {str(e)}")