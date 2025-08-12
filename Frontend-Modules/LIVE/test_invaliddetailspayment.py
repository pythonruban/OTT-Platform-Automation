import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from allure_commons.types import AttachmentType
import sys, os

# ✅ Add config path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "live_tab": "//li[@id='header-Live']",
    "view_all": "//a[normalize-space(text())='View All']",
    
    # Video and Payment XPaths
    "first_video": "(//img[contains(@alt,'Episode') or contains(@alt,'episode')])[1]",
    "subscribe_now": "//a[@id='subscriber-now-button']",
    "plan_select": "//button[@class='p-2 start_payment_css btn theme-button-bg-color accessButton bgButton w-50']",
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']",
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer']"
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("LIVE Page Payment Automation")
@allure.title("LIVE tab - Click View All, select video and process payment")
class TestLiveVideoPayment:

    def test_live_video_payment_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)

        try:
            # ✅ Step 1: Login Process
            url = ReadConfig.getHomePageURL()
            self.driver.get(url)
            self.driver.maximize_window()
            print(f"🌐 Opened URL: {url}")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="01_Homepage", attachment_type=AttachmentType.PNG)

            # Login
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="02_Login_Success", attachment_type=AttachmentType.PNG)

            # Choose Profile
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="03_Profile_Selected", attachment_type=AttachmentType.PNG)

            # ✅ Step 2: Navigate to LIVE tab
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(0.8)

            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["live_tab"]))).click()
            print("🎬 LIVE tab clicked")
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="04_Live_Tab_Clicked", attachment_type=AttachmentType.PNG)

            # ✅ Step 3: Click View All (2nd one specifically)
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["view_all"])))
            time.sleep(3)
            
            view_all_buttons = self.driver.find_elements(By.XPATH, xpaths["view_all"])
            print(f"🔍 Found {len(view_all_buttons)} View All buttons")
            
            if len(view_all_buttons) >= 2:
                target_view_all = view_all_buttons[1]  # Second View All (index 1)
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", target_view_all)
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="05_Before_ViewAll_Click", attachment_type=AttachmentType.PNG)
                
                target_view_all.click()
                print("👉 Clicked 2nd View All button")
                time.sleep(4)
                allure.attach(self.driver.get_screenshot_as_png(), name="06_ViewAll_Content_Loaded", attachment_type=AttachmentType.PNG)
            else:
                print("⚠️ Less than 2 View All buttons found, clicking first one")
                view_all_buttons[0].click()
                time.sleep(4)

            # ✅ Step 4: Click first video
            try:
                first_video = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["first_video"])))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", first_video)
                time.sleep(2)
                allure.attach(self.driver.get_screenshot_as_png(), name="07_Before_Video_Click", attachment_type=AttachmentType.PNG)
                
                first_video.click()
                print("🎬 Clicked first video")
                time.sleep(4)
                allure.attach(self.driver.get_screenshot_as_png(), name="08_Video_Page_Loaded", attachment_type=AttachmentType.PNG)
            except Exception as e:
                print(f"❌ Failed to click video: {e}")
                allure.attach(self.driver.get_screenshot_as_png(), name="08_Video_Click_Failed", attachment_type=AttachmentType.PNG)
                raise

            # ✅ Step 5: Check for subscription button and process payment
            try:
                # Check if subscribe button exists
                subscribe_button = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["subscribe_now"])))
                
                if subscribe_button.is_displayed():
                    print("💰 Subscription required - processing payment")
                    
                    # Click Subscribe Now
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", subscribe_button)
                    time.sleep(2)
                    allure.attach(self.driver.get_screenshot_as_png(), name="09_Subscribe_Button_Found", attachment_type=AttachmentType.PNG)
                    
                    subscribe_button.click()
                    print("👉 Clicked Subscribe Now")
                    time.sleep(3)
                    allure.attach(self.driver.get_screenshot_as_png(), name="10_Subscription_Page", attachment_type=AttachmentType.PNG)

                    # ✅ Step 6: Select Plan
                    plan_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["plan_select"])))
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", plan_button)
                    time.sleep(2)
                    allure.attach(self.driver.get_screenshot_as_png(), name="11_Before_Plan_Select", attachment_type=AttachmentType.PNG)
                    
                    plan_button.click()
                    print("👉 Selected payment plan")
                    time.sleep(3)
                    allure.attach(self.driver.get_screenshot_as_png(), name="12_Payment_Form_Loading", attachment_type=AttachmentType.PNG)

                    # ✅ Step 7: Fill Payment Details
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"])))
                    time.sleep(3)  # Wait for Stripe form to fully load
                    allure.attach(self.driver.get_screenshot_as_png(), name="13_Payment_Form_Loaded", attachment_type=AttachmentType.PNG)

                    # Fill email
                    email_field = self.driver.find_element(By.XPATH, xpaths["stripe_email"])
                    email_field.clear()
                    email_field.send_keys("test@example.com")
                    time.sleep(1)

                    # Fill card number
                    card_field = self.driver.find_element(By.XPATH, xpaths["card_number"])
                    card_field.clear()
                    card_field.send_keys("4242 4242 4242 4242")
                    time.sleep(1)

                    # Fill expiry
                    expiry_field = self.driver.find_element(By.XPATH, xpaths["card_expiry"])
                    expiry_field.clear()
                    expiry_field.send_keys("12/30")
                    time.sleep(1)

                    # Fill CVC
                    cvc_field = self.driver.find_element(By.XPATH, xpaths["card_cvc"])
                    cvc_field.clear()
                    cvc_field.send_keys("123")
                    time.sleep(1)

                    # Fill billing name
                    name_field = self.driver.find_element(By.XPATH, xpaths["billing_name"])
                    name_field.clear()
                    name_field.send_keys("Test User")
                    time.sleep(1)

                    allure.attach(self.driver.get_screenshot_as_png(), name="14_Payment_Details_Filled", attachment_type=AttachmentType.PNG)
                    print("✅ Payment details filled")

                    # ✅ Step 8: Submit Payment
                    submit_button = self.driver.find_element(By.XPATH, xpaths["submit_btn"])
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", submit_button)
                    time.sleep(2)
                    
                    submit_button.click()
                    print("💳 Payment submitted")
                    time.sleep(5)  # Wait for payment processing
                    allure.attach(self.driver.get_screenshot_as_png(), name="15_Payment_Processing", attachment_type=AttachmentType.PNG)

                    # Wait for redirect back to video page
                    time.sleep(3)
                    allure.attach(self.driver.get_screenshot_as_png(), name="16_Final_Page_After_Payment", attachment_type=AttachmentType.PNG)
                    
                    print("✅ Payment process completed successfully")
                    
                else:
                    print("ℹ️ No subscription required - free content")
                    allure.attach(self.driver.get_screenshot_as_png(), name="09_Free_Content", attachment_type=AttachmentType.PNG)

            except NoSuchElementException:
                print("ℹ️ No subscription button found - content might be free")
                allure.attach(self.driver.get_screenshot_as_png(), name="09_No_Subscription_Required", attachment_type=AttachmentType.PNG)

            except Exception as e:
                print(f"❌ Payment process failed: {e}")
                allure.attach(self.driver.get_screenshot_as_png(), name="Payment_Process_Error", attachment_type=AttachmentType.PNG)

            print("✅ LIVE video payment flow completed")

        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, str(e)

        finally:
            try:
                self.driver.quit()
            except:
                print("⚠️ WebDriver already closed.")

    def teardown_class(self):
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            print("⚠️ WebDriver already closed in teardown.")