import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
import sys, os

# Config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

# All XPaths and IDs
xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "series_tab": "//li[@id='header-Tv Show']",
    "view_all_3": "(//a[text()='View All'])[3]",
    "series_category_id": "series-genre-5",
    "video_block_id": "shows-4",
    "watch_now_btn": "watch-now-button",
    "subscribe_now": "//button[@id='rent-now-role-4-button']",
    "plan_select": "//button[@class='btn w-100 mb-2']",
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("PPV Guest Watch Flow")
@allure.title("User watches PPV episode through series category")
class TestPPVEpisodeWatch:

    def test_ppv_invalid_payment_episode_watch(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        self.driver.get(ReadConfig.getHomePageURL())
        self.driver.maximize_window()

        def click(by, locator, label, scroll=True):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", elem)
                    time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label}: {e}")

        try:
            # Step 1: Login
            click(By.XPATH, xpaths["login_icon"], "01_Login_Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Submitted", attachment_type=AttachmentType.PNG)

            # Step 2: Choose profile
            click(By.XPATH, xpaths["choose_profile"], "03_Profile_Chosen")

            # Step 3: Series tab
            click(By.XPATH, xpaths["series_tab"], "04_Series_Tab")

            # Step 4: View All (3rd)
            click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")

            # Step 5: Category - genre 5
            click(By.ID, xpaths["series_category_id"], "06_Series_Category")

            # Step 6: Click Video block (shows-5)
            show_elem = wait.until(EC.element_to_be_clickable((By.ID, xpaths["video_block_id"])))
            self.driver.execute_script("arguments[0].click();", show_elem)
            print("✅ Show Clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Clicked", attachment_type=AttachmentType.PNG)

            # Step 7: Click Subscribe Now
            click(By.XPATH, xpaths["subscribe_now"], "08_Subscribe_Now")
            allure.attach(self.driver.get_screenshot_as_png(), name="08_ppv_button_click", attachment_type=AttachmentType.PNG)
            # Step 8: Select Plan
            click(By.XPATH, xpaths["plan_select"], "09_Plan_Selected")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="09_confrom_ppv_click", attachment_type=AttachmentType.PNG)

            # Step 9: Stripe payment form
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("1234 5678 9012 3456")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
            self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Ruban Fail")
            time.sleep(4)
            allure.attach(self.driver.get_screenshot_as_png(), name="08_ppv_payment_invalid_card", attachment_type=AttachmentType.PNG)
            

            # Submit Payment
            self.driver.find_element(By.XPATH, xpaths["submit_btn"]).click()
            print("✅ Payment failed")
            
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")
