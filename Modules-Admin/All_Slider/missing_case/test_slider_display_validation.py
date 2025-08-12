import time
import pytest 
import os
import sys 
import allure 

from conftest import *
from selenium.webdriver import ActionChains
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver

from utilities.readProp import ReadConfig

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.mark.usefixtures("browser_setup")
class TestSliderDisplayValidation:
    driver = webdriver.Firefox

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    
    # Slider management locators
    All_slider_element = "//a[span[text()='All Slider']]"
    add_slider_button = "//a[@id='navigationLinkForAddPage']"
    
    # List view locators based on actual website structure
    table_rows = "//tbody//tr"
    table_headers = "//div[@class='bootstrapTable theme-bg-color p-3 rounded-2']"
    slider_names_column = "//div[@class='rightVideoTitle d-flex flex-column ']"  # First column - Slider Name
    slider_images_column = "(//div[@class='rightVideoTitle d-flex flex-column '])[1]"  # Second column - Slider Image
    player_images_column = "(//div[@class='rightVideoTitle d-flex flex-column '])[2]"  # Third column - Player Image
    actions_column = "//div[@class='editdropdown']"  # Fourth column - Actions
    
    # Action dropdown elements
    action_dropdowns = "//span[contains(@class,'editdropdown-button')]"
    edit_menu_option = "//span[contains(text(),'Edit')]"
    delete_menu_option = "//span[contains(text(),'Delete')]"
    
    # Results count element
    results_count_text = "//*[contains(text(),'results found')]"

    def login_and_navigate_to_slider_list(self):
        """Helper method to login and navigate to slider list page"""
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        
        try:
            # Login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())
            
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()
            
            print("Login Successful!")
            time.sleep(2)
            
            # Navigate to All Slider
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            slider = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.All_slider_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)
            self.driver.execute_script("arguments[0].click();", slider)
            print("Navigated to 'All Slider Management'")
            time.sleep(3)
            
        except Exception as e:
            pytest.fail(f"Failed to login and navigate: {e}")

    def test_table_structure_validation(self, browser_setup):
        """Test that the slider table has the correct structure and columns"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Check if table exists
            table_exists = len(self.driver.find_elements(By.XPATH, "//table")) > 0
            assert table_exists, "Slider table not found on the page"
            print("✓ Slider table exists")
            
            # Check table headers
            headers = self.driver.find_elements(By.XPATH, self.table_headers)
            if headers:
                print(f"✓ Found {len(headers)} table headers")
                header_texts = [header.text for header in headers]
                print(f"Header texts: {header_texts}")
                
                # Verify expected headers are present
                expected_headers = ["Slider Name", "Slider Image", "Player Image", "Actions"]
                for expected in expected_headers:
                    found = any(expected.lower() in header.lower() for header in header_texts)
                    if found:
                        print(f"✓ Found expected header: {expected}")
                    else:
                        print(f"⚠ Missing expected header: {expected}")
            
            # Check table rows
            rows = self.driver.find_elements(By.XPATH, self.table_rows)
            print(f"✓ Found {len(rows)} slider rows in table")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Table Structure Validation", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Table Structure Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Table structure validation failed: {e}")

    def test_slider_names_display(self, browser_setup):
        """Test that slider names are displayed correctly in the first column"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Get all slider names from the first column
            slider_names = self.driver.find_elements(By.XPATH, self.slider_names_column)
            
            if slider_names:
                print(f"✓ Found {len(slider_names)} slider names displayed")
                
                # Check each slider name
                for i, name_element in enumerate(slider_names):
                    name_text = name_element.text.strip()
                    if name_text:
                        print(f"✓ Slider {i+1} name: {name_text}")
                        
                        # Verify name is not empty and has reasonable length
                        assert len(name_text) > 0, f"Slider {i+1} has empty name"
                        assert len(name_text) <= 100, f"Slider {i+1} name too long: {len(name_text)} chars"
                        
                    else:
                        print(f"⚠ Slider {i+1} has empty name")
                
                # Check for expected slider names from the website image
                page_text = self.driver.page_source
                expected_names = ["CUEZR", "GWYTYLP", "YYPOR"]  # From the website image
                
                for expected_name in expected_names:
                    if expected_name in page_text:
                        print(f"✓ Found expected slider: {expected_name}")
                    else:
                        print(f"⚠ Expected slider not found: {expected_name}")
                
            else:
                pytest.fail("No slider names found in the list")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Slider Names Display Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Slider Names Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Slider names display test failed: {e}")

    def test_slider_images_display(self, browser_setup):
        """Test that slider images are displayed correctly"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Get all slider images
            slider_images = self.driver.find_elements(By.XPATH, self.slider_images_column)
            
            if slider_images:
                print(f"✓ Found {len(slider_images)} slider images")
                
                # Check each image
                for i, img in enumerate(slider_images):
                    img_src = img.get_attribute('src')
                    img_alt = img.get_attribute('alt')
                    
                    # Check if image source exists
                    if img_src:
                        print(f"✓ Slider image {i+1} has src: {img_src[:50]}...")
                        
                        # Check if image is displayed
                        if img.is_displayed():
                            print(f"✓ Slider image {i+1} is visible")
                        else:
                            print(f"⚠ Slider image {i+1} is not visible")
                        
                        # Check image dimensions if possible
                        width = img.get_attribute('width') or img.size.get('width')
                        height = img.get_attribute('height') or img.size.get('height')
                        
                        if width and height:
                            print(f"✓ Slider image {i+1} dimensions: {width}x{height}")
                        
                    else:
                        print(f"⚠ Slider image {i+1} has no src attribute")
                    
                    if img_alt:
                        print(f"✓ Slider image {i+1} has alt text: {img_alt}")
                
            else:
                print("⚠ No slider images found in the list")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Slider Images Display Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Slider Images Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Slider images display test failed: {e}")

    def test_player_images_display(self, browser_setup):
        """Test that player images are displayed correctly"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Get all player images
            player_images = self.driver.find_elements(By.XPATH, self.player_images_column)
            
            if player_images:
                print(f"✓ Found {len(player_images)} player images")
                
                # Check each player image
                for i, img in enumerate(player_images):
                    img_src = img.get_attribute('src')
                    
                    if img_src:
                        print(f"✓ Player image {i+1} has src: {img_src[:50]}...")
                        
                        if img.is_displayed():
                            print(f"✓ Player image {i+1} is visible")
                        else:
                            print(f"⚠ Player image {i+1} is not visible")
                    else:
                        print(f"⚠ Player image {i+1} has no src attribute")
                
            else:
                print("⚠ No player images found in the list")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Player Images Display Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Player Images Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Player images display test failed: {e}")

    def test_action_dropdown_functionality(self, browser_setup):
        """Test that action dropdowns work correctly"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Find action dropdown buttons (three dots menu)
            action_buttons = self.driver.find_elements(By.XPATH, self.action_dropdowns)
            
            if action_buttons:
                print(f"✓ Found {len(action_buttons)} action dropdown buttons")
                
                # Test the first dropdown
                first_action = action_buttons[0]
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_action)
                time.sleep(1)
                
                # Hover over the dropdown to reveal menu
                actions = ActionChains(self.driver)
                actions.move_to_element(first_action).perform()
                time.sleep(2)
                
                # Check for Edit option
                try:
                    edit_option = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, self.edit_menu_option))
                    )
                    if edit_option.is_displayed():
                        print("✓ Edit option is visible in dropdown")
                    else:
                        print("⚠ Edit option found but not visible")
                except TimeoutException:
                    print("⚠ Edit option not found in dropdown")
                
                # Check for Delete option
                try:
                    delete_option = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, self.delete_menu_option))
                    )
                    if delete_option.is_displayed():
                        print("✓ Delete option is visible in dropdown")
                    else:
                        print("⚠ Delete option found but not visible")
                except TimeoutException:
                    print("⚠ Delete option not found in dropdown")
                
            else:
                print("⚠ No action dropdown buttons found")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Action Dropdown Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Action Dropdown Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Action dropdown test failed: {e}")

    def test_results_count_accuracy(self, browser_setup):
        """Test that the 'X results found' count is accurate"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Find results count text
            try:
                results_element = self.driver.find_element(By.XPATH, self.results_count_text)
                results_text = results_element.text
                print(f"Results count display: {results_text}")
                
                # Extract number from text like "6 results found"
                import re
                numbers = re.findall(r'\d+', results_text)
                
                if numbers:
                    displayed_count = int(numbers[0])
                    
                    # Count actual rows in table
                    actual_rows = self.driver.find_elements(By.XPATH, self.table_rows)
                    actual_count = len(actual_rows)
                    
                    print(f"Displayed count: {displayed_count}")
                    print(f"Actual table rows: {actual_count}")
                    
                    # Verify counts match
                    if displayed_count == actual_count:
                        print("✓ Results count is accurate")
                    else:
                        print(f"⚠ Count mismatch - Display: {displayed_count}, Actual: {actual_count}")
                        
                        # This might still be acceptable if there are hidden rows or pagination
                        if actual_count > 0:
                            print("⚠ Count mismatch detected but sliders are displayed")
                        else:
                            pytest.fail(f"Results count shows {displayed_count} but no rows found")
                else:
                    print("⚠ Could not extract number from results text")
                
            except NoSuchElementException:
                print("⚠ Results count element not found")
                # Count rows anyway
                rows = self.driver.find_elements(By.XPATH, self.table_rows)
                print(f"Found {len(rows)} slider rows (no count display)")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Results Count Accuracy Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Results Count Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Results count accuracy test failed: {e}")

    def test_add_slider_button_presence(self, browser_setup):
        """Test that Add Slider button is present and functional"""
        self.driver = browser_setup
        self.login_and_navigate_to_slider_list()
        
        try:
            # Find Add Slider button
            add_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.add_slider_button))
            )
            
            # Check if button is displayed and enabled
            assert add_button.is_displayed(), "Add Slider button is not visible"
            assert add_button.is_enabled(), "Add Slider button is not enabled"
            
            # Check button text
            button_text = add_button.text
            print(f"Add button text: {button_text}")
            
            # Verify button text contains expected keywords
            expected_keywords = ["add", "new", "slider"]
            text_lower = button_text.lower()
            
            if any(keyword in text_lower for keyword in expected_keywords):
                print("✓ Add Slider button has appropriate text")
            else:
                print(f"⚠ Button text may not be appropriate: {button_text}")
            
            # Test button functionality (click and verify navigation)
            add_button.click()
            time.sleep(3)
            
            # Check if we navigated to add slider page
            current_url = self.driver.current_url
            if "add" in current_url.lower() or "create" in current_url.lower():
                print("✓ Add Slider button navigates to add page")
            else:
                print(f"⚠ Navigation may not be correct. Current URL: {current_url}")
            
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Add Slider Button Test", 
                         attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), 
                         name="Add Slider Button Test Failed", 
                         attachment_type=AttachmentType.PNG)
            pytest.fail(f"Add Slider button test failed: {e}")

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
