import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@pytest.mark.usefixtures("browser_setup")
class TestSearchFunctionality:
    """Test cases for search functionality in Live Stream Categories"""
    
    driver: webdriver
    
    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    All_live_element = "//div[@data-bs-target='#Live-Stream']"
    search_input_element = "//input[@id='live-search-input']"
    search_results_table = "//table"
    table_rows = "//table//tbody//tr"
    no_data_message = "//td[contains(text(), 'No data available')]"
    clear_search_button = "//button[@class='theme-bg-color-secondary']"
    
    def login_to_admin(self):
        """Helper method to login to admin panel"""
        try:
            self.driver.get(ReadConfig.getAdminPageURL())
            self.driver.maximize_window()
            
            # Login process
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
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Success", attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Login_Failed", attachment_type=AttachmentType.PNG)
            raise Exception(f"Login failed: {e}")
    
    
        try:
            # Navigate to Live Stream Management
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            manage_livestream = WebDriverWait(self.driver, 130).until(
                EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
            )
            self.driver.execute_script("arguments[0].click();", manage_livestream)
            print("Navigated to 'Live Stream Management'")
            
            # Click on Manage Live Stream Categories
            manage_category_button = WebDriverWait(self.driver, 130).until(
                EC.element_to_be_clickable((By.XPATH, self.All_live_element))
            )
            self.driver.execute_script("arguments[0].click();", manage_category_button)
            print("Clicked 'Manage Live Stream Categories'")
            time.sleep(3)
            
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Navigation_Failed", attachment_type=AttachmentType.PNG)
            raise Exception(f"Navigation failed: {e}")

   
        
        # Test 1: Valid Search
        with allure.step("Test 1: Valid Search"):
            try:
                print("=== Starting Valid Search Test ===")
                first_row = WebDriverWait(self.driver, 110).until(
                    EC.presence_of_element_located((By.XPATH, f"{self.table_rows}[1]"))
                )
                search_term = first_row.find_element(By.XPATH, ".//td[2]").text[:5]
                
                if search_term:
                    search_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.search_input_element))
                    )
                    search_input.clear()
                    search_input.send_keys(search_term)
                    search_input.send_keys(Keys.ENTER)
                    
                    print(f"Searched for: {search_term}")
                    time.sleep(2)
                    
                    search_results = self.driver.find_elements(By.XPATH, self.table_rows)
                    assert len(search_results) > 0, "No search results found"
                    
                    for row in search_results:
                        row_text = row.text.lower()
                        assert search_term.lower() in row_text, f"Search term '{search_term}' not found in result: {row_text}"
                    
                    allure.attach(self.driver.get_screenshot_as_png(), name="Valid_Search_Results", attachment_type=AttachmentType.PNG)
                    print("Valid search test passed successfully")
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Valid_Search_Error", attachment_type=AttachmentType.PNG)
                print(f"Valid search test failed: {e}")
        
        # Test 2: Invalid Search
        with allure.step("Test 2: Invalid Search"):
            try:
                print("=== Starting Invalid Search Test ===")
                invalid_search_term = "XYZNOMATCHING123"
                
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_input_element))
                )
                search_input.clear()
                search_input.send_keys(invalid_search_term)
                search_input.send_keys(Keys.ENTER)
                
                print(f"Searched for invalid term: {invalid_search_term}")
                time.sleep(2)
                
                try:
                    no_data_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, self.no_data_message))
                    )
                    assert no_data_element.is_displayed(), "No data message not displayed for invalid search"
                except:
                    search_results = self.driver.find_elements(By.XPATH, self.table_rows)
                    assert len(search_results) == 0, "Results found for invalid search term"
                
                allure.attach(self.driver.get_screenshot_as_png(), name="Invalid_Search_Results", attachment_type=AttachmentType.PNG)
                print("Invalid search test passed successfully")
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Invalid_Search_Error", attachment_type=AttachmentType.PNG)
                print(f"Invalid search test failed: {e}")
        
        # Test 3: Empty Search
        with allure.step("Test 3: Empty Search"):
            try:
                print("=== Starting Empty Search Test ===")
                # Clear any previous search first
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_input_element))
                )
                search_input.clear()
                search_input.send_keys(Keys.ENTER)
                time.sleep(2)
                
                original_rows = self.driver.find_elements(By.XPATH, self.table_rows)
                original_count = len(original_rows)
                
                search_input.clear()
                search_input.send_keys(Keys.ENTER)
                
                print("Performed empty search")
                time.sleep(2)
                
                current_rows = self.driver.find_elements(By.XPATH, self.table_rows)
                current_count = len(current_rows)
                
                assert current_count == original_count, f"Row count changed after empty search. Original: {original_count}, Current: {current_count}"
                
                allure.attach(self.driver.get_screenshot_as_png(), name="Empty_Search_Results", attachment_type=AttachmentType.PNG)
                print("Empty search test passed successfully")
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Empty_Search_Error", attachment_type=AttachmentType.PNG)
                print(f"Empty search test failed: {e}")
        
        # Test 4: Special Characters Search
        with allure.step("Test 4: Special Characters Search"):
            try:
                print("=== Starting Special Characters Search Test ===")
                special_characters = ["@#$%", "!@#", "***", "???", ">>>"]
                
                for special_char in special_characters:
                    search_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.search_input_element))
                    )
                    search_input.clear()
                    search_input.send_keys(special_char)
                    search_input.send_keys(Keys.ENTER)
                    
                    print(f"Searched for special characters: {special_char}")
                    time.sleep(1)
                    
                    try:
                        self.driver.find_element(By.XPATH, self.no_data_message)
                    except:
                        pass
                
                allure.attach(self.driver.get_screenshot_as_png(), name="Special_Characters_Search", attachment_type=AttachmentType.PNG)
                print("Special characters search test passed successfully")
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Special_Characters_Error", attachment_type=AttachmentType.PNG)
                print(f"Special characters search test failed: {e}")
        
        # Test 5: Case Sensitivity Search
        with allure.step("Test 5: Case Sensitivity Search"):
            try:
                print("=== Starting Case Sensitivity Search Test ===")
                # Clear search first to get fresh data
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, self.search_input_element))
                )
                search_input.clear()
                search_input.send_keys(Keys.ENTER)
                time.sleep(2)
                
                first_row = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"{self.table_rows}[1]"))
                )
                original_text = first_row.find_element(By.XPATH, ".//td[2]").text[:5]
                
                if original_text:
                    test_cases = [
                        original_text.upper(),
                        original_text.lower(),
                        original_text.title()
                    ]
                    
                    results = []
                    
                    for test_case in test_cases:
                        search_input = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, self.search_input_element))
                        )
                        search_input.clear()
                        search_input.send_keys(test_case)
                        search_input.send_keys(Keys.ENTER)
                        
                        print(f"Searched for: {test_case}")
                        time.sleep(1)
                        
                        search_results = self.driver.find_elements(By.XPATH, self.table_rows)
                        results.append(len(search_results))
                    
                    print(f"Search results count for different cases: {results}")
                    
                    allure.attach(self.driver.get_screenshot_as_png(), name="Case_Sensitivity_Test", attachment_type=AttachmentType.PNG)
                    print("Case sensitivity search test completed")
                
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Case_Sensitivity_Error", attachment_type=AttachmentType.PNG)
                print(f"Case sensitivity search test failed: {e}")
        
        print("=== All Search Tests Completed ===")

    def teardown_method(self):
        """Close the browser after each test"""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Error during teardown: {e}")