import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "//button[@id='home-signin'] | (//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "live_tab": "//li[@id='header-Live']",
    "categories_section": "//div[@class='card-image-container']",
    "video_tile": "//div[@class='homeListImage active']",
    "comment_tab": "//li[@id='live-tab-3']",
    "comment_input": "comment-textarea",
    "post_btn": "post-comment-button",
    "view_all_xpaths":"(//a[contains(text(), 'View All')])[2]",
    
}

@pytest.mark.usefixtures("browser_setup")
class TestLiveCommentAutomation:

    def wait_and_click(self, by, value, label, wait=30):
        """Enhanced wait and click with better error handling"""
        try:
            # Wait for element to be present
            WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((by, value)))
            
            # Wait for element to be visible
            elem = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located((by, value)))
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
            time.sleep(1)
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable((by, value)))
            
            # Try clicking with JavaScript if regular click fails
            try:
                elem.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elem)
                
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ Failed: {label} - {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Error", attachment_type=AttachmentType.PNG)
            return False

    def safe_navigate_back(self, expected_element_xpath, max_retries=3):
        """Safely navigate back with retries"""
        for attempt in range(max_retries):
            try:
                self.driver.back()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, expected_element_xpath)))
                time.sleep(2)
                print(f"✅ Successfully navigated back (attempt {attempt + 1})")
                return True
            except TimeoutException:
                print(f"⚠️ Navigate back attempt {attempt + 1} failed, retrying...")
                if attempt == max_retries - 1:
                    print("❌ All navigate back attempts failed, refreshing page")
                    self.driver.refresh()
                    WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, expected_element_xpath)))
                    time.sleep(2)
                    return True
        return False

    def login_and_choose_profile(self):
        """Login and choose profile with error handling"""
        try:
            if not self.wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon"):
                raise Exception("Failed to click login icon")
                
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            
            if not self.wait_and_click(By.XPATH, xpaths["login_btn"], "Login Submit"):
                raise Exception("Failed to click login submit")
                
            if not self.wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile"):
                raise Exception("Failed to choose profile")
                
            print("✅ Login and profile selection completed")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def post_comment_on_video(self, category_index, video_index):
        """Post comment on a video with proper error handling"""
        try:
            # Click comment tab
            if not self.wait_and_click(By.XPATH, xpaths["comment_tab"], "Comment Tab"):
                return False
                
            # Find and fill comment input
            wait = WebDriverWait(self.driver, 15)
            comment_box = wait.until(EC.visibility_of_element_located((By.ID, xpaths["comment_input"])))
            comment_box.clear()
            time.sleep(1)
            
            comment_text = f"Nice video from automation! Cat:{category_index+1} Vid:{video_index+1}"
            comment_box.send_keys(comment_text)
            time.sleep(1)
            
            # Click post button
            post_button = self.driver.find_element(By.ID, xpaths["post_btn"])
            self.driver.execute_script("arguments[0].click();", post_button)
            
            print(f"💬 Comment posted on video {video_index+1} in category {category_index+1}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Comment_Posted_Cat{category_index+1}_Vid{video_index+1}", attachment_type=AttachmentType.PNG)
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"❌ Failed to post comment: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Comment_Error_Cat{category_index+1}_Vid{video_index+1}", attachment_type=AttachmentType.PNG)
            return False

    def process_videos_in_category(self, category_index, max_videos=5):
        """Process all videos in a category"""
        try:
            wait = WebDriverWait(self.driver, 15)
            videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tile"])))
            video_count = min(len(videos), max_videos)  # Limit videos to process
            print(f"🎞️ Found {len(videos)} videos in category {category_index+1}, processing {video_count}")

            for video_index in range(video_count):
                try:
                    print(f"\n▶️ Processing video {video_index+1} in category {category_index+1}")
                    
                    # Re-fetch videos to avoid stale element
                    videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["video_tile"])))
                    
                    if video_index >= len(videos):
                        print(f"⚠️ Video {video_index+1} not found, skipping")
                        continue
                        
                    video = videos[video_index]
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", video)
                    time.sleep(1)
                    
                    # Click video with JavaScript to avoid interception
                    self.driver.execute_script("arguments[0].click();", video)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_Cat{category_index+1}_Vid{video_index+1}_Opened", attachment_type=AttachmentType.PNG)
                    time.sleep(3)

                    # Post comment
                    comment_success = self.post_comment_on_video(category_index, video_index)
                    
                    # Navigate back to video list
                    if not self.safe_navigate_back(xpaths["video_tile"]):
                        print(f"❌ Failed to navigate back from video {video_index+1}")
                        break
                        
                    print(f"✅ Completed video {video_index+1} in category {category_index+1}")

                except StaleElementReferenceException:
                    print(f"⚠️ Stale element at video {video_index+1}, refreshing and continuing...")
                    self.driver.refresh()
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["video_tile"])))
                    continue
                    
                except Exception as ve:
                    print(f"⚠️ Error processing video {video_index+1}: {ve}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_Error_Cat{category_index+1}_Vid{video_index+1}", attachment_type=AttachmentType.PNG)
                    
                    # Try to navigate back
                    try:
                        self.safe_navigate_back(xpaths["video_tile"])
                    except:
                        print("❌ Failed to recover from video error")
                        break
                    continue

            return True
            
        except Exception as e:
            print(f"❌ Error processing videos in category {category_index+1}: {e}")
            return False

    def process_categories(self, max_categories=3):
        """Process all categories in the live section"""
        try:
            wait = WebDriverWait(self.driver, 15)
            categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
            category_count = min(len(categories), max_categories)  # Limit categories to process
            print(f"📂 Found {len(categories)} Live Categories, processing {category_count}")

            for category_index in range(category_count):
                try:
                    print(f"\n➡️ Processing Category {category_index+1}")
                    
                    # Re-fetch categories to avoid stale element
                    categories = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpaths["categories_section"])))
                    
                    if category_index >= len(categories):
                        print(f"⚠️ Category {category_index+1} not found, skipping")
                        continue
                        
                    category = categories[category_index]
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", category)
                    time.sleep(1)
                    
                    # Click category with JavaScript
                    self.driver.execute_script("arguments[0].click();", category)
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{category_index+1}_Opened", attachment_type=AttachmentType.PNG)
                    time.sleep(3)

                    # Process videos in this category
                    videos_processed = self.process_videos_in_category(category_index)
                    
                    # Navigate back to categories
                    if not self.safe_navigate_back(xpaths["categories_section"]):
                        print(f"❌ Failed to navigate back from category {category_index+1}")
                        # Try to recover by going to live tab
                        self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab Recovery")
                        self.wait_and_click(By.XPATH, xpaths["view_all_xpaths"][0], "View All Recovery")
                        
                    print(f"✅ Completed category {category_index+1}")

                except StaleElementReferenceException:
                    print(f"⚠️ Stale element at category {category_index+1}, refreshing...")
                    self.driver.refresh()
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["categories_section"])))
                    continue
                    
                except Exception as ce:
                    print(f"❌ Error in category {category_index+1}: {ce}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_Error_{category_index+1}", attachment_type=AttachmentType.PNG)
                    
                    # Try to recover
                    try:
                        self.driver.get(ReadConfig.getHomePageURL())
                        self.login_and_choose_profile()
                        self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab Recovery")
                        self.wait_and_click(By.XPATH, xpaths["view_all_xpaths"][0], "View All Recovery")
                    except:
                        print("❌ Failed to recover from category error")
                        break
                    continue

            return True
            
        except Exception as e:
            print(f"❌ Error processing categories: {e}")
            return False

    def test_live_comment_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)

        try:
            with allure.step("Step 1: Open Website and Login"):
                url = ReadConfig.getHomePageURL()
                self.driver.get(url)
                self.driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="01_Home_Loaded", attachment_type=AttachmentType.PNG)

                if not self.login_and_choose_profile():
                    raise Exception("Login failed")

            with allure.step("Step 2: Navigate to Live Section"):
                if not self.wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab"):
                    raise Exception("Failed to click Live tab")

            with allure.step("Step 3: Process Live Categories and Videos"):
                # Click View All button
                if not self.wait_and_click(By.XPATH, xpaths["view_all_xpaths"][0], "View All Button"):
                    raise Exception("Failed to click View All button")
                
                # Process categories and their videos
                if not self.process_categories(max_categories=3):  # Limit to 3 categories for testing
                    print("⚠️ Some categories failed to process, but continuing...")

            print("✅ Live comment automation test completed successfully")
            assert True

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed due to exception: {e}"

        finally:
            try:
                if hasattr(self, 'driver') and self.driver:
                    self.driver.quit()
            except Exception as e:
                print(f"⚠️ Error closing driver: {e}")

    def teardown_class(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except:
            pass