import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup")
class TestRedirectShowToSeries:

    def test_click_show_header_and_series_test(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        # Step 1: Open Home Page
        self.driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Home page loaded")

        # Step 2: Click on 'SHOW' header
        show_tab_xpath = '//a[@href="/show"]'
        show_tab = wait.until(EC.element_to_be_clickable((By.XPATH, show_tab_xpath)))
        show_tab.click()
        print("🎬 Clicked on 'SHOW' tab")

        # Step 3: Wait and scroll Show page
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(2)

        # Step 4: Locate & click 'series test'
        try:
            series_xpath = '//img[contains(@alt, "series test")]'
            series_element = wait.until(EC.presence_of_element_located((By.XPATH, series_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: \'center\'});", series_element)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, series_xpath))).click()
            print("🎥 Clicked on series with alt='series test'")

            # Step 5: Wait for page load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)
            print("✅ Navigated to series detail page")

        except Exception as e:
            raise AssertionError(f"❌ Failed to click series test: {e}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
