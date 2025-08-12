import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Only base_url used

# ✅ Load base URL from config
base_url = ReadConfig.getHomePageURL()

xpaths = {
    "signin_button": "//button[@id='home-signin']",
    "email": "//input[@id='signin-email']",
    "password": "//input[@id='signin-password']",
    "login_submit": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "home_check": "(//li[@class='homeNavList p-3'])[2]",
    "movies_menu": "(//li[@id='header-Movies'])",
    "movies_content": "//div[contains(@class, 'movieCard') or contains(@class, 'grid')]"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Login and Movies Page Flow")
class TestLoginAndMoviesFlow:

    def test_login_and_movies(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)

        def scroll_page(direction="down", label=""):
            offset = window_height // 2
            for _ in range(10):
                scroll_value = offset if direction == "down" else -offset
                self.driver.execute_script(f"window.scrollBy(0, {scroll_value});")
                time.sleep(0.4)
            print(f"📜 Scrolled {direction} on {label} page.")

        try:
            window_height = self.driver.execute_script("return window.innerHeight")
            self.driver.get(base_url)  # ✅ base_url from config
            self.driver.maximize_window()

            # Step 1: Sign In
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["signin_button"]))).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys("ruban.k@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
            self.driver.find_element(By.XPATH, xpaths["login_submit"]).click()
            print("✅ Logged in")

            # Step 2: Choose Profile
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
                print("✅ Profile selected")
            except Exception:
                print("⚠️ Profile selection skipped (maybe auto-logged in)")

            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)

            # Step 3: Wait for Home to load
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["home_check"])))
            print("🏠 Home page loaded")

            scroll_page("down", "Home")
            scroll_page("up", "Home")

            # Step 4: Navigate to Movies
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["movies_menu"]))).click()
            print("🎬 Navigated to Movies section")

            # Step 5: Wait and scroll Movies page
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["movies_content"])))
            scroll_page("down", "Movies")
            scroll_page("up", "Movies")

            allure.attach(self.driver.get_screenshot_as_png(), name="Movies_Success", attachment_type=AttachmentType.PNG)
            print("✅ Movies flow completed")

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Error_Screenshot", attachment_type=AttachmentType.PNG)
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

        finally:
            self.driver.quit()

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
