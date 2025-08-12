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
class TestAudioManagement:
    
    driver = webdriver.Firefox
      

    # Locators
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    imagefile1080_1080_path =os.path.join(base_dir,"1080.1080.jpg")
    Audio1_file =os.path.join(base_dir,"Audio1.mp3")
    Audio2_file =os.path.join(base_dir,"Audio2.mp3")

    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Audio_element = "//div[@data-bs-target='#Audio-Management']"
    add_audio_element = "//span[text()='Add New Audio']"

    audio_upload_element = "//input[@value='mp3_live_url']" 
    audio_field_element = "//input[@type='text' and @name='mp3_live_url']"
    submit_elemnt="//button[@id='audio-mp3-live-url']"
    upload_next_element = "//button[normalize-space(.)='Proceed Next']"
    #edit meta 
    #edit Audio
    title_element = "//input[@name='title']" 
    slug_element = "//input[@name='slug']"
    short_description_element = "//textarea[@name='description']"
    live_description_element ="//div[@class='jodit-wysiwyg']"
    duration_element ="//input[@name='duration']"
    year_element ="//select[@name='year']"

    rating_element ="//select[@name='rating']"
    age_element ="//select[@name='age_restrict']"
    album_element ="//select[@name='album_id']"
    
    Search_Tag_element= "//input[@name='search_tags']"
    #lyric
    audio_lyric_element =  "//input[@type='file' and @accept='.xlsx']"
    Audio_lyric_file = "C:/Users/Dharshini v/Downloads/SampleLyrics (3).xlsx"
     #image
    live_image_element = "//input[@name='image']"
    player_image_element = "//input[@name='player_image']"
    TV_image_element = "//input[@name='tv_image']"
     #access
    access_element = "//select[@name='access']"
    #SEO
    Website_title_element= "//input[@name='website_page_title']"
    Website_Url_element= "//input[@name='website_URL']"
    Meta_description_element= "//textarea[@name='Meta_description']"
     #Status Settings
    feature_element = "(//span[contains(@class, 'admin-slider')])[1]"
    active_element = "(//span[contains(@class, 'admin-slider')])[2]"
    banner_element = "(//span[contains(@class, 'admin-slider')])[3]"
     #SAVE BUTTON
    submit_button_element = "//button[@id='audio-submit-button-down']"
    


    def test_add_guest(self,browser_setup):
        self.driver = browser_setup
        """Login to the admin panel"""
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
        time.sleep(2)

    
        # Scroll to ensure all elements are loaded
        
        # Click "Audio Management"
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            Manage_audio = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.Audio_element))
            )
            self.driver.execute_script("arguments[0].click();", Manage_audio)
            print(" Navigated to 'Audio Management'")
        except Exception as e:
            print(f" Failed to click 'Audio Management': {e}")
            

        # Click "Add New Audio"
        try:
            add_audio_button = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, self.add_audio_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_audio_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", add_audio_button)
            print(" Clicked 'Add New Audio'")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to click 'Add New Audio': {e}")
            

        # Click MP3 upload field
        try:
            mp3_url = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_upload_element))
            )
            mp3_url.click()
            time.sleep(2)
            file_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_field_element))
            )
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
            self.driver.execute_script("arguments[0].scrollIntoView();", file_input)
            file_input.send_keys("https://onlinetestcase.com/wp-content/uploads/2023/06/10-MB-MP3.mp3")
            time.sleep(1)
            self.driver.find_element(By.XPATH, self.submit_elemnt).click()
            time.sleep(2)
            print(" Clicked Submit button")

            next_button = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.XPATH, self.upload_next_element))
            )
            next_button.click()
            print(" The Audio was added successfully. Proceeding to Edit page.")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to click MP3 upload field: {e}")
        
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
            #short description
        
           
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
        
            #Year
        year =WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.year_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year)
        Select(year).select_by_value("2020")
        time.sleep(3)

        try:
            Category = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'audio-category')]"))
             )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Category)
            time.sleep(1)  # Wait for any transitions or overlays
            self.driver.execute_script("arguments[0].click();", Category)

    # Get already selected categories (assuming they are displayed somewhere in the UI)
     # Adjust XPath below based on actual UI elements showing selected options
            selected_elements = self.driver.find_elements(By.XPATH, "(//div[contains(@class, ' css-qbdosj-Input')])[2]")
            selected_categories = [el.text.strip() for el in selected_elements]

            options_to_select = ["Pop", "Hip-Hop" , "Rock"]

            for option in options_to_select:
                if option not in selected_categories:
                   Category.send_keys(option)
                   time.sleep(1)
                   Category.send_keys(Keys.RETURN)
                   time.sleep(1)
                else:
                   print(f"Category '{option}' already selected, skipping.")
        except Exception as e:
                   print(f" Error while selecting categories: {e}")

            #Organizer
        
        #Age Restrict
        try:
            Age = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.age_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Age)
            
            time.sleep(2)
            Select(Age).select_by_visible_text("18_Plus")
            time.sleep(2)
            print(" Age restriction set to '18_Plus' successfully.")
        except Exception as e:
            print(f" Error setting Age restriction: {e}")

         #language dropdown    
        try:
            Lanugage = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'audio-language')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Lanugage)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Lanugage)

    # Get already selected languages (adjust XPath based on actual selected tags)
            selected_elements = self.driver.find_elements(By.XPATH, "(//div[contains(@class, ' css-qbdosj-Input')])[2]")
            selected_languages = [el.text.strip() for el in selected_elements]

            options_to_select = ["Tamil", "English"]

            for option in options_to_select:
                if option not in selected_languages:
                  Lanugage.send_keys(option)
                  time.sleep(1)
                  Lanugage.send_keys(Keys.RETURN)
                  time.sleep(1)
                else:
                  print(f"Language '{option}' already selected, skipping.")
        except Exception as e:
                 print(f" Error while selecting languages: {e}")

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

        


        #Artists
        try:
            Artist = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'audio-artist')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Artist)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Artist)

            # Get already selected artists (adjust XPath if needed)
            selected_artists_elements = self.driver.find_elements(By.XPATH, "(//div[contains(@class, ' css-qbdosj-Input')])[3]")
            selected_artists = [el.text.strip() for el in selected_artists_elements]

            options_to_select = ["John"]

            for option in options_to_select:
                if option not in selected_artists:
                    Artist.send_keys(option)
                    time.sleep(1)
                    Artist.send_keys(Keys.RETURN)
                    time.sleep(1)
                else:
                    print(f"Artist '{option}' already selected, skipping.")
        except Exception as e:
            print(f" Error while selecting artist(s): {e}")
        try:
            Album = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.album_element))
            )
            Select(Album).select_by_value("1")
            time.sleep(2)
        except Exception as e:
            print(f" Error while selecting artist(s): {e}")

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

        
       
        # #BLOCK COUNTRY dropdown
        # Country = self.driver.find_element(By.XPATH, "(//input[contains(@id, 'react-select')])[4]")
        # Country.click()
        # time.sleep(2)
        # # Country.clear()
        # # List of options to select
        # options_to_select = ["ARMENIA",  "CHINA" , "FINLAND","AMERICA"]

        # # Select multiple options
        # for option in options_to_select:
        #     Country.send_keys(option) 
        #     time.sleep(1)  
        #     Country.send_keys(Keys.RETURN)  
        #     time.sleep(1)

        # #Available COUNTRY dropdown
        # Available_Country = self.driver.find_element(By.XPATH,  "(//input[contains(@id, 'react-select')])[5]")
        # Available_Country.click()
        # time.sleep(2)
        # # List of options to select
        # options_to_select = ["JAPAN"]

        # # Select multiple options
        # for option in options_to_select:
        #     Available_Country.send_keys(option) 
        #     time.sleep(1)  
        #     Available_Country.send_keys(Keys.RETURN)  
        #     time.sleep(1)

            
            #image
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
            lyric = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.audio_lyric_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lyric)
            time.sleep(2)
            lyric.send_keys(self.Audio_lyric_file)
            time.sleep(4)
            print(" Lyrics file uploaded successfully.")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="lyric_upload_error", attachment_type=allure.attachment_type.PNG)
            print(f" Failed to upload lyrics file: {e}")


                # Upload Image
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

            # ACCESS 
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

    #    # ====== ACTIVE TOGGLE ======
    #     try:
    #         print(" Checking 'Active' toggle state...")
    #         Active = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, self.active_element))
    #         )
    #         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Active)
    #         time.sleep(1)
    #         active_class = Active.get_attribute("class")
    #         if "active"  in active_class.lower():
    #              print(" 'Active' toggle already ON. Skipped.")
    #         else:
    #             WebDriverWait(self.driver, 10).until(
    #                 EC.element_to_be_clickable((By.XPATH, self.active_element))
    #             )
    #             self.driver.execute_script("arguments[0].click();", Active)
    #             print(" 'Active' toggle was OFF, now turned ON.")
               
    #     except Exception as e:
    #         print(f" Error handling 'Active' toggle: {e}")
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
            time.sleep(8)
            allure.attach(self.driver.get_full_page_screenshot_as_png(),  "Audio was added successfully And it was Redirected to  All Audio Page ",  attachment_type=AttachmentType.PNG)
            time.sleep(6)
            
        except Exception as e:
            print(f" Error clicking submit button: {e}")    
        

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.") 
    
 

    