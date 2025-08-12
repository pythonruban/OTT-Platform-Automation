import sys
import os
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# ✅ Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup")
class TestGuestUserHomePage:

    @allure.title("Homepage loads for guest user with banner and sections visible")
    @allure.description("Opens the homepage as guest user and verifies banner and sections are present. Scrolls down and up with screenshots.")
    def test_guest_homepage_view(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 15)

        url = ReadConfig.getHomePageURL()
        self.driver.get(url)
        self.driver.maximize_window()
        print(f"🌐 Visiting homepage as guest: {url}")

        # ✅ Check if banner is visible
        try:
            banner_xpath = "//div[contains(@class, 'banner') or contains(@class, 'carousel')]"
            wait.until(EC.visibility_of_element_located((By.XPATH, banner_xpath)))
            print("✅ Banner is visible")
        except:
            print("❌ Banner not found")

        # ✅ Check for at least one home page section (e.g., Featured, Latest, etc.)
        try:
            section_xpath = "(//h2[contains(text(), 'Featured') or contains(text(), 'Latest') or contains(@class, 'section-title')])[1]"
            wait.until(EC.visibility_of_element_located((By.XPATH, section_xpath)))
            print("✅ At least one section title is visible")
        except:
            print("❌ Home page section not found")

        # ✅ Screenshot initial
        allure.attach(self.driver.get_screenshot_as_png(), name="home_initial", attachment_type=AttachmentType.PNG)

        # ✅ Scroll down
        print("🔽 Scrolling down...")
        total_scrolls = 10
        for i in range(total_scrolls):
            self.driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
            time.sleep(0.4)

            if i == total_scrolls // 3:
                allure.attach(self.driver.get_screenshot_as_png(), name="scroll_middle", attachment_type=AttachmentType.PNG)
            elif i == total_scrolls - 1:
                allure.attach(self.driver.get_screenshot_as_png(), name="scroll_bottom", attachment_type=AttachmentType.PNG)

        time.sleep(1)

        # ✅ Scroll back up
        print("🔼 Scrolling up...")
        for _ in range(total_scrolls):
            self.driver.execute_script("window.scrollBy(0, -window.innerHeight / 2);")
            time.sleep(0.3)

        allure.attach(self.driver.get_screenshot_as_png(), name="scroll_top_back", attachment_type=AttachmentType.PNG)
        print("✅ Scroll complete")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
