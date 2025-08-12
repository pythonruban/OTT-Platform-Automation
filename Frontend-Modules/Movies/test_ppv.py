import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Import from readProp

# ✅ Load base URL from config
base_url = ReadConfig.getHomePageURL()

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "movies_tab": "//li[@id='header-Movies']",
    "genre_action": "//img[@alt='categories']",
    "video_tile": "//img[@alt='Maaman.mp4']",
    "ppv_rent_now": "//button[@id='rent-now-role-4-button']",
    "confirm_payment": "//button[@class='btn w-100 mb-2']",
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']",
    "watch_now_btn": "watch-now-button"
}


@pytest.mark.usefixtures("browser_setup")
class TestmoviesPPVWatchFlow:

    def test_ppv_payment_and_watch(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        def debug_click(by, locator, label):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_clicked", attachment_type=AttachmentType.PNG)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_fail", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {repr(e)}")

        try:
            # Step 1: Open site using dynamic base_url
            self.driver.get(base_url)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

            # Step 2: Login
            debug_click(By.XPATH, xpaths["login_icon"], "Login Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys("abi@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
            debug_click(By.XPATH, xpaths["login_btn"], "Login Button")
            debug_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 3: Navigate to Video
            debug_click(By.XPATH, xpaths["movies_tab"], "Movies Tab")
            view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
            wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()
            debug_click(By.XPATH, xpaths["genre_action"], "Action Genre")
            debug_click(By.XPATH, xpaths["video_tile"], "Video Maaman.mp4")

            # Step 4: Rent PPV
            debug_click(By.XPATH, xpaths["ppv_rent_now"], "Rent Now Button")
            debug_click(By.XPATH, xpaths["confirm_payment"], "Confirm Payment")

            # Step 5: Stripe Payment (Invalid)
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("test@fail.com")
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("1234 5678 9012 3456")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
            self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Invalid Test")
            debug_click(By.XPATH, xpaths["submit_btn"], "Submit Invalid Stripe")

            # Step 6: Retry with Valid Payment
            time.sleep(2)
            for key in ["card_number", "card_expiry", "card_cvc"]:
                self.driver.find_element(By.XPATH, xpaths[key]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("4242 4242 4242 4242")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/55")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("122")
            billing = self.driver.find_element(By.XPATH, xpaths["billing_name"])
            billing.clear()
            billing.send_keys("Ruban Stripe")
            debug_click(By.XPATH, xpaths["submit_btn"], "Submit Valid Stripe")

            print("✅ Waiting for Stripe success redirect...")
            time.sleep(7)

            # Step 7: Go again to video after purchase
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            debug_click(By.XPATH, xpaths["movies_tab"], "Movies Tab (Post Payment)")
            debug_click(By.XPATH, xpaths["genre_action"], "Action Genre")
            debug_click(By.XPATH, xpaths["video_tile"], "Video Maaman.mp4 (Again)")

            # Step 8: Watch Now
            debug_click(By.ID, xpaths["watch_now_btn"], "Watch Now Button")

            # Step 9: Confirm playback
            print("▶️ Waiting 5 sec to confirm video is playing...")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="Video_Played_5s", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Final_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {repr(e)}")

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver was not initialized.")
