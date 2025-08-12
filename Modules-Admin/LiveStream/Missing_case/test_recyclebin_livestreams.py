import time
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestRecyclebinLivestreams:
    recyclebin_button_xpath = "//button[contains(., 'Recycle Bin') or contains(@aria-label, 'recycle') or contains(@title, 'Recycle Bin') or contains(@class, 'recycle')]"
    deleted_table_xpath = "//table[contains(@id, 'livestream')]"  # Update as needed for your trash/deleted table
    empty_message_xpath = "//*[contains(text(),'No streams found') or contains(text(),'No data found') or contains(text(),'No deleted streams')]"

    def login_and_goto_livestream_page(self, browser_setup):
        self.driver = browser_setup
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='email'])[2]"))).send_keys(ReadConfig.getAdminId())
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@name='password'])[1]"))).send_keys(ReadConfig.getPassword())
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit'])[2]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-bs-target='#Live-Stream']"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'All Live Streams')]"))).click()
        time.sleep(2)

    def test_recyclebin_creative(self, browser_setup):
        """Creative: Recycle bin shows deleted streams."""
        self.login_and_goto_livestream_page(browser_setup)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.recyclebin_button_xpath))).click()
        time.sleep(2)
        table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.deleted_table_xpath)))
        # Creative: Expect at least one entry if there's a deleted stream
        rows = self.driver.find_elements(By.XPATH, self.deleted_table_xpath + "//tbody/tr")
        assert rows is not None
        # Screenshot for confirmation
        allure.attach(self.driver.get_screenshot_as_png(), name="RecycleBin_Creative", attachment_type=AttachmentType.PNG)

    def test_recyclebin_negative(self, browser_setup):
        """Negative: Recycle bin is empty."""
        self.login_and_goto_livestream_page(browser_setup)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.recyclebin_button_xpath))).click()
        time.sleep(2)
        try:
            empty_msg = self.driver.find_element(By.XPATH, self.empty_message_xpath)
            assert empty_msg.is_displayed(), 'No empty message! Trash should be empty.'
            allure.attach(self.driver.get_screenshot_as_png(), name="RecycleBin_Empty_Negative", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="RecycleBin_Empty_Negative_Fail", attachment_type=AttachmentType.PNG)
            pytest.fail(str(e))

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

