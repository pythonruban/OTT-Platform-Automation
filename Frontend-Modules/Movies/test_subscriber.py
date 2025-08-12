import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Correct import

# 🔍 Centralized XPath Dictionary
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "video_category_link": "//li[@id='header-Categories']",
    "genre_action": "//img[@alt='categories']",
    "episode_1": "//img[@alt='Episode 1']",
    "live_Video": "//img[@alt='RIRHHTW']",

    # Subscription
    "subscribe_now": "//a[@id='subscriber-now-button']",
    "plan_select": "//button[@class='p-2 start_payment_css btn theme-button-bg-color accessButton bgButton w-50']",

    # Stripe Fields
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']",

    # Player
    "watch_now": "watch-now-button",
    "play_button": "//button[@class='ytp-large-play-button ytp-button']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Live Video Subscription & Playback")
class TestLiveVideoSubscription:

    def test_subscribe_and_watch_video(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click_with_scroll(by, locator, label):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"fail_{label}", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Load Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["login_icon"])))
            print("🌐 Homepage loaded")

            # Step 2: Login
            click_with_scroll(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            click_with_scroll(By.XPATH, xpaths["login_btn"], "Login Button")
            click_with_scroll(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Navigate to Video Category
            click_with_scroll(By.XPATH, xpaths["video_category_link"], "Video Categories")
            click_with_scroll(By.XPATH, xpaths["genre_action"], "Action Genre")
            click_with_scroll(By.XPATH, xpaths["episode_1"], "Episode 1")

            # Step 4: Subscription Flow
            click_with_scroll(By.XPATH, xpaths["subscribe_now"], "Subscribe Now")
            click_with_scroll(By.XPATH, xpaths["plan_select"], "Select Plan")

            # Step 5: Stripe Payment - Invalid
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("1234 5678 9012 3456")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
            self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Ruban Fail")
            click_with_scroll(By.XPATH, xpaths["submit_btn"], "Stripe Invalid Submit")

            # Step 6: Stripe Payment - Valid Retry
            for key in ["card_number", "card_expiry", "card_cvc"]:
                self.driver.find_element(By.XPATH, xpaths[key]).clear()
            time.sleep(1)
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("4242 4242 4242 4242")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/55")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("122")
            billing = self.driver.find_element(By.XPATH, xpaths["billing_name"])
            billing.clear()
            billing.send_keys("Ruban Success")
            click_with_scroll(By.XPATH, xpaths["submit_btn"], "Stripe Valid Submit")

            # Step 7: Redirect after success
            print("⏳ Waiting for homepage redirect after payment...")
            WebDriverWait(self.driver, 20).until(EC.url_to_be(base_url))
            print("✅ Redirected to homepage")

            # Step 8: Reopen video
            click_with_scroll(By.XPATH, xpaths["video_category_link"], "Video Categories Again")
            click_with_scroll(By.XPATH, xpaths["genre_action"], "Action Genre Again")
            click_with_scroll(By.XPATH, xpaths["live_Video"], "RIRHHTW")
            click_with_scroll(By.ID, xpaths["watch_now"], "Watch Now")

            # Step 9: Play YouTube video
            time.sleep(3)
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            print("✅ Switched to iframe")

            play_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["play_button"])))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", play_btn)
            time.sleep(1)
            play_btn.click()
            print("▶️ Video is playing")
            time.sleep(5)
            self.driver.switch_to.default_content()

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Browser already closed.")
