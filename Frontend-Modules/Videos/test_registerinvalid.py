import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "login_email": "//input[@name='email']",
    "login_password": "//input[@name='password']",
    "login_submit": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    "category_tab": "//li[@id='header-Categories']",
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
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                wait.until(EC.element_to_be_clickable((by, locator))).click()
                print(f"✅ Clicked: {label}")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Failed to click {label}: {e}")
                raise

        def login_and_profile():
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["login_email"]))).send_keys("ruban.k@webnexs.in")
            self.driver.find_element(By.XPATH, xpaths["login_password"]).send_keys("program12@12A")
            wait_and_click(By.XPATH, xpaths["login_submit"], "Login Submit")
            wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

        def go_home_to_category():
            self.driver.get(ReadConfig.getHomePageURL())
            wait_and_click(By.XPATH, xpaths["category_tab"], "category Tab")

        # Step 1: Open Home → Login
        self.driver.get(ReadConfig.getHomePageURL())
        wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon")
        login_and_profile()
        go_home_to_category()
        view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
        wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

        categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))

        if not categories:
            raise AssertionError("❌ No categories found.")

        for cat_index in range(len(categories)):
            try:
                go_home_to_category()
                categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", categories[cat_index])
                categories[cat_index].click()
                print(f"📁 Opened Category {cat_index}")
                time.sleep(2)

                videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["videos"])))

                for vid_index in range(len(videos)):
                    try:
                        videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[vid_index])
                        videos[vid_index].click()
                        print(f"🎬 Opened Video {vid_index}")
                        time.sleep(2)

                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                        wait_and_click(By.XPATH, xpaths["ppv_button"], "PPV Button")
                        wait_and_click(By.XPATH, xpaths["confirm_ppv"], "Confirm PPV")

                        # Stripe - Invalid
                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
                        self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("1234 5678 9012 3456")
                        self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
                        self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
                        self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Fail Test")
                        wait_and_click(By.XPATH, xpaths["submit_payment"], "Invalid Stripe Submit")
                        time.sleep(3)

                        time.sleep(10)

                    except Exception as ve:
                        print(f"❌ Skipping video {vid_index}: {ve}")
                        go_home_to_category()
                        categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                        categories[cat_index].click()
                        time.sleep(2)

            except Exception as ce:
                print(f"⚠️ Skipping category {cat_index}: {ce}")

        raise AssertionError("❌ No PPV video succeeded after all attempts.")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
