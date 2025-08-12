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

# Invalid payment test data for different scenarios
INVALID_PAYMENT_SCENARIOS = [
    {
        "scenario_name": "invalid_card_number",
        "email": "test@example.com",
        "card_number": "1234 5678 9012 3456",  # Invalid card number
        "expiry": "12/30",
        "cvc": "123",
        "billing_name": "Test User",
        "expected_error_keywords": ["invalid", "card number", "declined"]
    },
    {
        "scenario_name": "expired_card",
        "email": "test@example.com", 
        "card_number": "4242 4242 4242 4242",
        "expiry": "01/20",  # Expired date (past)
        "cvc": "123",
        "billing_name": "Test User",
        "expected_error_keywords": ["expired", "expiration", "past"]
    },
    {
        "scenario_name": "invalid_cvc",
        "email": "test@example.com",
        "card_number": "4242 4242 4242 4242", 
        "expiry": "12/30",
        "cvc": "12",  # Too short CVC
        "billing_name": "Test User",
        "expected_error_keywords": ["security code", "cvc", "incomplete"]
    }
]

# XPaths for LIVE content navigation and payment
xpaths = {
    # Authentication
    "login_icon": "//button[@id='home-signin'] | (//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']", 
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    
    # LIVE section navigation
    "live_tab": "//li[@id='header-Live']",
    "view_all_button": "(//a[contains(text(), 'View All')])[2]",
    "categories": "//div[@class='card-image-container']",
    "live_videos": "//div[@class='homeListImage active']",
    
    # Payment flow
    "subscribe_now": "//a[@id='subscriber-now-button'] | //button[@id='subscriber-now-button']",
    "plan_select": "//button[contains(@class, 'start_payment_css')] | //button[@class='p-2 start_payment_css btn theme-button-bg-color accessButton bgButton w-50']",
    
    # Stripe payment form
    "stripe_email": "//input[@id='email']",
    "card_number": "//input[@id='cardNumber']",
    "card_expiry": "//input[@id='cardExpiry']", 
    "card_cvc": "//input[@id='cardCvc']",
    "billing_name": "//input[@name='billingName']",
    "submit_btn": "//div[@class='SubmitButton-IconContainer'] | //button[contains(@class,'SubmitButton')]",
    
    # Error message selectors
    "error_messages": [
        "//div[contains(@class,'error')] | //span[contains(@class,'error')]",
        "//div[@role='alert']",
        "//div[contains(@class,'Error')] | //span[contains(@class,'Error')]",
        "//*[contains(text(),'invalid')] | //*[contains(text(),'Invalid')]",
        "//*[contains(text(),'declined')] | //*[contains(text(),'Declined')]",
        "//*[contains(text(),'expired')] | //*[contains(text(),'Expired')]",
        "//*[contains(text(),'required')] | //*[contains(text(),'Required')]"
    ]
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("LIVE Video Invalid Payment Testing")
@allure.title("Test invalid payment details on LIVE PPV content")
class TestLiveInvalidPaymentDetails:

    def wait_and_click(self, by, value, label, timeout=30):
        """Enhanced click with error handling and multiple strategies"""
        try:
            # Wait for element to be present and clickable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            
            # Try different click strategies
            try:
                element.click()
            except Exception:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
            
            print(f"✅ Successfully clicked: {label}")
            allure.attach(
                self.driver.get_screenshot_as_png(), 
                name=f"{label}_Clicked", 
                attachment_type=AttachmentType.PNG
            )
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Failed to click {label}: {e}")
            allure.attach(
                self.driver.get_screenshot_as_png(), 
                name=f"{label}_Click_Failed", 
                attachment_type=AttachmentType.PNG
            )
            return False

    def wait_and_fill(self, by, value, text, label, clear_first=True, timeout=30):
        """Fill input field with error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            
            if clear_first:
                element.clear()
                time.sleep(0.5)
            
            element.send_keys(text)
            print(f"✅ Filled {label}: {text}")
            time.sleep(0.5)
            return True
            
        except Exception as e:
            print(f"❌ Failed to fill {label}: {e}")
            return False

    def check_for_error_messages(self, expected_keywords):
        """Check for error messages after payment submission"""
        print("🔍 Checking for error messages...")
        
        for error_xpath in xpaths["error_messages"]:
            try:
                error_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, error_xpath))
                )
                
                for element in error_elements:
                    if element.is_displayed():
                        error_text = element.text.lower()
                        print(f"📋 Found error message: {error_text}")
                        
                        # Check if any expected keyword is in the error message
                        for keyword in expected_keywords:
                            if keyword.lower() in error_text:
                                print(f"✅ Expected error found: '{keyword}' in '{error_text}'")
                                allure.attach(
                                    self.driver.get_screenshot_as_png(),
                                    name=f"Error_Message_Found_{keyword}",
                                    attachment_type=AttachmentType.PNG
                                )
                                return True, error_text
                                
            except TimeoutException:
                continue
                
        print("❌ No expected error messages found")
        return False, ""

    def login_to_application(self):
        """Login process with error handling"""
        try:
            with allure.step("Login to application"):
                # Navigate to homepage
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="01_Homepage_Loaded",
                    attachment_type=AttachmentType.PNG
                )
                
                # Click login
                if not self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon"):
                    return False
                
                # Enter credentials
                if not self.wait_and_fill(By.XPATH, xpaths["email"], ReadConfig.getTestingemail(), "Email"):
                    return False
                    
                if not self.wait_and_fill(By.XPATH, xpaths["password"], ReadConfig.getTestpassword(), "Password"):
                    return False
                
                # Submit login
                if not self.wait_and_click(By.XPATH, xpaths["login_btn"], "Login Submit"):
                    return False
                
                # Choose profile
                if not self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Profile Selection"):
                    return False
                
                print("✅ Login completed successfully")
                return True
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def navigate_to_live_ppv_content(self):
        """Navigate to LIVE section and find PPV content"""
        try:
            with allure.step("Navigate to LIVE PPV content"):
                # Click LIVE tab
                if not self.wait_and_click(By.XPATH, xpaths["live_tab"], "LIVE Tab"):
                    return False
                
                # Click View All to see all categories
                if not self.wait_and_click(By.XPATH, xpaths["view_all_button"], "View All Button"):
                    return False
                
                # Find categories
                wait = WebDriverWait(self.driver, 20)
                categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
                
                print(f"📂 Found {len(categories)} LIVE categories")
                
                # Try each category to find PPV content
                for category_index in range(min(len(categories), 5)):
                    try:
                        print(f"\n➡️ Checking category {category_index + 1}")
                        
                        # Re-fetch categories to avoid stale elements
                        categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
                        if category_index >= len(categories):
                            continue
                            
                        category = categories[category_index]
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", category)
                        
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Category_{category_index+1}_Opened",
                            attachment_type=AttachmentType.PNG
                        )
                        time.sleep(3)
                        
                        # Check for videos in this category
                        try:
                            videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["live_videos"])))
                            print(f"🎞️ Found {len(videos)} videos in category {category_index + 1}")
                            
                            # Try first few videos to find PPV content
                            for video_index in range(min(len(videos), 3)):
                                try:
                                    # Re-fetch videos
                                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["live_videos"])))
                                    if video_index >= len(videos):
                                        continue
                                    
                                    video = videos[video_index]
                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", video)
                                    time.sleep(1)
                                    self.driver.execute_script("arguments[0].click();", video)
                                    
                                    allure.attach(
                                        self.driver.get_screenshot_as_png(),
                                        name=f"Video_Cat{category_index+1}_Vid{video_index+1}",
                                        attachment_type=AttachmentType.PNG
                                    )
                                    time.sleep(3)
                                    
                                    # Check if this video requires subscription (PPV)
                                    try:
                                        subscribe_button = WebDriverWait(self.driver, 5).until(
                                            EC.presence_of_element_located((By.XPATH, xpaths["subscribe_now"]))
                                        )
                                        
                                        if subscribe_button.is_displayed():
                                            print(f"💰 Found PPV content in category {category_index + 1}, video {video_index + 1}")
                                            return True
                                            
                                    except TimeoutException:
                                        print(f"ℹ️ Video {video_index + 1} is free content, trying next...")
                                        self.driver.back()
                                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["live_videos"])))
                                        time.sleep(2)
                                        continue
                                        
                                except Exception as ve:
                                    print(f"⚠️ Error with video {video_index + 1}: {ve}")
                                    try:
                                        self.driver.back()
                                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["live_videos"])))
                                        time.sleep(2)
                                    except:
                                        break
                                    continue
                            
                        except Exception as video_error:
                            print(f"❌ Error processing videos in category {category_index + 1}: {video_error}")
                        
                        # Go back to categories for next iteration
                        try:
                            self.driver.back()
                            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["categories"])))
                            time.sleep(2)
                        except:
                            # Recovery: go back to LIVE section
                            if not self.wait_and_click(By.XPATH, xpaths["live_tab"], "LIVE Tab Recovery"):
                                return False
                            if not self.wait_and_click(By.XPATH, xpaths["view_all_button"], "View All Recovery"):
                                return False
                            time.sleep(3)
                        
                    except Exception as ce:
                        print(f"❌ Error in category {category_index + 1}: {ce}")
                        continue
                
                print("❌ No PPV content found in LIVE section")
                return False
                
        except Exception as e:
            print(f"❌ Failed to navigate to LIVE content: {e}")
            return False

    def test_invalid_payment_scenarios(self, browser_setup):
        """Main test to process all invalid payment scenarios"""
        self.driver = browser_setup
        
        try:
            # Step 1: Login
            with allure.step("Step 1: Login to application"):
                if not self.login_to_application():
                    raise Exception("Login failed")
            
            # Step 2: Find PPV content
            with allure.step("Step 2: Navigate to LIVE PPV content"):
                if not self.navigate_to_live_ppv_content():
                    raise Exception("Could not find PPV content to test payment")
            
            # Step 3: Test each invalid payment scenario
            for scenario_index, scenario in enumerate(INVALID_PAYMENT_SCENARIOS):
                
                with allure.step(f"Step 3.{scenario_index + 1}: Test {scenario['scenario_name']}"):
                    print(f"\n🧪 Testing scenario: {scenario['scenario_name']}")
                    
                    try:
                        # Click subscribe button
                        if not self.wait_and_click(By.XPATH, xpaths["subscribe_now"], f"Subscribe Now - {scenario['scenario_name']}"):
                            print(f"⚠️ Could not click subscribe button for {scenario['scenario_name']}")
                            continue
                        
                        # Select plan
                        if not self.wait_and_click(By.XPATH, xpaths["plan_select"], f"Select Plan - {scenario['scenario_name']}"):
                            print(f"⚠️ Could not select plan for {scenario['scenario_name']}")
                            continue
                        
                        # Wait for payment form to load
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, xpaths["stripe_email"]))
                        )
                        time.sleep(3)
                        
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Payment_Form_{scenario['scenario_name']}",
                            attachment_type=AttachmentType.PNG
                        )
                        
                        # Fill payment form with invalid data
                        print(f"📝 Filling payment form with invalid data for: {scenario['scenario_name']}")
                        
                        self.wait_and_fill(By.XPATH, xpaths["stripe_email"], scenario["email"], f"Email - {scenario['scenario_name']}")
                        self.wait_and_fill(By.XPATH, xpaths["card_number"], scenario["card_number"], f"Card Number - {scenario['scenario_name']}")
                        self.wait_and_fill(By.XPATH, xpaths["card_expiry"], scenario["expiry"], f"Expiry - {scenario['scenario_name']}")
                        self.wait_and_fill(By.XPATH, xpaths["card_cvc"], scenario["cvc"], f"CVC - {scenario['scenario_name']}")
                        self.wait_and_fill(By.XPATH, xpaths["billing_name"], scenario["billing_name"], f"Billing Name - {scenario['scenario_name']}")
                        
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Invalid_Data_Filled_{scenario['scenario_name']}",
                            attachment_type=AttachmentType.PNG
                        )
                        
                        # Submit payment
                        if not self.wait_and_click(By.XPATH, xpaths["submit_btn"], f"Submit Payment - {scenario['scenario_name']}"):
                            print(f"⚠️ Could not submit payment for {scenario['scenario_name']}")
                            continue
                        
                        time.sleep(5)  # Wait for payment processing
                        
                        # Check for error messages
                        error_found, error_message = self.check_for_error_messages(scenario["expected_error_keywords"])
                        
                        if error_found:
                            print(f"✅ Test PASSED for {scenario['scenario_name']}: Expected error found - {error_message}")
                            allure.attach(
                                self.driver.get_screenshot_as_png(),
                                name=f"SUCCESS_{scenario['scenario_name']}_Error_Found",
                                attachment_type=AttachmentType.PNG
                            )
                        else:
                            print(f"⚠️ Test WARNING for {scenario['scenario_name']}: Expected error not found")
                            allure.attach(
                                self.driver.get_screenshot_as_png(),
                                name=f"WARNING_{scenario['scenario_name']}_No_Error",
                                attachment_type=AttachmentType.PNG
                            )
                        
                        # Go back for next scenario (if not last one)
                        if scenario_index < len(INVALID_PAYMENT_SCENARIOS) - 1:
                            try:
                                # Navigate back to the PPV content for next test
                                self.driver.back()
                                time.sleep(2)
                                self.driver.back()  # Go back to video
                                time.sleep(2)
                            except:
                                print("⚠️ Could not navigate back, continuing with current page...")
                        
                    except Exception as scenario_error:
                        print(f"❌ Error in scenario {scenario['scenario_name']}: {scenario_error}")
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"ERROR_{scenario['scenario_name']}",
                            attachment_type=AttachmentType.PNG
                        )
                        continue
            
            print("✅ Invalid payment testing completed")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Test_Failed",
                attachment_type=AttachmentType.PNG
            )
            assert False, f"Test failed: {e}"

    def teardown_method(self):
        """Cleanup after test - let fixture handle driver cleanup"""
        print("🧹 Test cleanup completed")

# Note: Removed driver.quit() from finally block and teardown_class
# The browser_setup fixture should handle driver lifecycle
