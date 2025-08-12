import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# 🔍 Centralized XPath dictionary
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "video_category_link": "//li[@id='header-Categories']",
    "genre_action": "//img[@alt='categories']",
    "episode_1": "//img[@alt='Episode 1']",
    "live_video": "//img[@alt='RIRHHTW']",
    "subscribe_now": "//a[@id='subscriber-now-button']",
    "plan_select": "//button[contains(@class, 'start_payment_css')]",
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']",
    "watch_now": "watch-now-button",
    "play_button": "//button[@class='ytp-large-play-button ytp-button']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Live Video Subscription & Playback")
@allure.title("Subscribe to PPV Video & Play After Stripe Payment")
class TestLiveVideoSubscription:

    def test_subscribe_and_play(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
                    time.sleep(1)
                    elem.click()
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                    print(f"✅ Clicked: {label}")
                    time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Failed", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {e}")

        def fill_stripe_card(card, expiry, cvc, name):
            self.driver.find_element(By.XPATH, xpaths["card_number"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys(card)
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys(expiry)
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys(cvc)
            billing = self.driver.find_element(By.XPATH, xpaths["billing_name"])
            billing.clear()
            billing.send_keys(name)

        try:
            # Step 1: Load Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Step 2: Login
            click(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            click(By.XPATH, xpaths["login_btn"], "Login Button")
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Navigate to Action Genre
            click(By.XPATH, xpaths["video_category_link"], "Video Categories")
            click(By.XPATH, xpaths["genre_action"], "Action Genre")
            click(By.XPATH, xpaths["episode_1"], "Episode 1")

            # Step 4: Subscribe to PPV
            click(By.XPATH, xpaths["subscribe_now"], "Subscribe Now")
            click(By.XPATH, xpaths["plan_select"], "Select Plan")

            # Step 5: Stripe - Invalid
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
            fill_stripe_card("1234 5678 9012 3456", "12/30", "111", "Fail Card")
            click(By.XPATH, xpaths["submit_btn"], "Stripe Invalid Submit")
            time.sleep(3)

            # Step 6: Stripe - Valid
            fill_stripe_card("4242 4242 4242 4242", "12/55", "122", "Ruban Success")
            click(By.XPATH, xpaths["submit_btn"], "Stripe Valid Submit")
            time.sleep(10)

            # Step 7: Post-payment - Back to Homepage
            WebDriverWait(self.driver, 20).until(EC.url_to_be(base_url))

            # Step 8: Replay the video
            click(By.XPATH, xpaths["video_category_link"], "Video Categories Reload")
            click(By.XPATH, xpaths["genre_action"], "Action Genre Reload")
            click(By.XPATH, xpaths["live_video"], "Live Video Reload")
            click(By.ID, xpaths["watch_now"], "Watch Now")

            # Step 9: Play inside iframe
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["play_button"]))).click()
            time.sleep(5)
            self.driver.switch_to.default_content()
            print("🎬 Video Played Successfully")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
