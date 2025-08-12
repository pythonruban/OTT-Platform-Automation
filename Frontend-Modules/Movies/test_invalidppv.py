import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Config reader

# 🔍 All element XPaths centralized
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "video_category_link": "//li[@id='header-Categories']",
    "genre_action": "//img[@alt='categories']",
    "episode_1": "//img[@alt='Episode 1']",

    # Subscription
    "subscribe_now": "//a[@id='subscriber-now-button']",
    "plan_select": "//button[@class='p-2 start_payment_css btn theme-button-bg-color accessButton bgButton w-50']",

    # Stripe Elements
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']",
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Live Video - Subscription")
@allure.title("Subscribe to Video with Invalid Stripe Card")
class TestLiveVideoSubscription:

    def test_subscribe_and_watch_video(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click_with_scroll(by, locator, label):
            try:
                with allure.step(f"Click: {label}"):
                    elem = wait.until(EC.element_to_be_clickable((by, locator)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", elem)
                    time.sleep(1)
                    elem.click()
                    print(f"✅ Clicked: {label}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                    time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {e}")

        try:
            # Step 1: Load Homepage
            with allure.step("Open Homepage"):
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["login_icon"])))
                print("🌐 Homepage loaded")

            # Step 2: Login (using ReadConfig)
            click_with_scroll(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            click_with_scroll(By.XPATH, xpaths["login_btn"], "Login Button")
            click_with_scroll(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Navigate to Video Categories → Action → Episode 1
            click_with_scroll(By.XPATH, xpaths["video_category_link"], "Video Categories")
            click_with_scroll(By.XPATH, xpaths["genre_action"], "Action Genre")
            click_with_scroll(By.XPATH, xpaths["episode_1"], "Episode 1")

            # Step 4: Click Subscribe and choose a plan
            click_with_scroll(By.XPATH, xpaths["subscribe_now"], "Subscribe Now")
            click_with_scroll(By.XPATH, xpaths["plan_select"], "Select Plan")

            # Step 5: Stripe payment (with invalid card)
            with allure.step("Fill Stripe Payment with Invalid Card"):
                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
                self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("1234 5678 9012 3456")
                self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
                self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
                self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Ruban Fail")
                click_with_scroll(By.XPATH, xpaths["submit_btn"], "Stripe Submit Button")
                print("💳 Submitted invalid Stripe form")

            # Optional: wait for error popup
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="Stripe_Submission_Result", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"Test Failed: {e}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception:
            print("⚠️ Browser already closed.")
