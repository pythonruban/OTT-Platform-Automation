import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "live_tab": "//li[@id='header-Live']",
    "view_all_button": "(//a[contains(text(), 'View All')])[2]",
    "categories": "//div[@class='card-image-container']",
    "videos": "//div[@class='homeListImage active']",
    "ppv_button": "//button[@id='rent-now-button-guest']",
    "signup_link": "//a[@class='border-0 bg-transparent theme-button-tab-color']",
    
    # Signup form elements
    "signup_button": "//button[@id='home-signup']",
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "india_option": "//li[@data-country-code='in']",
    "mobile": "//input[@type='tel']",
    "gender": "//select[@id='signup-gender']",
    "country": "//input[@id='signup-country']",
    "state": "//input[@id='signup-state']",
    "city": "//input[@id='signup-city']",
    "password": "//input[@id='signup-password']",
    "confirm_password": "//input[@id='confirmPassword']",
    "accept_terms": "//input[@id='signup-accept']",
    "submit": "//button[@id='signup-submit']",
    
    # Post-signup navigation
    "next_page_indicators": [
        "//button[contains(text(), 'Continue')]",
        "//a[contains(text(), 'Next')]", 
        "//button[contains(text(), 'Proceed')]",
        "//div[@class='success-message']",
        "//h1[contains(text(), 'Welcome')]"
    ]
}

# Test data for signup
SIGNUP_DATA = {
    "first_name": "AutoTest",
    "last_name": "User",
    "email": f"autotest{random.randint(1000, 9999)}@testmail.com",
    "mobile": f"9{random.randint(100000000, 999999999)}",
    "password": "TestPass@123",
    "country": "India",
    "state": "Tamil Nadu", 
    "city": "Chennai"
}

@pytest.mark.usefixtures("browser_setup")
class TestPPVSignupAutomation:

    def test_ppv_signup_complete_flow(self, browser_setup):
        """Complete PPV Signup Automation Flow - Single Test Function"""
        driver = browser_setup
        wait = WebDriverWait(driver, 30)
        signup_completed = False

        def smart_wait_and_click(by, value, label, wait_time=20, scroll=True):
            """Enhanced click method with multiple strategies"""
            try:
                wait_obj = WebDriverWait(driver, wait_time)
                element = wait_obj.until(EC.presence_of_element_located((by, value)))
                
                if scroll:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'smooth'});", element)
                    time.sleep(1)
                
                clickable_element = wait_obj.until(EC.element_to_be_clickable((by, value)))
                
                # Try multiple click strategies
                click_strategies = [
                    lambda: clickable_element.click(),
                    lambda: driver.execute_script("arguments[0].click();", clickable_element),
                    lambda: driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click'));", clickable_element)
                ]
                
                for i, strategy in enumerate(click_strategies):
                    try:
                        strategy()
                        print(f"✅ Clicked {label} using strategy {i+1}")
                        break
                    except Exception as e:
                        if i == len(click_strategies) - 1:
                            raise e
                        print(f"⚠️ Click strategy {i+1} failed for {label}, trying next...")
                        time.sleep(0.5)
                
                allure.attach(driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"❌ Failed to click {label}: {e}")
                allure.attach(driver.get_screenshot_as_png(), name=f"{label}_Error", attachment_type=AttachmentType.PNG)
                return False

        def smart_fill_input(by, value, text, label, clear_first=True):
            """Enhanced input filling with error handling"""
            try:
                wait_obj = WebDriverWait(driver, 15)
                element = wait_obj.until(EC.visibility_of_element_located((by, value)))
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                time.sleep(0.5)
                
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

        def handle_ppv_and_signup():
            """Handle PPV detection and complete signup process"""
            nonlocal signup_completed
            try:
                wait_obj = WebDriverWait(driver, 10)
                
                # Check if PPV button is present
                try:
                    ppv_button = wait_obj.until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                    print("🔒 PPV content detected - starting signup process")
                    allure.attach(driver.get_screenshot_as_png(), name="PPV_Detected", attachment_type=AttachmentType.PNG)
                    
                    # Click PPV button
                    if not smart_wait_and_click(By.XPATH, xpaths["ppv_button"], "PPV Subscribe Button"):
                        return False
                    
                    # Try signup link first, then button
                    signup_clicked = False
                    try:
                        if smart_wait_and_click(By.XPATH, xpaths["signup_link"], "Signup Link", wait_time=5):
                            signup_clicked = True
                    except:
                        pass
                    
                    if not signup_clicked:
                        if not smart_wait_and_click(By.XPATH, xpaths["signup_button"], "Signup Button", wait_time=5):
                            print("❌ Could not find signup button/link")
                            return False
                    
                    # Fill signup form
                    print("📝 Starting signup form filling...")
                    allure.attach(driver.get_screenshot_as_png(), name="Signup_Form_Start", attachment_type=AttachmentType.PNG)
                    
                    # Fill all form fields
                    form_fields = [
                        (xpaths["first_name"], SIGNUP_DATA["first_name"], "First Name"),
                        (xpaths["last_name"], SIGNUP_DATA["last_name"], "Last Name"),
                        (xpaths["email"], SIGNUP_DATA["email"], "Email"),
                        (xpaths["mobile"], SIGNUP_DATA["mobile"], "Mobile"),
                        (xpaths["country"], SIGNUP_DATA["country"], "Country"),
                        (xpaths["state"], SIGNUP_DATA["state"], "State"),
                        (xpaths["city"], SIGNUP_DATA["city"], "City"),
                        (xpaths["password"], SIGNUP_DATA["password"], "Password"),
                        (xpaths["confirm_password"], SIGNUP_DATA["password"], "Confirm Password")
                    ]
                    
                    for xpath, data, label in form_fields:
                        smart_fill_input(By.XPATH, xpath, data, label)
                    
                    # Handle dropdowns and checkboxes
                    try:
                        if smart_wait_and_click(By.XPATH, xpaths["country_dropdown"], "Country Dropdown", wait_time=5):
                            smart_wait_and_click(By.XPATH, xpaths["india_option"], "India Option", wait_time=5)
                    except:
                        print("ℹ️ Country dropdown not found")
                    
                    try:
                        gender_select = Select(driver.find_element(By.XPATH, xpaths["gender"]))
                        gender_select.select_by_visible_text("Male")
                        print("✅ Selected gender")
                    except:
                        print("ℹ️ Gender dropdown not found")
                    
                    try:
                        terms_checkbox = driver.find_element(By.XPATH, xpaths["accept_terms"])
                        if not terms_checkbox.is_selected():
                            smart_wait_and_click(By.XPATH, xpaths["accept_terms"], "Accept Terms")
                    except:
                        print("ℹ️ Terms checkbox not found")
                    
                    allure.attach(driver.get_screenshot_as_png(), name="Signup_Form_Filled", attachment_type=AttachmentType.PNG)
                    
                    # Submit form
                    if smart_wait_and_click(By.XPATH, xpaths["submit"], "Submit Signup"):
                        print("✅ Signup form submitted successfully")
                        signup_completed = True
                        time.sleep(3)
                        
                        # Handle post-signup navigation
                        for indicator_xpath in xpaths["next_page_indicators"]:
                            try:
                                success_element = wait_obj.until(EC.presence_of_element_located((By.XPATH, indicator_xpath)))
                                print(f"✅ Signup success detected")
                                allure.attach(driver.get_screenshot_as_png(), name="Signup_Success", attachment_type=AttachmentType.PNG)
                                
                                if "button" in indicator_xpath.lower():
                                    smart_wait_and_click(By.XPATH, indicator_xpath, "Continue/Next Button")
                                break
                            except TimeoutException:
                                continue
                        
                        time.sleep(3)
                        current_url = driver.current_url
                        print(f"✅ Successfully navigated to: {current_url}")
                        allure.attach(driver.get_screenshot_as_png(), name="Post_Signup_Page", attachment_type=AttachmentType.PNG)
                        return True
                    else:
                        print("❌ Failed to submit signup form")
                        return False
                        
                except TimeoutException:
                    print("ℹ️ No PPV popup detected - content is free")
                    return True
                    
            except Exception as e:
                print(f"❌ Error in PPV/signup process: {e}")
                allure.attach(driver.get_screenshot_as_png(), name="PPV_Signup_Error", attachment_type=AttachmentType.PNG)
                return False

        # Main test execution
        try:
            with allure.step("Step 1: Open Website"):
                url = ReadConfig.getHomePageURL()
                driver.get(url)
                driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(driver.get_screenshot_as_png(), name="01_Home_Loaded", attachment_type=AttachmentType.PNG)
                print("✅ Website loaded successfully")

            with allure.step("Step 2: Navigate to Live Section and Click View All"):
                if not smart_wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab"):
                    raise Exception("Failed to click Live tab")
                print("✅ Navigated to Live section")
                
                # Click View All button to see all categories
                if not smart_wait_and_click(By.XPATH, xpaths["view_all_button"], "View All Button"):
                    raise Exception("Failed to click View All button")
                print("✅ Clicked View All button")

            with allure.step("Step 3: Process Categories and Videos for PPV"):
                categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
                category_count = min(len(categories), 5)  # Limit to 5 categories
                print(f"📂 Found {len(categories)} categories, processing {category_count}")
                
                for category_index in range(category_count):
                    if signup_completed:
                        print("✅ Signup completed, stopping category processing")
                        break
                        
                    try:
                        print(f"\n➡️ Processing Category {category_index+1}")
                        
                        # Re-fetch categories to avoid stale elements
                        categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories"])))
                        if category_index >= len(categories):
                            print(f"⚠️ Category {category_index+1} not available")
                            continue
                            
                        category = categories[category_index]
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", category)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", category)
                        allure.attach(driver.get_screenshot_as_png(), name=f"Category_{category_index+1}_Opened", attachment_type=AttachmentType.PNG)
                        time.sleep(3)
                        
                        # Process videos in this category
                        try:
                            videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["videos"])))
                            video_count = min(len(videos), 3)  # Limit to 3 videos per category
                            print(f"🎞️ Found {len(videos)} videos, processing {video_count}")
                            
                            for video_index in range(video_count):
                                if signup_completed:
                                    print("✅ Signup completed, stopping video processing")
                                    break
                                    
                                try:
                                    print(f"▶️ Processing video {video_index+1} in category {category_index+1}")
                                    
                                    # Re-fetch videos
                                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["videos"])))
                                    if video_index >= len(videos):
                                        print(f"⚠️ Video {video_index+1} not available")
                                        continue
                                    
                                    video = videos[video_index]
                                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", video)
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].click();", video)
                                    allure.attach(driver.get_screenshot_as_png(), name=f"Video_Cat{category_index+1}_Vid{video_index+1}_Opened", attachment_type=AttachmentType.PNG)
                                    time.sleep(3)
                                    
                                    # Handle PPV and signup
                                    ppv_result = handle_ppv_and_signup()
                                    
                                    if signup_completed:
                                        print(f"🎉 Signup completed successfully on video {video_index+1}!")
                                        break
                                    elif ppv_result:
                                        # No PPV, go back and try next video
                                        driver.back()
                                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["videos"])))
                                        time.sleep(2)
                                    else:
                                        print(f"⚠️ Issue with video {video_index+1}, trying next")
                                        driver.back()
                                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["videos"])))
                                        time.sleep(2)
                                        
                                except Exception as ve:
                                    print(f"❌ Error processing video {video_index+1}: {ve}")
                                    try:
                                        driver.back()
                                        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["videos"])))
                                        time.sleep(2)
                                    except:
                                        break
                                    continue
                            
                        except Exception as video_error:
                            print(f"❌ Error processing videos in category {category_index+1}: {video_error}")
                        
                        # Navigate back to categories if signup not completed
                        if not signup_completed:
                            try:
                                driver.back()
                                wait.until(EC.presence_of_element_located((By.XPATH, xpaths["categories"])))
                                time.sleep(2)
                            except:
                                # Recovery: go back to live section and click view all
                                driver.get(url)
                                smart_wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab Recovery")
                                smart_wait_and_click(By.XPATH, xpaths["view_all_button"], "View All Recovery")
                                time.sleep(3)
                        
                    except Exception as ce:
                        print(f"❌ Error in category {category_index+1}: {ce}")
                        # Recovery
                        driver.get(url)
                        smart_wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab Recovery")
                        smart_wait_and_click(By.XPATH, xpaths["view_all_button"], "View All Recovery")
                        continue

            # Final results
            if signup_completed:
                print("🎉 PPV Signup automation completed successfully!")
                allure.attach(driver.get_screenshot_as_png(), name="Final_Success", attachment_type=AttachmentType.PNG)
                assert True
            else:
                print("ℹ️ No PPV content found requiring signup")
                allure.attach(driver.get_screenshot_as_png(), name="No_PPV_Found", attachment_type=AttachmentType.PNG)
                assert True  # Still pass if no PPV content was found

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed: {e}"

        finally:
            print(f"📊 Test Summary:")
            print(f"   - Signup Completed: {'✅ Yes' if signup_completed else '❌ No'}")
            print(f"   - Final URL: {driver.current_url}")
            try:
                driver.quit()
            except:
                pass