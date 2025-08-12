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
    "watch_now_btn": "//img[@alt='Player 27']",
    "subscribe_now": "//button[@id='rent-now-role-4-button-seasons']",
    "plan_select": "(//button[@class='btn w-100 mb-2'])[2]",
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

        # Your previous steps...

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

            # Step 6: Click Video block (shows-4)
            show_elem = wait.until(EC.element_to_be_clickable((By.ID, xpaths["video_block_id"])))
            self.driver.execute_script("arguments[0].click();", show_elem)
            print("✅ Show Clicked")
            allure.attach(self.driver.get_screenshot_as_png(), name="07_Show_Clicked", attachment_type=AttachmentType.PNG)
            
            # Step 7: Click Watch Now
            try:
                watch_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["watch_now_btn"])))
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["watch_now_btn"])))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", watch_btn)
                time.sleep(1)

                # Attempt regular click for Watch Now
                try:
                    watch_btn.click()
                    print("✅ Watch Now clicked")
                    allure.attach(self.driver.get_screenshot_as_png(), name="11_WatchNow_Clicked", attachment_type=AttachmentType.PNG)
                except Exception as click_error:
                    # Fallback to JavaScript click for Watch Now
                    self.driver.execute_script("arguments[0].click();", watch_btn)
                    print("✅ Watch Now clicked via JS")
                    allure.attach(self.driver.get_screenshot_as_png(), name="11_WatchNow_JS_Clicked", attachment_type=AttachmentType.PNG)
                
                time.sleep(5)  # Wait after click for new elements to load

                # Step 8: Wait for Subscribe Now button to become visible
                subscribe_btn = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["subscribe_now"])))
                wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["subscribe_now"])))

                # Scroll to Subscribe Now button and click
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'})", subscribe_btn)
                time.sleep(1)
                subscribe_btn.click()
                print("✅ Subscribe Now clicked")
                allure.attach(self.driver.get_screenshot_as_png(), name="12_SubscribeNow_Clicked", attachment_type=AttachmentType.PNG)
                
                time.sleep(5)  # Wait after clicking Subscribe Now
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="10_WatchNow_Failed", attachment_type=AttachmentType.PNG)
                allure.attach(self.driver.get_screenshot_as_png(), name="12_SubscribeNow_Failed", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed in Watch Now and Subscribe flow: {str(e)}")
                
            print("✅ PPV Guest Episode Watch flow completed")

            click(By.XPATH, xpaths["plan_select"], "09_Plan_Selected")
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name="09_confrom_ppv_click", attachment_type=AttachmentType.PNG)

                        # Step 9: Stripe payment form
            try:
                # Enter Stripe Email (if required)
                stripe_email_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["stripe_email"])))
                stripe_email_field.send_keys("fail@test.com")
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_Email_Entered", attachment_type=AttachmentType.PNG)

                # Enter Stripe Card Number
                card_number_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["card_number"])))
                card_number_field.send_keys("4242 4242 4242 4242")  # Sample card number for testing
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_CardNumber_Entered", attachment_type=AttachmentType.PNG)

                # Enter Card Expiry Date (MM/YY)
                card_expiry_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["card_expiry"])))
                card_expiry_field.send_keys("12/30")
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_CardExpiry_Entered", attachment_type=AttachmentType.PNG)

                # Enter Card CVC
                card_cvc_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["card_cvc"])))
                card_cvc_field.send_keys("111")
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_CardCVC_Entered", attachment_type=AttachmentType.PNG)

                # Enter Billing Name
                billing_name_field = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["billing_name"])))
                billing_name_field.send_keys("Ruban Fail")
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_BillingName_Entered", attachment_type=AttachmentType.PNG)

                # Wait a few seconds to ensure everything is properly entered
                time.sleep(2)

                # Step 10: Submit the payment
                submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["submit_btn"])))
                submit_btn.click()
                print("✅ Payment form submitted")
                allure.attach(self.driver.get_screenshot_as_png(), name="10_Payment_Form_Submitted", attachment_type=AttachmentType.PNG)

                # Wait for a few seconds after form submission
                time.sleep(5)
                allure.attach(self.driver.get_screenshot_as_png(), name="10_Payment_Success", attachment_type=AttachmentType.PNG)
                time.sleep(15)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="09_Payment_Failure", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to enter payment details or submit: {str(e)}")
            

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failure", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Test failed: {str(e)}")
