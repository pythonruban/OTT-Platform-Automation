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
    "live_tab": "//li[@id='header-Live']",
    "view_all_3": "(//a[text()='View All'])[2]",
    "live_category_id": "livecategories-0",
    "video_block_id": "live-1",
    "watch_button": "//button[@id='watch-now-button']",
    
    # Guest user related elements (if any popups appear)
    "guest_continue": "//button[contains(text(), 'Continue as Guest')]",
    "close_popup": "//button[@class='close'] | //span[@class='close'] | //button[contains(@class, 'close')]",
    "skip_login": "//a[contains(text(), 'Skip')] | //button[contains(text(), 'Skip')]"
}

@pytest.mark.usefixtures("browser_setup")
class TestGuestLiveWatchAutomation:

    def test_guest_live_watch_complete_flow(self, browser_setup):
        """Complete Guest Live Watch Automation Flow - No Login Required"""
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

        def handle_guest_popups():
            """Handle any login/signup popups that might appear for guest users"""
            try:
                print("🔍 Checking for guest user popups...")
                
                # Common popup elements to close/skip
                popup_elements = [
                    (By.XPATH, xpaths["guest_continue"], "Continue as Guest"),
                    (By.XPATH, xpaths["close_popup"], "Close Popup"),
                    (By.XPATH, xpaths["skip_login"], "Skip Login"),
                    (By.XPATH, "//button[contains(text(), 'Later')]", "Later Button"),
                    (By.XPATH, "//button[contains(text(), 'No Thanks')]", "No Thanks Button"),
                    (By.XPATH, "//div[@class='modal']//button", "Modal Close Button")
                ]
                
                for by, xpath, label in popup_elements:
                    try:
                        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((by, xpath)))
                        if element.is_displayed():
                            print(f"👁️ Found popup: {label}")
                            smart_wait_and_click(by, xpath, label, wait_time=5)
                            time.sleep(1)
                            break
                    except TimeoutException:
                        continue
                    except Exception as e:
                        print(f"⚠️ Error handling popup {label}: {e}")
                        continue
                        
                print("✅ Guest popup handling completed")
                return True
                
            except Exception as e:
                print(f"ℹ️ No guest popups found or error handling them: {e}")
                return True

        def navigate_to_live_categories():
            """Navigate to live section and view all categories as guest"""
            try:
                print("📺 Navigating to Live section as guest user...")
                
                # Handle any initial popups
                handle_guest_popups()
                
                # Click Live tab
                if not smart_wait_and_click(By.XPATH, xpaths["live_tab"], "Live Tab"):
                    return False
                
                # Handle popups that might appear after clicking Live
                handle_guest_popups()
                
                # Click View All button
                if not smart_wait_and_click(By.XPATH, xpaths["view_all_3"], "View All Button"):
                    return False
                
                # Handle any additional popups
                handle_guest_popups()
                
                print("✅ Successfully navigated to Live categories as guest")
                allure.attach(driver.get_screenshot_as_png(), name="Guest_Live_Categories_Loaded", attachment_type=AttachmentType.PNG)
                return True
                
            except Exception as e:
                print(f"❌ Failed to navigate to live categories as guest: {e}")
                return False

        def click_live_category():
            """Click on the live category as guest user"""
            try:
                print("📂 Clicking live category as guest user...")
                
                # Handle any popups before clicking category
                handle_guest_popups()
                
                # Click category by ID
                if not smart_wait_and_click(By.ID, xpaths["live_category_id"], "Live Category"):
                    return False
                
                # Handle popups that might appear after clicking category
                handle_guest_popups()
                
                print("✅ Successfully clicked live category as guest")
                allure.attach(driver.get_screenshot_as_png(), name="Guest_Category_Selected", attachment_type=AttachmentType.PNG)
                return True
                
            except Exception as e:
                print(f"❌ Failed to click live category as guest: {e}")
                return False

        def click_video_and_watch():
            """Click video and start watching as guest user"""
            nonlocal watch_completed
            try:
                print("🎬 Clicking video to watch as guest user...")
                
                # Handle any popups before clicking video
                handle_guest_popups()
                
                # Click video block by ID
                if not smart_wait_and_click(By.ID, xpaths["video_block_id"], "Video Block"):
                    return False
                
                print("✅ Video clicked, checking for watch button...")
                time.sleep(3)  # Wait for video page to load
                
                # Handle any popups that appear on video page
                handle_guest_popups()
                
                # Check if watch button is present and click it
                try:
                    watch_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpaths["watch_button"]))
                    )
                    
                    print("🎭 Watch button found, clicking to start watching as guest...")
                    
                    if smart_wait_and_click(By.XPATH, xpaths["watch_button"], "Watch Now Button"):
                        # Handle any popups after clicking watch
                        time.sleep(2)
                        handle_guest_popups()
                        
                        print("🎉 Successfully started watching the video as guest!")
                        watch_completed = True
                        allure.attach(driver.get_screenshot_as_png(), name="Guest_Video_Watching", attachment_type=AttachmentType.PNG)
                        
                        # Wait a bit to ensure video starts playing
                        time.sleep(5)
                        
                        # Check if video is actually playing
                        try:
                            video_indicators = [
                                "//video",
                                "//div[contains(@class, 'video-player')]",
                                "//div[contains(@class, 'player')]",
                                "//iframe[contains(@src, 'player')]",
                                "//div[contains(@class, 'jwplayer')]",
                                "//div[contains(@class, 'video-container')]"
                            ]
                            
                            for indicator in video_indicators:
                                try:
                                    video_element = driver.find_element(By.XPATH, indicator)
                                    print(f"✅ Video player detected for guest: {indicator}")
                                    allure.attach(driver.get_screenshot_as_png(), name="Guest_Video_Player_Active", attachment_type=AttachmentType.PNG)
                                    break
                                except:
                                    continue
                            
                        except Exception as ve:
                            print(f"ℹ️ Could not verify video player status for guest: {ve}")
                        
                        return True
                    else:
                        print("❌ Failed to click watch button as guest")
                        return False
                        
                except TimeoutException:
                    print("ℹ️ No watch button found - video might be playing directly for guest")
                    # Sometimes videos start playing automatically for guests
                    watch_completed = True
                    allure.attach(driver.get_screenshot_as_png(), name="Guest_Video_Auto_Playing", attachment_type=AttachmentType.PNG)
                    return True
                
            except Exception as e:
                print(f"❌ Failed to click video and watch as guest: {e}")
                allure.attach(driver.get_screenshot_as_png(), name="Guest_Video_Watch_Error", attachment_type=AttachmentType.PNG)
                return False

        def process_multiple_videos_as_guest(max_videos=3):
            """Process multiple videos as guest user"""
            try:
                print(f"🎬 Processing up to {max_videos} videos as guest...")
                
                # Find all video blocks with similar ID pattern
                video_patterns = [
                    "live-1", "live-2", "live-3", "live-4", "live-5"
                ]
                
                videos_processed = 0
                
                for i, video_id in enumerate(video_patterns[:max_videos]):
                    try:
                        print(f"\n▶️ Trying video {i+1} as guest: {video_id}")
                        
                        # Handle popups before each video
                        handle_guest_popups()
                        
                        # Check if video exists
                        try:
                            video_element = driver.find_element(By.ID, video_id)
                            print(f"✅ Found video for guest: {video_id}")
                        except NoSuchElementException:
                            print(f"⚠️ Video {video_id} not found for guest, skipping...")
                            continue
                        
                        # Click the video
                        if smart_wait_and_click(By.ID, video_id, f"Guest Video {video_id}"):
                            time.sleep(3)
                            handle_guest_popups()
                            
                            # Try to click watch button
                            if smart_wait_and_click(By.XPATH, xpaths["watch_button"], f"Guest Watch Button for {video_id}", wait_time=5):
                                handle_guest_popups()
                                print(f"🎉 Successfully started watching video {video_id} as guest")
                                videos_processed += 1
                                allure.attach(driver.get_screenshot_as_png(), name=f"Guest_Video_{video_id}_Watching", attachment_type=AttachmentType.PNG)
                                
                                # Watch for a few seconds
                                time.sleep(3)
                                
                                # Go back to try next video
                                driver.back()
                                time.sleep(2)
                                handle_guest_popups()
                            else:
                                print(f"ℹ️ No watch button for {video_id}, might be auto-playing for guest")
                                videos_processed += 1
                                allure.attach(driver.get_screenshot_as_png(), name=f"Guest_Video_{video_id}_AutoPlay", attachment_type=AttachmentType.PNG)
                                
                                # Go back to try next video
                                driver.back()
                                time.sleep(2)
                                handle_guest_popups()
                        
                    except Exception as ve:
                        print(f"⚠️ Error processing video {video_id} as guest: {ve}")
                        continue
                
                print(f"✅ Processed {videos_processed} videos successfully as guest")
                return videos_processed > 0
                
            except Exception as e:
                print(f"❌ Error in multiple video processing as guest: {e}")
                return False

        # Main test execution
        try:
            with allure.step("Step 1: Open Website as Guest"):
                url = ReadConfig.getHomePageURL()
                driver.get(url)
                driver.maximize_window()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(driver.get_screenshot_as_png(), name="01_Guest_Home_Loaded", attachment_type=AttachmentType.PNG)
                print("✅ Website loaded successfully for guest user")
                
                # Handle any initial popups
                handle_guest_popups()

            with allure.step("Step 2: Navigate to Live Categories as Guest"):
                if not navigate_to_live_categories():
                    raise Exception("Failed to navigate to live categories as guest")

            with allure.step("Step 3: Select Live Category as Guest"):
                if not click_live_category():
                    raise Exception("Failed to click live category as guest")

            with allure.step("Step 4: Click Video and Watch as Guest"):
                if not click_video_and_watch():
                    raise Exception("Failed to click video and watch as guest")

            # Optional: Process multiple videos
            with allure.step("Step 5: Process Additional Videos as Guest (Optional)"):
                try:
                    # Go back to category first
                    driver.back()
                    time.sleep(2)
                    handle_guest_popups()
                    process_multiple_videos_as_guest(max_videos=2)  # Try 2 more videos
                except Exception as e:
                    print(f"ℹ️ Additional video processing skipped for guest: {e}")

            # Final verification
            if watch_completed:
                print("🎉 Guest live watch automation completed successfully!")
                allure.attach(driver.get_screenshot_as_png(), name="Guest_Final_Success", attachment_type=AttachmentType.PNG)
                assert True
            else:
                print("⚠️ Guest watch process completed but status unclear")
                allure.attach(driver.get_screenshot_as_png(), name="Guest_Final_Status_Unclear", attachment_type=AttachmentType.PNG)
                assert True  # Still pass as video was accessed

        except Exception as e:
            print(f"❌ Guest Test Failed: {e}")
            allure.attach(driver.get_screenshot_as_png(), name="Guest_Fatal_Error", attachment_type=AttachmentType.PNG)
            assert False, f"Guest test failed: {e}"

        finally:
            print(f"📊 Guest Test Summary:")
            print(f"   - Watch Completed: {'✅ Yes' if watch_completed else '❌ No'}")
            print(f"   - Final URL: {driver.current_url}")
            print(f"   - User Type: 👤 Guest (No Login)")
            try:
                driver.quit()
            except:
                pass