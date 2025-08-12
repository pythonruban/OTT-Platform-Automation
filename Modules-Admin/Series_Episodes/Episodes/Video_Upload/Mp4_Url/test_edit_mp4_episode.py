import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium.webdriver import ActionChains, Keys
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig

# Add the project root (D:\Automation\) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))





@pytest.mark.usefixtures("browser_setup") 

class TestSeries_EpisodesVideouploading:

    driver = webdriver.Firefox

    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    vttfile_path = os.path.join(base_dir, "vttfile.vtt")  

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Series_episodes_element = "//div[@data-bs-target='#Series-Episode']"
    all_series_element = "//span[text()='All Series']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[3]"
    edit_menu = "(//span[contains(text(), 'Edit')])[3]"

    #episodes 
    Manage_episode_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    episodes_menu = "(//span[contains(text(), 'Manage Episode')])[1]"
     #edit video 
    Edit_video_menu_element = "(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_video_elemnt ="(//span[contains(text(), 'Edit Video')])[1]"

    mp4_radio_button ="(//input[@id='videoTypeOptionRadio'])[3]"
    mp4_url_upload_element = "//input[@id='episode-mp4-url']"
    mp4_url_upload = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    submit_upload_element ="//button[@id='episode-mp4-url-button']"
    proceed_next_element = " //span[text()='Proceed Next']"



    title_element = "//input[@name='title']" 
    slug_element = "//input[@name='slug']"
    short_description_element = "//textarea[@name='episode_description']"
    live_description_element ="//div[@class='jodit-wysiwyg']"
    duration_element ="//input[@name='duration']"
    year_element ="//select[@id='series-custom-select']"
    age_element ="//select[@name='age_restrict']"

    rating_element ="//select[@name='rating']"
   
   
    #SEO
    Website_title_element= "//input[@name='website_page_title']"
    Website_Url_element= "//input[@name='website_URL']"
    Meta_description_element= "//textarea[@name='Meta_description']"
    #SEARCH TAG
    Search_Tag_element= "//input[@name='search_tags']"
    #THUMBNAIL
    live_image_element = "//input[@name='image']"
    player_image_element = "//input[@name='player']"
    TV_image_element = "//input[@name='tv']"
    #trailer type 
    trailer_url_source_element = "//select[@name='trailer_type']"
    embed_url_element = "//input[@id='episode-trailer-embed-url']"
    mp4_url_element ="//input[@id='episode-trailer-mp4-url']"
    m3u8_url_element ="//input[@id='episode-trailer-m3u8_url']"
    Live_source_element ="//input[@name='trailer_url']"
    
    mp4_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    #access
    access_element = "//select[@name='access']"
    choose_file_element ="//input[@id='live-file-upload']"
    video_path ="C:/Users/Dharshini v/Downloads/Animal.mp4"
    #free Duration
    free_duration_element = "(//span[contains(@class, 'admin-slider')])[1]"
    free_text_element = "//input[@name='free_duration_time']"
    #Status Settings
    feature_element = "//input[@name='featured']/following-sibling::span"
    active_element = "//input[@name='active']/following-sibling::span"
    banner_element = "//input[@name='banner']/following-sibling::span"
    #intro time
    Skip_Start_Time_element ="//input[@name='skip_start_time']"
    Skip_end_Time_element ="//input[@name='skip_end_time']"
    recap_Start_Time_element ="//input[@name='recap_start_time']"
    recap_end_Time_element ="//input[@name='recap_end_time']"
    Skip_Start_session_element ="//input[@name='skip_start_session']"
    Skip_End_session_element ="//input[@id='episode-recap-start-session']"

  
    #Subtitle
    tamizh_subtitle_element ="//input[@name='ta']"
    English_subtitle_element ="//input[@name='en']"
    spanish_subtitle_element ="//input[@name='sp']"
    close_button_element ="(//button[@type='button' and contains(@class, 'bg-transparent')])[2]"
    submit_button_element = "//button[@id='episodeFormSubmitButtonDown']"

    def test_edit_mp4_Episodes(self,browser_setup):
        self.driver = browser_setup    
            
        """Navigate and add a Live Stream """
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()
        actions = ActionChains(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.email_element))
            ).send_keys(ReadConfig.getAdminId())

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.password_element))
            ).send_keys(ReadConfig.getPassword())

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.login_element))
            ).click()

            print(" Login Successful!")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error", attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 
        
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(" Scrolled to bottom of the page.")
            
        except Exception as e:
            
            print(f" Failed to scroll the page: {e}")

# W
        try:
            all_series = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, self.Series_episodes_element))
             )
            self.driver.execute_script("arguments[0].click();", all_series)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")
   
            

        try:
            add_series_button = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, self.all_series_element))
        )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_series_button)
            time.sleep(1)  # Smooth scroll
            self.driver.execute_script("arguments[0].click();", add_series_button)
            print(" Clicked 'Add New live stream'")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to click 'Add New live stream': {e}")

        try:
            # ====== EDIT ELEMENT ======
            edit = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.edit_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_menu))
            ).click()
            time.sleep(6)

            print(" Edit element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        
        try:
            # ====== EDIT ELEMENT ======
            Manage_episodes = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Manage_episode_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Manage_episodes)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.Manage_episode_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.episodes_menu))
            ).click()
            time.sleep(6)

            print(" Manage Episodes element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        try:
            # ====== EDIT ELEMENT ======
            EDit_video = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Edit_video_menu_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", EDit_video)
            time.sleep(3)

            actions = ActionChains(self.driver)
            element_to_hover = self.driver.find_element(By.XPATH, self.Edit_video_menu_element)
            actions.move_to_element(element_to_hover).perform()
            time.sleep(2)

            # ====== EDIT MENU ======
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.edit_video_elemnt))
            ).click()
            time.sleep(6)

            print(" Manage Episodes element and menu interaction succeeded.")
        
        except Exception as e:
            print(f" Failed to interact with edit element or menu: {e}")

        #video Uploading 
        try:
            radio =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.mp4_radio_button))
            )
            self.driver.execute_script("arguments[0].parentNode.scrollIntoView({block: 'center'});", radio)
            time.sleep(2)
            radio.click()
            time.sleep(2)
            # Locate and scroll to the Live Source dropdown
            series_source_dropdown = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.mp4_url_upload_element))
            )
            time.sleep(2)
            series_source_dropdown.send_keys(self.mp4_url_upload)
            print(f" Entered Embed URL: {self.mp4_url_upload}")
            time.sleep(2)
            WebDriverWait(self.driver, 320).until(EC.visibility_of_element_located((By.XPATH, self.submit_button_element))).click()
            time.sleep(2) 
            WebDriverWait(self.driver, 320).until(EC.visibility_of_element_located((By.XPATH, self.proceed_next_element))).click() 
            time.sleep(4)

        except Exception as e:
            print(f" Error while setting embed URL: {e}")
            #Add Live stream

            #Add Live stream
        try:
            # Generate a random uppercase string of length between 5 and 7
            length = random.randint(5, 7)
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")

            print(f"Using XPath: {self.title_element}")

            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name)
            time.sleep(2)
            name.clear()
            time.sleep(2)  # small delay to ensure field is cleared
            name.send_keys(auto_name)
            time.sleep(2)
            print(" Auto name entered in the title field.")

        except Exception as e:
            print(f" Failed to enter title: {e}")


        try:
                print(f"Using XPath for slug input: {self.slug_element}")

                slug = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, self.slug_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
                time.sleep(2)
                slug.clear()
                time.sleep(2)
                slug.send_keys(auto_name)
                time.sleep(2)
                print(" Auto slug entered using the name.")

        except Exception as e:
                print(f" Failed to enter slug: {e}")
        
           
        test_inputs = {
        "negative_1": "",
        "negative_2": "B" * 251,
        "positive_2": "A" * 250,
        "positive_1": "This is a valid short description.",
        

        }

            # Loop through tests
        for case_name, input_text in test_inputs.items():
                try:
                        try:
                            short_desc_field = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, self.short_description_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", short_desc_field)
                            time.sleep(1)  # Smooth scroll
                            short_desc_field.clear()
                            time.sleep(2)
                            short_desc_field.send_keys(input_text)


                            # Validation conditions
                            if not input_text.strip():
                                msg = " Negative Test: Empty or whitespace-only input is invalid."
                            elif len(input_text) > 1000:
                                msg = " Negative Test: Input exceeds 100 characters."
                            elif all(not c.isalnum() for c in input_text):
                                msg = " Negative Test: Only special characters — likely invalid."
                            else:
                                msg = " Positive Test: Input accepted as valid."

                            print(msg)

                        except Exception as e:
                            error_msg = f" Exception during test '{case_name}': {e}"
                            print(error_msg)

                except Exception as e:
                    outer_msg = f" Unexpected failure in loop for case '{case_name}': {e}"
                    print(outer_msg)

       
            

        
        try:
            live_description = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.live_description_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", live_description)
            time.sleep(2)
            live_description.click()
            time.sleep(3)
            actions.send_keys(
            "Artificial intelligence is a field of science concerned with building computers and machines that can reason, learn, and act in such a way that would normally require human intelligence or that involves data whose scale exceeds what humans can analyze."
             ).perform()
            time.sleep(3)
            print(" Entered Live Description")
        except Exception as e:
            print(f" Failed to enter Live Description: {e}")

        
            
            #Organizer
        try:
            print("Starting category selection...")
            
            # 1. Click into the react-select input box
            input_xpath = "(//input[contains(@id, 'react-select')])[1]"
            input_box = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, input_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)
            input_box.click()
            time.sleep(2)  # Increased wait time for dropdown to fully load

            # 2. Wait for dropdown menu to appear and get all options
            # Fixed: Look for actual dropdown options, not input elements
            dropdown_options_xpath = [
                "//div[contains(@class, 'react-select__option')]",
                "//div[contains(@class, 'css-') and @role='option']",
                "//div[contains(@class, 'select__option')]",
                "//*[@role='option']"
            ]
            
            option_elements = []
            for xpath in dropdown_options_xpath:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        print(f"Found options using xpath: {xpath}")
                        break
                except TimeoutException:
                    continue
            
            if not option_elements:
                print("No dropdown options found. Trying alternative method...")
                # Alternative: Type a character to trigger options
                input_box.send_keys("a")
                time.sleep(1)
                input_box.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                
                # Try again to find options
                for xpath in dropdown_options_xpath:
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        break

            # 3. Extract option labels
            option_labels = []
            for opt in option_elements:
                text = opt.text.strip()
                if text and text not in option_labels:
                    option_labels.append(text)

            print(f"Available options: {option_labels}")
            
            if not option_labels:
                print("No options found in dropdown!")
            else:
                # 4. Select random options (up to 3)
                num_to_select = min(3, len(option_labels))
                random_options = random.sample(option_labels, num_to_select)
                print(f"Will select: {random_options}")

                successfully_selected = []
                
                # 5. For each option, search and select
                for i, option in enumerate(random_options):
                    try:
                        print(f"Selecting option {i+1}: {option}")
                        
                        # Clear the input and type the option name
                        input_box.clear()
                        time.sleep(0.5)
                        input_box.send_keys(option)
                        time.sleep(1.5)  # Wait for filtering to complete
                        
                        # Try multiple methods to select the option
                        selected = False
                        
                        # Method 1: Click on the filtered option
                        try:
                            filtered_option = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-select__option') and normalize-space(text())='{option}']"))
                            )
                            self.driver.execute_script("arguments[0].click();", filtered_option)
                            selected = True
                            print(f"✓ Selected {option} by clicking")
                        except:
                            pass
                        
                        # Method 2: Press ENTER
                        if not selected:
                            try:
                                input_box.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by pressing ENTER")
                            except:
                                pass
                        
                        # Method 3: Press DOWN arrow then ENTER
                        if not selected:
                            try:
                                input_box.send_keys(Keys.ARROW_DOWN)
                                time.sleep(0.5)
                                input_box.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by arrow + ENTER")
                            except:
                                pass
                        
                        if selected:
                            successfully_selected.append(option)
                            time.sleep(1)  # Wait between selections
                        else:
                            print(f"✗ Failed to select {option}")
                            
                    except Exception as e:
                        print(f"Error selecting option '{option}': {e}")
                        continue

                print(f"Successfully selected options: {successfully_selected}")

        except Exception as e:
            print(f"Error while selecting dynamic random options: {e}")

                   
        try:
            Age = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.age_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Age)
            time.sleep(2)
            Age.click()
            time.sleep(2)
            Select(Age).select_by_visible_text("18")
            time.sleep(2)
            print(" Age restriction set to '18_Plus' successfully.")
        except Exception as e:
            print(f" Error setting Age restriction: {e}")

        #Lanugae
        try:
            print("Starting Lanugage selection...")
            
            # 1. Click into the react-select input box
            input_xpath = "(//input[contains(@id, 'react-select')])[2]"
            Lanugage = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, input_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Lanugage)
            Lanugage.click()
            time.sleep(2)  # Increased wait time for dropdown to fully load

            # 2. Wait for dropdown menu to appear and get all options
            # Fixed: Look for actual dropdown options, not input elements
            dropdown_options_xpath = [
                "//div[contains(@class, 'react-select__option')]",
                "//div[contains(@class, 'css-') and @role='option']",
                "//div[contains(@class, 'select__option')]",
                "//*[@role='option']"
            ]
            
            option_elements = []
            for xpath in dropdown_options_xpath:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        print(f"Found options using xpath: {xpath}")
                        break
                except TimeoutException:
                    continue
            
            if not option_elements:
                print("No dropdown options found. Trying alternative method...")
                # Alternative: Type a character to trigger options
                Lanugage.send_keys("a")
                time.sleep(1)
                Lanugage.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                
                # Try again to find options
                for xpath in dropdown_options_xpath:
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        break

            # 3. Extract option labels
            option_labels = []
            for opt in option_elements:
                text = opt.text.strip()
                if text and text not in option_labels:
                    option_labels.append(text)

            print(f"Available options: {option_labels}")
            
            if not option_labels:
                print("No options found in dropdown!")
            else:
                # 4. Select random options (up to 3)
                num_to_select = min(3, len(option_labels))
                random_options = random.sample(option_labels, num_to_select)
                print(f"Will select: {random_options}")

                successfully_selected = []
                
                # 5. For each option, search and select
                for i, option in enumerate(random_options):
                    try:
                        print(f"Selecting option {i+1}: {option}")
                        
                        # Clear the input and type the option name
                        Lanugage.clear()
                        time.sleep(0.5)
                        Lanugage.send_keys(option)
                        time.sleep(1.5)  # Wait for filtering to complete
                        
                        # Try multiple methods to select the option
                        selected = False
                        
                        # Method 1: Click on the filtered option
                        try:
                            filtered_option = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-select__option') and normalize-space(text())='{option}']"))
                            )
                            self.driver.execute_script("arguments[0].click();", filtered_option)
                            selected = True
                            print(f"✓ Selected {option} by clicking")
                        except:
                            pass
                        
                        # Method 2: Press ENTER
                        if not selected:
                            try:
                                Lanugage.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by pressing ENTER")
                            except:
                                pass
                        
                        # Method 3: Press DOWN arrow then ENTER
                        if not selected:
                            try:
                                Lanugage.send_keys(Keys.ARROW_DOWN)
                                time.sleep(0.5)
                                Lanugage.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by arrow + ENTER")
                            except:
                                pass
                        
                        if selected:
                            successfully_selected.append(option)
                            time.sleep(1)  # Wait between selections
                        else:
                            print(f"✗ Failed to select {option}")
                            
                    except Exception as e:
                        print(f"Error selecting option '{option}': {e}")
                        continue

                print(f"Successfully selected options: {successfully_selected}")

        except Exception as e:
            print(f"Error while selecting dynamic random options: {e}")

        try:
            Rating = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.rating_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Rating)
            time.sleep(2)
            Select(Rating).select_by_value("9")
            time.sleep(2)
            print(" Rating set to 9 successfully.")
        except Exception as e:
            print(f" Error setting rating: {e}")
                 

                    # #Artists
        try:
            print("Starting Artists selection...")
            
            # 1. Click into the react-select input box
            input_xpath = "(//input[contains(@id, 'react-select')])[3]"
            Artists = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, input_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Artists)
            Artists.click()
            time.sleep(2)  # Increased wait time for dropdown to fully load

            # 2. Wait for dropdown menu to appear and get all options
            # Fixed: Look for actual dropdown options, not input elements
            dropdown_options_xpath = [
                "//div[contains(@class, 'react-select__option')]",
                "//div[contains(@class, 'css-') and @role='option']",
                "//div[contains(@class, 'select__option')]",
                "//*[@role='option']"
            ]
            
            option_elements = []
            for xpath in dropdown_options_xpath:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        print(f"Found options using xpath: {xpath}")
                        break
                except TimeoutException:
                    continue
            
            if not option_elements:
                print("No dropdown options found. Trying alternative method...")
                # Alternative: Type a character to trigger options
                Artists.send_keys("a")
                time.sleep(1)
                Artists.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                
                # Try again to find options
                for xpath in dropdown_options_xpath:
                    option_elements = self.driver.find_elements(By.XPATH, xpath)
                    if option_elements:
                        break

            # 3. Extract option labels
            option_labels = []
            for opt in option_elements:
                text = opt.text.strip()
                if text and text not in option_labels:
                    option_labels.append(text)

            print(f"Available options: {option_labels}")
            
            if not option_labels:
                print("No options found in dropdown!")
            else:
                # 4. Select random options (up to 3)
                num_to_select = min(3, len(option_labels))
                random_options = random.sample(option_labels, num_to_select)
                print(f"Will select: {random_options}")

                successfully_selected = []
                
                # 5. For each option, search and select
                for i, option in enumerate(random_options):
                    try:
                        print(f"Selecting option {i+1}: {option}")
                        
                        # Clear the input and type the option name
                        Artists.clear()
                        time.sleep(0.5)
                        Artists.send_keys(option)
                        time.sleep(1.5)  # Wait for filtering to complete
                        
                        # Try multiple methods to select the option
                        selected = False
                        
                        # Method 1: Click on the filtered option
                        try:
                            filtered_option = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-select__option') and normalize-space(text())='{option}']"))
                            )
                            self.driver.execute_script("arguments[0].click();", filtered_option)
                            selected = True
                            print(f"✓ Selected {option} by clicking")
                        except:
                            pass
                        
                        # Method 2: Press ENTER
                        if not selected:
                            try:
                                Artists.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by pressing ENTER")
                            except:
                                pass
                        
                        # Method 3: Press DOWN arrow then ENTER
                        if not selected:
                            try:
                                Artists.send_keys(Keys.ARROW_DOWN)
                                time.sleep(0.5)
                                Lanugage.send_keys(Keys.RETURN)
                                selected = True
                                print(f"✓ Selected {option} by arrow + ENTER")
                            except:
                                pass
                        
                        if selected:
                            successfully_selected.append(option)
                            time.sleep(1)  # Wait between selections
                        else:
                            print(f"✗ Failed to select {option}")
                            
                    except Exception as e:
                        print(f"Error selecting option '{option}': {e}")
                        continue

                print(f"Successfully selected options: {successfully_selected}")

        except Exception as e:
            print(f"Error while selecting dynamic random options: {e}")   
            
        try:
            duration_inputs = ["07:22:00", "25:25:0", "01:45:33"]
            pattern = r"^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$"
            max_allowed_seconds = 24 * 3600 + 24 * 60 + 24  # 24h 24m 24s

            for duration_input in duration_inputs:
                print(f"\n🔹 Testing Duration: {duration_input}")
                match = re.match(pattern, duration_input)

                if match:
                    h, m, s = map(int, duration_input.split(":"))
                    total_seconds = h * 3600 + m * 60 + s

                    if total_seconds < max_allowed_seconds:
                        try:
                            duration_field = WebDriverWait(self.driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, self.duration_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", duration_field)
                            time.sleep(1)
                            duration_field.click()
                            duration_field.clear()
                            time.sleep(1)
                            duration_field.send_keys(duration_input)
                            print(f"  Duration '{duration_input}' entered successfully.")
                            time.sleep(1)
                        except Exception as field_error:
                            print(f"  Error entering duration '{duration_input}': {field_error}")
                    else:
                        print(f"  Input '{duration_input}' exceeds max allowed duration.")
                else:
                    print(f"  Invalid time format for '{duration_input}'. Must be HH:MM:SS.")

        except Exception as e:
            print(f" General error: {e}")   
            
        try:
            duration_inputs = ["07:22:00", "25:25:0", "01:45:33"]
            pattern = r"^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$"
            max_allowed_seconds = 24 * 3600 + 24 * 60 + 24  # 24h 24m 24s

            for duration_input in duration_inputs:
                print(f"\n🔹 Testing Duration: {duration_input}")
                match = re.match(pattern, duration_input)

                if match:
                    h, m, s = map(int, duration_input.split(":"))
                    total_seconds = h * 3600 + m * 60 + s

                    if total_seconds < max_allowed_seconds:
                        try:
                            duration_field = WebDriverWait(self.driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, self.duration_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", duration_field)
                            time.sleep(1)
                            duration_field.click()
                            duration_field.clear()
                            time.sleep(1)
                            duration_field.send_keys(duration_input)
                            print(f"  Duration '{duration_input}' entered successfully.")
                            time.sleep(1)
                        except Exception as field_error:
                            print(f"  Error entering duration '{duration_input}': {field_error}")
                    else:
                        print(f"  Input '{duration_input}' exceeds max allowed duration.")
                else:
                    print(f"  Invalid time format for '{duration_input}'. Must be HH:MM:SS.")

        except Exception as e:
            print(f" General error: {e}")

        try:
            # Scroll to "Free Duration" toggle
            Free_Duration = self.driver.find_element(By.XPATH, self.free_duration_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Free_Duration)
            time.sleep(1)

            # Check if the toggle is already enabled
            is_checked = Free_Duration.get_attribute("aria-checked") == "true" or \
                        Free_Duration.get_attribute("class").find("active") != -1

            if not is_checked:
                self.driver.execute_script("arguments[0].click();", Free_Duration)
                time.sleep(2)
                self.driver.find_element(By.XPATH, self.free_text_element).send_keys("01042025")
                time.sleep(2)
                print(" Feature toggle clicked successfully!")
                time.sleep(2)
            else:
                print(" Feature toggle not clicked enabled, skipping click.")

            # Enter Free Duration Date
            
        except Exception as e:
            print(f" Error handling Free Duration toggle or input: {e}")
        # Intro time
       
        try:
            star = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Skip_Start_Time_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", star)
            star.clear()
            time.sleep(2)
            star.send_keys("010200")
            time.sleep(2)

            end=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Skip_end_Time_element))
            )
            end.clear()
            time.sleep(2)
            end.send_keys("005000")
            time.sleep(2)

            rec = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.recap_Start_Time_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rec)
            rec.clear()
            time.sleep(2)
            rec.send_keys("001229")
            time.sleep(2)

            rec_end =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.recap_end_Time_element))
            )
            rec_end.clear()
            time.sleep(2)
            rec_end.send_keys("001830")
            time.sleep(2)

            ses = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Skip_Start_session_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ses)
            ses.clear()
            time.sleep(2)
            ses.send_keys("002410")
            time.sleep(2)

            ses_end=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.Skip_End_session_element))
            )
            ses_end.clear()
            time.sleep(2)
            ses_end.send_keys("004042")
            time.sleep(2)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element interaction failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
                   

        # ====== FEATURE TOGGLE ======
        try:
            Feature = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.feature_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Feature)
            time.sleep(1)
            feature_class = Feature.get_attribute("class")
            if "active" in feature_class.lower():
                print(" 'Feature' toggle already active. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.feature_element))
                )
                self.driver.execute_script("arguments[0].click();", Feature)
                print(" 'Feature' toggle was OFF, now turned ON.")
        except Exception as e:
            print(f" Error handling 'Feature' toggle: {e}")

        # ====== ACTIVE TOGGLE ======
        # try:
        #     print(" Checking 'Active' toggle state...")
        #     Active = WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, self.active_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Active)
        #     time.sleep(1)
        #     active_class = Active.get_attribute("class")
        #     if "active"  in active_class.lower():
        #          print(" 'Active' toggle already ON. Skipped.")
        #     else:
        #         WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, self.active_element))
        #         )
        #         self.driver.execute_script("arguments[0].click();", Active)
        #         print(" 'Active' toggle was OFF, now turned ON.")
               
        # except Exception as e:
        #     print(f" Error handling 'Active' toggle: {e}")
        
        # ====== BANNER TOGGLE ======
        try:
            print(" Checking 'Banner' toggle state...")
            banner = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.banner_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", banner)
            time.sleep(1)
            banner_class = banner.get_attribute("class")
            if "active" in banner_class.lower():
                print(" 'Banner' toggle already active. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.banner_element))
                )
                self.driver.execute_script("arguments[0].click();", banner)
                print(" 'Banner' toggle was OFF, now turned ON.")
            time.sleep(2)
        except Exception as e:
            print(f" Error handling 'Banner' toggle: {e}")
        
         
    # Advertisement
 
    #    # Select user role Dropdown
    #     drop_down3 = self.driver.find_element(By.XPATH, self.pre_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down3)
    #     drop_down3.click()
    #     time.sleep(2)
    #     select = Select(drop_down3)
    #     select.select_by_visible_text("8")
 
    #        # Select user role Dropdown
    #     drop_down4 = self.driver.find_element(By.XPATH, self.post_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down4)
    #     drop_down4.click()
    #     time.sleep(2)
    #     select = Select(drop_down4)
    #     select.select_by_visible_text("8")
 
    #        # Select user role Dropdown
    #     drop_down5 = self.driver.find_element(By.XPATH, self.mid_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down5)
    #     drop_down5.click()
    #     time.sleep(2)
    #     select = Select(drop_down5)
    #     select.select_by_visible_text("8")
 

        try:
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.live_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imageFile_path_9_16) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
         # Player Image field
        try:
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.player_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imageFile1280_720_path)
                

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        #Tv Image Module

        try:
            image=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.TV_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.imageFile1280_720_path)
                
        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        try:
            # Locate and scroll to the Live Source dropdown
            trailer_type = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.trailer_url_source_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trailer_type)
            time.sleep(2)
            # Select only embed_url from dropdown
            Select(trailer_type).select_by_value("mp4_url")
            print("🔹 Selected Live Source: mp4_url")
            time.sleep(2)

            # Enter the Embed URL
            
            _url_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.mp4_url_element))
            )
            time.sleep(2)
            _url_input.clear()
            time.sleep(2)
            _url_input.send_keys(self.mp4_url)
            print(f" Entered Embed URL: {self.mp4_url}")
            time.sleep(2)

        except Exception as e:
            print(f" Error while setting embed URL: {e}")


        try:
            # Locate the dropdown element
            ACCESS = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.access_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ACCESS)
            dropdown = Select(ACCESS)

            # Select only 'guest' access
            access_value = "guest"
            try:
                time.sleep(2)
                dropdown.select_by_value(access_value)
                time.sleep(2)
                msg = f" Access type selected: {access_value}"
                print(msg)
            except Exception as inner_e:
                error_msg = f" Failed to select access '{access_value}': {inner_e}"
                print(error_msg)

        except Exception as e:
            final_error = f" Error initializing access dropdown: {e}"
            print(final_error)
            #image
        
        try:
            # SEO Name (Website Title)
          
                seo_name = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.Website_title_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", seo_name)
                time.sleep(2)
                seo_name.send_keys("CHATGPT")
                time.sleep(3)
                print(" SEO Name entered.")
            

            # SEO Website URL
          
                url = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.Website_Url_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url)
                time.sleep(2)
                url.send_keys("https://chatgpt.com/")
                time.sleep(3)
                print(" SEO URL entered.")
        

            # SEO Meta Description
   
                desc = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, self.Meta_description_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", desc)
                time.sleep(2)
                desc.send_keys(
                    "Artificial intelligence is a constellation of many different technologies working together "
                    "to enable machines to sense, comprehend, act, and learn with human-like levels of intelligence"
                )
                time.sleep(2)
                print(" Meta Description entered.")
        except Exception as e:
                print(f" Error entering Seo DATA: {e}")

        Search_tag = self.driver.find_element(By.XPATH, self.Search_Tag_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Search_tag)
        time.sleep(2)
        Search_tag.click()
        time.sleep(2)

        # List of options to select
        options_to_select = ["Sample", "video"]

        # Send each value individually followed by RETURN
        for option in options_to_select:
            Search_tag.send_keys(option)
            time.sleep(1)  # Let autocomplete suggestions appear, if any
            Search_tag.send_keys(Keys.RETURN)
            time.sleep(1)  # Wait for the tag to be added

        try:
            tamizh=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.tamizh_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tamizh)
            time.sleep(2)
            tamizh.send_keys(self.vttfile_path) 

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
         # Player Image field
        try:
            english=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.English_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", english)
            time.sleep(2)
            english.send_keys(self.vttfile_path)
                

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        #Tv Image Module

        try:
            Malayalam=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.malayalam_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Malayalam)
            time.sleep(2)
            Malayalam.send_keys(self.vttfile_path)
            #close button 
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.close_button_element))
            ).click()
            time.sleep(2)
                
        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)

    
           # ====== SUBMIT BUTTON ======
        try:

            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All metadata was entered successfully while adding the livestream for the guest user ", attachment_type=AttachmentType.PNG)
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print(" The Live stream was added successfully.")
            time.sleep(3)
            allure.attach(self.driver.get_full_page_screenshot_as_png(),  "Live stream was added successfully And it was Redirected to  All live Page ",  attachment_type=AttachmentType.PNG)
            time.sleep(6)
            
        except Exception as e:
            print(f" Error clicking submit button: {e}")    
               
                      

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")   
 
 