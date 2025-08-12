import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "login_email": "//input[@name='email']",
    "login_password": "//input[@name='password']",
    "login_submit": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    "live_tab": "//li[@id='header-Live']",
    "categories": "//div[@class='card-image-container']",
    "videos": "//div[@class='homeListImage active']",
    "ppv_button": "//button[contains(@id,'rent-now-role')]",
    "confirm_ppv": "//button[@class='btn w-100 mb-2']",

    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_payment": "//div[@class='SubmitButton-IconContainer']",
}

@pytest.mark.usefixtures("browser_setup")
class TestGuestLoginPPVStripe:

    @allure.step("Click on: {label}")
    def wait_and_click(self, by, locator, label):
        wait = WebDriverWait(self.driver, 30)
        try:
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            wait.until(EC.element_to_be_clickable((by, locator))).click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Click Failed - {label}", attachment_type=AttachmentType.PNG)
            raise Exception(f"❌ Failed to click {label}: {e}")

    @allure.step("Login with credentials and select profile")
    def login_and_profile(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["login_email"]))).send_keys(ReadConfig.getTestingemail())
        self.driver.find_element(By.XPATH, xpaths["login_password"]).send_keys(ReadConfig.getTestpassword())
        self.wait_and_click(By.XPATH, xpaths["login_submit"], "Login Submit")
        self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

    @allure.step("Navigate to LIVE tab")
    def go_home_to_live(self):
        self.driver.get(ReadConfig.getHomePageURL())
        self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab")

    @allure.step("Enter Stripe Card: {label}")
    def enter_stripe_card(self, card_num, exp, cvc, name, label):
        try:
            self.driver.find_element(By.XPATH, xpaths["stripe_email"]).clear()
            self.driver.find_element(By.XPATH, xpaths["stripe_email"]).send_keys("testuser@example.com")
            self.driver.find_element(By.XPATH, xpaths["card_number"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys(card_num)
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys(exp)
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).clear()
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys(cvc)
            billing = self.driver.find_element(By.XPATH, xpaths["billing_name"])
            billing.clear()
            billing.send_keys(name)
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Before_Submit", attachment_type=AttachmentType.PNG)
            self.wait_and_click(By.XPATH, xpaths["submit_payment"], label)
            time.sleep(5)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Stripe Error", attachment_type=AttachmentType.PNG)
            raise Exception(f"❌ Stripe form error: {e}")

    @allure.title("Guest PPV Payment Flow with Stripe")
    def test_updated_ppv_flow(self, browser_setup):
        self.driver = browser_setup

        with allure.step("Step 1: Load Homepage and Login"):
            self.driver.get(ReadConfig.getHomePageURL())
            self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
            self.login_and_profile()
            self.go_home_to_live()

        with allure.step("Step 2: Loop Through Categories"):
            categories = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
            if not categories:
                allure.attach(self.driver.get_screenshot_as_png(), name="No Categories", attachment_type=AttachmentType.PNG)
                raise AssertionError("❌ No categories found.")

            for cat_index in range(len(categories)):
                try:
                    self.go_home_to_live()
                    categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", categories[cat_index])
                    categories[cat_index].click()
                    allure.attach(body=f"📁 Opened Category {cat_index + 1}", name="Category Info", attachment_type=AttachmentType.TEXT)
                    time.sleep(2)

                    videos = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpaths["videos"])))
                    for vid_index in range(len(videos)):
                        try:
                            with allure.step(f"🎬 Try Video {vid_index + 1}"):
                                videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", videos[vid_index])
                                videos[vid_index].click()
                                time.sleep(2)

                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                                self.wait_and_click(By.XPATH, xpaths["ppv_button"], "PPV Button")
                                self.wait_and_click(By.XPATH, xpaths["confirm_ppv"], "Confirm PPV")

                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"])))

                                # ❌ Attempt 1 - Invalid card
                                self.enter_stripe_card("1234 5678 9012 3456", "12/30", "111", "Fail Test", "Invalid Stripe Submit")

                                # ✅ Attempt 2 - Valid card
                                self.enter_stripe_card("4242 4242 4242 4242", "12/55", "123", "Ruban Stripe", "Valid Stripe Submit")

                                allure.attach(self.driver.get_screenshot_as_png(), name="Payment Success", attachment_type=AttachmentType.PNG)
                                print("✅ Stripe payment completed successfully.")
                                return

                        except Exception as ve:
                            print(f"⚠️ Skipping video {vid_index + 1}: {ve}")
                            self.go_home_to_live()
                            categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                            categories[cat_index].click()
                            time.sleep(2)

                except Exception as ce:
                    print(f"⚠️ Skipping category {cat_index + 1}: {ce}")

        raise AssertionError("❌ No PPV video succeeded after all attempts.")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Browser already closed.")
