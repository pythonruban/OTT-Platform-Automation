import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.readProp import ReadConfig  # ✅ Your config reader for base URL

@pytest.mark.usefixtures("browser_setup")
class TestRedirectFromHomeToMusic:

    def test_home_wait_scroll_redirect_to_music(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 20)
        base_url = ReadConfig.getHomePageURL()

        # Step 1: Go to Home Page
        self.driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Home page loaded")

        # Step 2: Wait 3 seconds
        time.sleep(3)
        print("⏳ Waited 3 seconds on Home Page")

        # Step 3: Scroll down slowly
        for _ in range(5):
            self.driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(0.5)
        print("📜 Scrolled down the homepage")

        # Step 4: Redirect to Music → Latest Audios
        music_url = "https://node-trial.webnexs.org/music/latest_audios"
        self.driver.get(music_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"🎵 Redirected to: {music_url}")

        # Step 5: Wait 2 seconds on Music page
        time.sleep(2)
        print("⏳ Waited 2 seconds on music page")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
