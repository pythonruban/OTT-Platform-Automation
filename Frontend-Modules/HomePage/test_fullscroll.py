import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup")
class TestLoginAndHomeScrollOnly:

    def test_login_and_scroll_home(self, browser_setup):
        self.driver = browser_setup
        self.wait = WebDriverWait(self.driver, 20)

        homepage_url = ReadConfig.getHomePageURL()
        self.driver.get(homepage_url)
        self.driver.maximize_window()
        print(f"🌐 Website opened: {homepage_url}")

        xpaths = {
            "signin_button": "//button[@id='home-signin']",
            "email": "//input[@id='signin-email']",
            "password": "//input[@id='signin-password']",
            "login_submit": "//button[@id='signin-submit']",
            "choose_profile": "(//img[@alt='Avatar'])[1]",
            "home_check": "(//li[@class='homeNavList p-3'])[2]"
        }

        try:
            # Step 2: Login
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signin_button"]))).click()
            
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
            self.driver.find_element(By.XPATH, xpaths["login_submit"]).click()
            print("✅ Logged in")

            # Step 3: Choose Profile
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
                print("✅ Profile selected")
            except:
                print("⚠️ Profile selection skipped")

            # Step 4: Wait for Home Page
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths["home_check"])))
            print("🏠 Home page loaded")
            allure.attach(self.driver.get_screenshot_as_png(), name="home_initial", attachment_type=AttachmentType.PNG)

            # Step 5: Scroll Down
            print("🔽 Scrolling down Home page")
            total_scrolls = 10
            for i in range(total_scrolls):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
                time.sleep(0.4)
                if i == 0:
                    allure.attach(self.driver.get_screenshot_as_png(), name="scroll_first", attachment_type=AttachmentType.PNG)
                elif i == total_scrolls // 2:
                    allure.attach(self.driver.get_screenshot_as_png(), name="scroll_middle", attachment_type=AttachmentType.PNG)
                elif i == total_scrolls - 1:
                    allure.attach(self.driver.get_screenshot_as_png(), name="scroll_last", attachment_type=AttachmentType.PNG)

            time.sleep(1)

            # Step 6: Scroll Up
            print("🔼 Scrolling up Home page")
            for _ in range(total_scrolls):
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight / 2);")
                time.sleep(0.4)

            allure.attach(self.driver.get_screenshot_as_png(), name="home_scroll_back", attachment_type=AttachmentType.PNG)
            print("✅ Scrolling complete")

        except Exception as e:
            print("❌ Error:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="error_screenshot", attachment_type=AttachmentType.PNG)
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
