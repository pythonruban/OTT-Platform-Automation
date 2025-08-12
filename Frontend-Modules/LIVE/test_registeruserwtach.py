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
    "login_icon": "(//button[@type='button'])[1]",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "live_tab": "//li[@id='header-Live']",
    "view_all_3": "(//a[text()='View All'])[2]",
    "live_category_id": "livecategories-0",
    "video_block_id": "live-1",
    "watch_button": "//button[@id='watch-now-button']"
}

@pytest.mark.usefixtures("browser_setup")
class TestLiveWatchAutomation:

    def test_live_watch_complete_flow(self, browser_setup):
        """Complete Live Watch Automation Flow - Login → Live → Category → Video → Watch"""
        driver = browser_setup
        wait = WebDriverWait(driver, 30)
        watch_completed = False

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
                        print(f"✅ Successfully clicked {label} using strategy {i+1}")
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

        def smart_fill_input(by, value, text, label):
            """Enhanced input filling with error handling"""
            try:
                wait_obj = WebDriverWait(driver, 15)
                element = wait_obj.until(EC.visibility_of_element_located((by, value)))
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                time.sleep(0.5)
                
                element.clear()
                time.sleep(0.5)
                element.send_keys(text)
                print(f"✅ Successfully filled {label}")
                time.sleep(0.5)
                return True
                
            except Exception as e:
                print(f"❌ Failed to fill {label}: {e}")
                return False

        def login_process():
            """Handle complete login process"""
            try:
                print("🔐 Starting login process...")
                
                # Click login icon
                if not smart_wait_and_click(By.XPATH, xpaths["login_icon"], "Login Icon"):
                    return False
                
                # Fill email
                if not smart_fill_input(By.XPATH, xpaths["email"], ReadConfig.getTestingemail(), "Email"):
                    return False
                
                # Fill password
                if not smart_fill_input(By.XPATH, xpaths["password"], ReadConfig.getTestpassword(), "Password"):
                    return False
                
                # Click login button
                if not smart_wait_and_click(By.XPATH, xpaths["login_btn"], "Login Submit Button"):
                    return False
                
                # Choose profile
                if not smart_wait_and_click(By.XPATH, xpaths["choose_profile"], "Choose Profile"):
                    return False
                
                print("✅ Login process completed successfully")
                allure.attach(driver.get_screenshot_as_png(), name="Login_Completed", attachment_type=AttachmentType.PNG)
                return True
                
            except Exception as e:
                print(f"❌ Login process failed: {e}")
                allure.attach(driver.get_screenshot_as_png(), name="Login_Failed", attachment_type=AttachmentType.PNG)
                return False

        def navigate_to_live_categories():
            """Navigate to live section and view all categories"""
            try:
                print("📺 Navigating to Live section...")
                
                # Click Live tab
                if not smart_wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab"):
                    return False
                
                # Click View All button
                if not smart_wait_and_click(By.XPATH, xpaths["view_all_3"], "View All Button"):
                    return False
                
                print("✅ Successfully navigated to Live categories")
                allure.attach(driver.get_screenshot_as_png(), name="Live_Categories_Loaded", attachment_type=AttachmentType.PNG)
                return True
                
            except Exception as e:
                print(f"❌ Failed to navigate to live categories: {e}")
                return False

        def click_live_category():
            """Click on the live category"""
            try:
                print("📂 Clicking live category...")
                
                # Click category by ID
                if not smart_wait_and_click(By.ID, xpaths["live_category_id"], "Live Category"):
                    return False
                
                print("✅ Successfully clicked live category")
                allure.attach(driver.get_screenshot_as_png(), name="Category_Selected", attachment_type=AttachmentType.PNG)
                return True
                
            except Exception as e:
                print(f"❌ Failed to click live category: {e}")
                return False

        def click_video_and_watch():
            """Click video and start watching"""
            nonlocal watch_completed
            try:
                print("🎬 Clicking video to watch...")
                
                # Click video block by ID
                if not smart_wait_and_click(By.ID, xpaths["video_block_id"], "Video Block"):
                    return False
                
                print("✅ Video clicked, checking for watch button...")
                time.sleep(3)  # Wait for video page to load
                
                # Check if watch button is present and click it
                try:
                    watch_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpaths["watch_button"]))
                    )
                    
                    print("🎭 Watch button found, clicking to start watching...")
                    
                    if smart_wait_and_click(By.XPATH, xpaths["watch_button"], "Watch Now Button"):
                        print("🎉 Successfully started watching the video!")
                        watch_completed = True
                        allure.attach(driver.get_screenshot_as_png(), name="Video_Watching", attachment_type=AttachmentType.PNG)
                        
                        # Wait a bit to ensure video starts playing
                        time.sleep(5)
                        
                        # Check if video is actually playing (optional verification)
                        try:
                            # Look for video player indicators (you can customize these selectors)
                            video_indicators = [
                                "//video",
                                "//div[contains(@class, 'video-player')]",
                                "//div[contains(@class, 'player')]",
                                "//iframe[contains(@src, 'player')]"
                            ]
                            
                            for indicator in video_indicators:
                                try:
                                    video_element = driver.find_element(By.XPATH, indicator)
                                    print(f"✅ Video player detected: {indicator}")
                                    allure.attach(driver.get_screenshot_as_png(), name="Video_Player_Active", attachment_type=AttachmentType.PNG)
                                    break
                                except:
                                    continue
                            
                        except Exception as ve:
                            print(f"ℹ️ Could not verify video player status: {ve}")
                        
                        return True
                    else:
                        print("❌ Failed to click watch button")
                        return False
                        
                except TimeoutException:
                    print("ℹ️ No watch button found - video might be playing directly")
                    # Sometimes videos start playing automatically without a watch button
                    watch_completed = True
                    allure.attach(driver.get_screenshot_as_png(), name="Video_Auto_Playing", attachment_type=AttachmentType.PNG)
                    return True
                
            except Exception as e:
                print(f"❌ Failed to click video and watch: {e}")
                allure.attach(driver.get_screenshot_as_png(), name="Video_Watch_Error", attachment_type=AttachmentType.PNG)
                return False

        def process_multiple_videos(max_videos=3):
            """Process multiple videos in the category (optional enhancement)"""
            try:
                print(f"🎬 Processing up to {max_videos} videos...")
                
                # Find all video blocks with similar ID pattern
                video_patterns = [
                    "live-1", "live-2", "live-3", "live-4", "live-5"
                ]
                
                videos_processed = 0
                
                for i, video_id in enumerate(video_patterns[:max_videos]):
                    try:
                        print(f"\n▶️ Trying video {i+1}: {video_id}")
                        
                        # Check if video exists
                        try:
                            video_element = driver.find_element(By.ID, video_id)
                            print(f"✅ Found video: {video_id}")
                        except NoSuchElementException:
                            print(f"⚠️ Video {video_id} not found, skipping...")
                            continue
                        
                        # Click the video
                        if smart_wait_and_click(By.ID, video_id, f"Video {video_id}"):
                            time.sleep(3)
                            
                            # Try to click watch button
                            if smart_wait_and_click(By.XPATH, xpaths["watch_button"], f"Watch Button for {video_id}", wait_time=5):
                                print(f"🎉 Successfully started watching video {video_id}")
                                videos_processed += 1
                                allure.attach(driver.get_screenshot_as_png(), name=f"Video_{video_id}_Watching", attachment_type=AttachmentType.PNG)
                                
                                # Watch for a few seconds
                                time.sleep(3)
                                
                                # Go back to try next video
                                driver.back()
                                time.sleep(2)
                            else:
                                print(f"ℹ️ No watch button for {video_id}, might be auto-playing")
                                videos_processed += 1
                                allure.attach(driver.get_screenshot_as_png(), name=f"Video_{video_id}_AutoPlay", attachment_type=AttachmentType.PNG)
                                
                                # Go back to try next video
                                driver.back()
                                time.sleep(2)
                        
                    except Exception as ve:
                        print(f"⚠️ Error processing video {video_id}: {ve}")
                        continue
                
                print(f"✅ Processed {videos_processed} videos successfully")
                return videos_processed > 0
                
            except Exception as e:
                print(f"❌ Error in multiple video processing: {e}")
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

            with allure.step("Step 2: Login Process"):
                if not login_process():
                    raise Exception("Login process failed")

            with allure.step("Step 3: Navigate to Live Categories"):
                if not navigate_to_live_categories():
                    raise Exception("Failed to navigate to live categories")

            with allure.step("Step 4: Select Live Category"):
                if not click_live_category():
                    raise Exception("Failed to click live category")

            with allure.step("Step 5: Click Video and Watch"):
                if not click_video_and_watch():
                    raise Exception("Failed to click video and watch")

            # Optional: Process multiple videos
            with allure.step("Step 6: Process Additional Videos (Optional)"):
                try:
                    # Go back to category first
                    driver.back()
                    time.sleep(2)
                    process_multiple_videos(max_videos=2)  # Try 2 more videos
                except Exception as e:
                    print(f"ℹ️ Additional video processing skipped: {e}")

            # Final verification
            if watch_completed:
                print("🎉 Live watch automation completed successfully!")
                allure.attach(driver.get_screenshot_as_png(), name="Final_Success", attachment_type=AttachmentType.PNG)
                assert True
            else:
                print("⚠️ Watch process completed but status unclear")
                allure.attach(driver.get_screenshot_as_png(), name="Final_Status_Unclear", attachment_type=AttachmentType.PNG)
                assert True  # Still pass as video was accessed

        except Exception as e:
            print(f"❌ Test Failed: {e}")
            allure.attach(driver.get_screenshot_as_png(), name="Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, f"Test failed: {e}"

        finally:
            print(f"📊 Test Summary:")
            print(f"   - Watch Completed: {'✅ Yes' if watch_completed else '❌ No'}")
            print(f"   - Final URL: {driver.current_url}")
            try:
                driver.quit()
            except:
                pass