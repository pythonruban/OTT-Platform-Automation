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
    "watch_now_btn": "//a[@id='watch-now-button']",
    "subscribe_now": "//a[@id='become-subscriber-button']",
    "plan_select": "//button[@class='p-2 start_payment_css btn theme-button-bg-color accessButton bgButton w-50']",
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

    def click(self, by, locator, label, scroll=True):
        try:
            wait = WebDriverWait(self.driver, 25)
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

    def test_ppv_invalid_payment_episode_watch(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        self.driver.get(ReadConfig.getHomePageURL())
        self.driver.maximize_window()

        try:
            # Step 1–6: Login and navigate to show
            self.click(By.XPATH, xpaths["login_icon"], "01_Login_Icon")
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Submitted", attachment_type=AttachmentType.PNG)
            self.click(By.XPATH, xpaths["choose_profile"], "03_Profile_Chosen")
            self.click(By.XPATH, xpaths["series_tab"], "04_Series_Tab")
            self.click(By.XPATH, xpaths["view_all_3"], "05_ViewAll_3")
            self.click(By.ID, xpaths["series_category_id"], "06_Series_Category")
            show_elem = wait.until(EC.element_to_be_clickable((By.ID, xpaths["video_block_id"])))
            self.driver.execute_script("arguments[0].click();", show_elem)
            print("✅ Show Clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Clicked", attachment_type=AttachmentType.PNG)

            # Step 7: Watch Now
            try:
                watch_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["watch_now_btn"])))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", watch_btn)
                time.sleep(1)
                try:
                    watch_btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", watch_btn)
                allure.attach(self.driver.get_screenshot_as_png(), name="08_WatchNow_Clicked", attachment_type=AttachmentType.PNG)
            except Exception as e:
                raise AssertionError(f"❌ Watch Now button failed: {str(e)}")

            # Step 8: Subscribe Now
            subscribe_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["subscribe_now"])))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", subscribe_btn)
            subscribe_btn.click()
            print("✅ Subscribe Now clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="09_SubscribeNow_Clicked", attachment_type=AttachmentType.PNG)

            # Step 9: Select plan
            self.click(By.XPATH, xpaths["plan_select"], "10_Plan_Select")

            # Step 10: Payment form
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["stripe_email"]))).send_keys("fail@test.com")
            self.driver.find_element(By.XPATH, xpaths["card_number"]).send_keys("4242 4242 4242 4242")
            self.driver.find_element(By.XPATH, xpaths["card_expiry"]).send_keys("12/30")
            self.driver.find_element(By.XPATH, xpaths["card_cvc"]).send_keys("111")
            self.driver.find_element(By.XPATH, xpaths["billing_name"]).send_keys("Ruban Fail")
            allure.attach(self.driver.get_screenshot_as_png(), name="11_Payment_Entered", attachment_type=AttachmentType.PNG)

            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
            submit_btn.click()
            print("✅ Payment submitted")
            time.sleep(15)

            # 🔁 Step 11–13: Retry show after payment
            self.click(By.XPATH, xpaths["series_tab"], "12_Series_Tab_Retry")
            self.click(By.XPATH, xpaths["view_all_3"], "13_ViewAll_3_Retry")
            self.click(By.ID, xpaths["series_category_id"], "14_Series_Category_Retry")

            show_elem = wait.until(EC.element_to_be_clickable((By.ID, xpaths["video_block_id"])))
            self.driver.execute_script("arguments[0].click();", show_elem)
            print("✅ Show Clicked After Payment")

            watch_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["watch_now_btn"])))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", watch_btn)
            watch_btn.click()
            print("✅ Watch Now After Payment")
            allure.attach(self.driver.get_screenshot_as_png(), name="15_Watch_After_Payment", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")
