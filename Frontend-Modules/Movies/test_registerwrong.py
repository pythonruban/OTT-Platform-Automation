import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.readProp import ReadConfig  # Ensure this has getTestingemail & getTestpassword

xpaths = {
    # Login
    "login_icon": "(//button[@type='button'])[1]",
    "login_email": "//input[@name='email']",
    "login_password": "//input[@name='password']",
    "login_submit": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    # Live & Video
    "live_tab": "//li[@id='header-Live']",
    "categories": "//div[@class='card-image-container']",
    "videos": "//div[@class='homeListImage active']",
    "ppv_button": "//button[contains(@id,'rent-now-role')]",
    "confirm_ppv": "//button[@class='btn w-100 mb-2']",

    # Stripe
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_payment": "//div[@class='SubmitButton-IconContainer']",
}


@pytest.mark.usefixtures("browser_setup")
class TestGuestLoginPPVStripe:

    def test_updated_ppv_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        def wait_and_click(by, locator, label):
            try:
                elem = wait.until(EC.presence_of_element_located((by, locator)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
                wait.until(EC.element_to_be_clickable((by, locator))).click()
                print(f"✅ Clicked: {label}")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Failed to click {label}: {e}")
                raise

        def login_and_profile():
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["login_email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["login_password"]).send_keys(ReadConfig.getTestpassword())
            wait_and_click(By.XPATH, xpaths["login_submit"], "Login Submit")
            wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

        def go_home_to_live():
            self.driver.get(ReadConfig.getHomePageURL())
            wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab")

        def enter_stripe_card(card_num, exp, cvc, name, label):
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
            wait_and_click(By.XPATH, xpaths["submit_payment"], label)
            time.sleep(5)

        # Step 1: Load Homepage and Login
        self.driver.get(ReadConfig.getHomePageURL())
        wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
        login_and_profile()
        go_home_to_live()

        # Step 2: Loop Through Categories
        categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
        if not categories:
            raise AssertionError("❌ No categories found.")

        for cat_index in range(len(categories)):
            try:
                go_home_to_live()
                categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", categories[cat_index])
                categories[cat_index].click()
                print(f"📁 Opened Category {cat_index + 1}")
                time.sleep(2)

                videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["videos"])))
                for vid_index in range(len(videos)):
                    try:
                        videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", videos[vid_index])
                        videos[vid_index].click()
                        print(f"🎬 Opened Video {vid_index + 1}")
                        time.sleep(2)

                        # PPV Flow
                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                        wait_and_click(By.XPATH, xpaths["ppv_button"], "PPV Button")
                        wait_and_click(By.XPATH, xpaths["confirm_ppv"], "Confirm PPV")

                        # Stripe - Invalid Attempt
                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"])))
                        enter_stripe_card("1234 5678 9012 3456", "12/30", "111", "Fail Test", "Invalid Stripe Submit")

                        # Stripe - Valid Attempt
                        enter_stripe_card("4242 4242 4242 4242", "12/55", "123", "Ruban Stripe", "Valid Stripe Submit")

                        print("✅ Stripe payment completed successfully.")
                        return  # Stop after successful payment

                    except Exception as ve:
                        print(f"⚠️ Skipping video {vid_index + 1} in category {cat_index + 1}: {ve}")
                        go_home_to_live()
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
