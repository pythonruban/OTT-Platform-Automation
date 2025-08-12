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

class TestSeries_EpisodesUserAccess:

    driver = webdriver.Firefox    
    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
    vttfile_path = os.path.join(base_dir, "vttfile.vtt")  

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    Series_episodes_element = "//div[@data-bs-target='#Series-Episode']"
    all_series_element = "//span[text()='All Series']"
    edit_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    edit_menu = "(//span[contains(text(), 'Edit')])[1]"
    #episodes 
    Manage_episode_element ="(//span[contains(@class, 'editdropdown-button')])[1]"
    episodes_menu = "(//span[contains(text(), 'Manage Episode')])[1]"
    m3u8_radio_button ="(//input[@id='videoTypeOptionRadio'])[2]"
    m3u8_url_upload_element = "//input[@id='episode-m3u8-url']"
    m3u8_url_upload = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
    submit_upload_element ="//button[.//span[text()='Submit']]"
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
    player_image_element = "//input[@name='player_image']"
    TV_image_element = "//input[@name='tv_image']"
    #trailer type 
    trailer_url_source_element = "//select[@name='trailer_type']"
    embed_url_element = "//input[@id='episode-trailer-embed-url']"
    mp4_url_element ="//input[@id='episode-trailer-mp4-url']"
    m3u8_url_element ="//input[@id='episode-trailer-m3u8_url']"
    Episodes_source_element ="//input[@name='trailer_url']"
    embed_url = "https://www.youtube.com/embed/YbCF6OqTWug?si=9NmwCGxALpAJ7ykS"
   
    #access
    access_element = "//select[@name='access']"
   
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
    #close button
    close_button_element ="(//button[ contains(@class, 'bg-transparent')])[2]"
    
    submit_button_element = "//button[@id='episodeFormSubmitButtonDown']"
    #fortend xpath
    frontend_email_element = "(//input[@id='signin-email'])"
    fortend_password_element = "(//input[@id='signin-password'])"
    forntend_login_element = "(//button[@type='submit'])"
    profile_element = "(//div[contains(@class, 'avatarProfile') and contains(@class, 'rounded-circle')]//img)[1]"
    episodes_menu_frontend_element ="//li[@id='header-Tv Show']//span[text()='Tv Show']"
    series_list_element = "(//div[@class='swiper-wrapper']//div[contains(@class, 'swiper-slide')])[3]//a"
    forntend_episodes_image_element = "(//div[@class='homeListImage active']//img)[1]"
    watch_now_button_element = "//button[@id='login-button']"
    play_button_element ="//button[contains(@class, 'ytp-large-play-button') and @title='Play']"


    def test_add_guest_episodes(self):    
            
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

        #video Uploading 
        try:
            radio =WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.m3u8_radio_button))
            )
            self.driver.execute_script("arguments[0].parentNode.scrollIntoView({block: 'center'});", radio)
            time.sleep(2)
            radio.click()
            time.sleep(2)
            # Locate and scroll to the Live Source dropdown
            series_source_dropdown = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.m3u8_url_upload_element))
            )
            time.sleep(2)
            series_source_dropdown.send_keys(self.m3u8_url_upload)
            print(f" Entered Embed URL: {self.m3u8_url_upload}")
            time.sleep(2)
            submit = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.submit_upload_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
            time.sleep(2)
            submit.click()
            time.sleep(2) 
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.proceed_next_element))).click() 
            time.sleep(4)

        except Exception as e:
            print(f" Error while setting embed URL: {e}")
            #Add Live stream

        #edit Live streamtry:
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 102-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]    

            for idx, (test_name, title_value) in enumerate(test_data):
                try:
                    print(f"\n🔹 {test_name} running...")

                    # === Title Field ===
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.title_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f" Title entered: {title_value[:30]}")

                    # === Slug Field ===
                    slug_input = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, self.slug_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                    time.sleep(2)

                    if idx == 0:
                        slug_input.clear()
                        slug_input.send_keys("x")
                        print(" Manually set slug to 'x' for negative test.")
                    else:
                        auto_slug = slug_input.get_attribute("value")
                        print(f"🔎 Auto-generated slug: {auto_slug}")
                        if title_value.lower()[:3] not in auto_slug.lower():
                            print(" Slug does not reflect title.")
                        else:
                            print(" Slug reflects title correctly.")

                    # === Submit Form ===
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    print(f" Submitted form for: {test_name}")
                    time.sleep(2)

                    # === Scroll back to Title Field ===
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)

                except Exception as case_error:
                    print(f" {test_name} - Error: {case_error}")

            # Final Screenshot Attachments for Reporting
            try:
                allure.attach(self.driver.get_screenshot_as_png(),
                            name="Final_TitleSlugValidation",
                            attachment_type=AttachmentType.PNG)
                print(" Final screenshot for Title & Slug validation attached.")
            except:
                print(" Screenshot capture failed at final step.")

        except Exception as total_error:
            print(f" Outer error in title & slug validation block: {total_error}")
                            
        test_inputs = {
            "negative_1": "",  # Empty input
            "negative_2": "B" * 251,  # Exceeds 250 characters, still a single character repeated
            "positive_1": "This is a valid short description.",
            "positive_2": (
                "This is a detailed description that contains multiple meaningful words, "
                "crafted to stay under the maximum character limit of two hundred and fifty. "
                "It simulates a real paragraph that a user might enter in a form input."
            )
        }

            # Loop through tests
        for case_name, input_text in test_inputs.items():
                try:
                    with allure.step(f"🔹 Test Case: {case_name}"):
                        try:
                            short_desc_field = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, self.short_description_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", short_desc_field)
                            time.sleep(1)  # Smooth scroll
                            short_desc_field.clear()
                            time.sleep(2)
                            short_desc_field.send_keys(input_text)

                            # Attach input value to Allure
                            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=f"{case_name} - Input",attachment_type=AttachmentType.PNG)

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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Live Description Error",attachment_type=AttachmentType.PNG)
            print(f" Failed to enter Live Description: {e}")
            
            #Organizer
        try:
            # ===== NEGATIVE CASE: Submit without selecting category =====
            print(" Negative Test: Submit without selecting Category")

            submit_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
            time.sleep(2)

            print("Submitted form without selecting category — expected validation.")

            # Optionally scroll to the error field itself
            try:
                category_error = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Category') or contains(text(), 'required')]"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_error)
                print(" Validation error message for category shown.")
            except:
                print(" No specific validation error located.")

            # Final allure screenshot for negative case only
            try:
                allure.attach(self.driver.get_screenshot_as_png(),
                            name="Negative - Missing Category Validation",
                            attachment_type=AttachmentType.PNG)
            except:
                print(" Failed to capture screenshot for negative case.")

            # ===== POSITIVE CASE: Select category and submit again =====
            print(" Positive Test: Selecting categories now...")

            category_input = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "(//input[contains(@id, 'react-select')])[1]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_input)
            time.sleep(1)
            category_input.click()
            time.sleep(1)

            # Select categories dynamically
            options_to_select = ["Action", "Drama", "Romance"]
            for option in options_to_select:
                category_input.send_keys(option)
                time.sleep(1)
                category_input.send_keys(Keys.RETURN)
                time.sleep(1)
                print(f"Selected category: {option}")

            # Scroll to submit again
            submit_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
            print(" Form submitted successfully after selecting categories.")
            time.sleep(2)

        except Exception as e:
            print(f" Error in category validation: {e}")
            try:
                allure.attach(self.driver.get_screenshot_as_png(),
                            name="Error - Category Field",
                            attachment_type=AttachmentType.PNG)
            except:
                print(" Could not attach error screenshot.")


                    
        try:
            # === Step 1: Try to submit without selecting age (Negative) ===
            print("🚨 Negative Test: Submit without selecting Age")

            submit_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
            time.sleep(2)

            # Attach screenshot of validation error (only for negative case)
            try:
                allure.attach(self.driver.get_screenshot_as_png(),
                            name="Negative - Age Not Selected",
                            attachment_type=AttachmentType.PNG)
                print("Submitted without selecting Age — validation expected.")
            except:
                print(" Failed to attach screenshot for negative case.")

            # === Step 2: Now select a valid Age and submit (Positive) ===
            print(" Positive Test: Select Age and Submit")

            age_dropdown = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.age_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", age_dropdown)
            time.sleep(1)

            # Select Age: "18"
            Select(age_dropdown).select_by_visible_text("18")
            time.sleep(1)
            print("Age '18' selected.")

            # Return to age dropdown after selecting
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", age_dropdown)

            # Re-click Submit after selecting age
            submit_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
            time.sleep(2)
            print("Form submitted successfully after selecting Age.")

        except Exception as e:
            print(f" Error during Age dropdown validation: {e}")
            try:
                allure.attach(self.driver.get_screenshot_as_png(),
                            name="Age Dropdown Validation Error",
                            attachment_type=AttachmentType.PNG)
            except:
                print(" Could not attach screenshot for error.")
        try:
            Lanugage = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, 'react-select')])[2]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Lanugage)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Lanugage)

    # Get already selected languages (adjust XPath based on actual selected tags)
            selected_elements = self.driver.find_elements(By.XPATH, "(//input[contains(@id, 'react-select')])[2]")
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
                 

            # #Artists
        try:
            Artist = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, 'react-select')])[3]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Artist)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", Artist)

            # Get already selected artists (adjust XPath if needed)
            selected_artists_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'selected-artist')]")
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

                
        try:
            duration_inputs = ["00:00:00", "24:00:00", "01:45:33"]
            pattern = r"^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$"
            max_allowed_seconds = 24 * 3600 + 24 * 60 + 24  # 24h 24m 24s

            for index, duration_input in enumerate(duration_inputs):
                print(f"\nTesting Duration: {duration_input}")
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
                            print(f"Duration '{duration_input}' entered successfully.")
                            time.sleep(1)

                            # ===== Submit only for first item (00:00:00) =====
                            if index == 0:
                                print("Submitting 00:00:00 duration to trigger validation...")
                                submit_btn = WebDriverWait(self.driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                                )
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                                submit_btn.click()
                                time.sleep(2)

                                try:
                                    allure.attach(self.driver.get_screenshot_as_png(),
                                                name=f"Validation_Error_{duration_input.replace(':', '-')}",
                                                attachment_type=AttachmentType.PNG)
                                    print("Validation screenshot captured.")
                                except:
                                    print("Screenshot capture failed.")

                            time.sleep(1)

                        except Exception as field_error:
                            print(f"Error entering duration '{duration_input}': {field_error}")

                    else:
                        print(f"Input '{duration_input}' exceeds max allowed duration.")
                        try:
                            allure.attach(self.driver.get_screenshot_as_png(),
                                        name=f"Negative_Exceeds_Max_{duration_input}",
                                        attachment_type=AttachmentType.PNG)
                        except:
                            print("Screenshot failed for exceeded duration.")

                else:
                    print(f"Invalid time format for '{duration_input}'. Must be HH:MM:SS.")
                    try:
                        allure.attach(self.driver.get_screenshot_as_png(),
                                    name=f"Negative_Invalid_Format_{duration_input}",
                                    attachment_type=AttachmentType.PNG)
                    except:
                        print("Screenshot failed for invalid format.")

        except Exception as e:
            print(f"General error: {e}")


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
                # File paths (replace with actual paths)
           

                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="PDF Missing",attachment_type=AttachmentType.PNG)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.live_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.pdfFile_path)
                            time.sleep(2)

                            # Optionally: Check for validation message on screen
                            msg = " PDF uploaded — expected to be rejected. Check UI validation."
                            print(msg)

                        except Exception as e:
                            msg = f" PDF rejected as expected: {e}"
                            print(msg)

                # Positive Test: Upload Image (should be accepted)
                    if not os.path.exists(self.imageFile_path_9_16):
                        msg = f" Image file not found: {self.imageFile_path_9_16}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.live_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.imageFile_path_9_16)
                            time.sleep(2)

                            msg = f" Image '{self.imageFile_path_9_16}' uploaded successfully."
                            print(msg)

                        except Exception as e:
                            msg = f" Error uploading image: {e}"
                            print(msg)

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
         # Player Image field
        try:
                # File paths (replace with actual paths)
                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.player_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            time.sleep(2)
                            upload_element.send_keys(self.pdfFile_path)
                            time.sleep(2)

                            # Optionally: Check for validation message on screen
                            msg = " PDF uploaded — expected to be rejected. Check UI validation."
                            print(msg)

                        except Exception as e:
                            msg = f" PDF rejected as expected: {e}"
                            print(msg)

                # Positive Test: Upload Image (should be accepted)
                    if not os.path.exists(self.imageFile1280_720_path):
                        msg = f" Image file not found: {self.imageFile1280_720_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.player_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.imageFile1280_720_path)
                            time.sleep(2)

                            msg = f" Image '{self.imageFile1280_720_path}' uploaded successfully."
                            print(msg)

                        except Exception as e:
                            msg = f" Error uploading image: {e}"
                            print(msg)

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        
        #Tv Image Module

        try:
                # File paths (replace with actual paths)
            
                   # Negative Test: Upload PDF (should be rejected)
                    if not os.path.exists(self.pdfFile_path):
                        msg = f" PDF file not found: {self.pdfFile_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.TV_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.pdfFile_path)
                            time.sleep(2)

                            # Optionally: Check for validation message on screen
                            msg = " PDF uploaded — expected to be rejected. Check UI validation."
                            print(msg)

                        except Exception as e:
                            msg = f" PDF rejected as expected: {e}"
                            print(msg)

                # Positive Test: Upload Image (should be accepted)
                    if not os.path.exists(self.imageFile1280_720_path):
                        msg = f" Image file not found: {self.imageFile1280_720_path}"
                        print(msg)
                    else:
                        try:
                            upload_element = WebDriverWait(self.driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, self.TV_image_element))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_element)
                            upload_element.send_keys(self.imageFile1280_720_path)
                            time.sleep(2)

                            msg = f" Image '{self.imageFile1280_720_path}' uploaded successfully."
                            print(msg)

                        except Exception as e:
                            msg = f" Error uploading image: {e}"
                            print(msg)

        except Exception as e:
                general_msg = f" General error in file upload process: {e}"
                print(general_msg)
        try:
            # Locate and scroll to the Live Source dropdown
            trailer_type = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.trailer_url_source_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trailer_type)

            # Select only embed_url from dropdown
            Select(trailer_type).select_by_value("embed_url")
            print("🔹 Selected Live Source: embed_url")
            time.sleep(2)

            # Enter the Embed URL
            
            _url_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.embed_url_element))
            )
            time.sleep(2)
            _url_input.clear()
            time.sleep(2)
            _url_input.send_keys(self.embed_url)
            print(f" Entered Embed URL: {self.embed_url}")
            time.sleep(2)

        except Exception as e:
            print(f" Error while setting embed URL: {e}")


        try:
            # Step 1: Leave Access Type empty and click Submit
            
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(1)
            submit_button.click()
            time.sleep(2)

            # Wait and capture validation error
            
            allure.attach(self.driver.get_screenshot_as_png(), name="AccessType_Missing_Error", attachment_type=AttachmentType.PNG)
    
            # Step 2: Now select valid Access Type
            ACCESS = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.access_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ACCESS)
            dropdown = Select(ACCESS)

            access_value = "registered"
            time.sleep(1)
            dropdown.select_by_value(access_value)
            print(f"Access type selected: {access_value}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name=f"Access_Selected_{access_value}", attachment_type=AttachmentType.PNG)

        except Exception as e:
            print(f"General error while handling Access dropdown: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="AccessDropdown_General_Error", attachment_type=AttachmentType.PNG)

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
          
                try:
                    # Locate the Website URL input
                    url_input = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, self.Website_Url_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url_input)
                    time.sleep(2)

                    # === NEGATIVE TEST: Enter invalid URL and submit ===
                    print("Negative Test: Entering invalid URL and submitting.")
                    url_input.clear()
                    url_input.send_keys("invalid-url")  # Invalid URL format
                    time.sleep(2)

                    # Click submit
                    submit_btn = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                    time.sleep(1)
                    submit_btn.click()
                    time.sleep(2)

                    # Attach screenshot for negative case
                    allure.attach(self.driver.get_screenshot_as_png(),
                                name="Negative_Invalid_Website_URL",
                                attachment_type=AttachmentType.PNG)

                    # Optionally scroll back to input
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url_input)
                    time.sleep(1)

                    # === POSITIVE TEST: Enter valid URL and submit ===
                    print("Positive Test: Entering valid URL and submitting.")
                    url_input.clear()
                    url_input.send_keys("https://chatgpt.com/")
                    time.sleep(2)

                    # Re-click submit
                    submit_btn = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                    time.sleep(1)
                    submit_btn.click()
                    time.sleep(2)

                    print("Form submitted with valid Website URL.")

                except Exception as e:
                    print(f"Error during Website URL test: {e}")
        

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
            # Tamil Subtitle - Negative (PDF) and Positive (VTT)
            tamizh = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.tamizh_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tamizh)
            time.sleep(1)
            tamizh.send_keys(self.pdfFile_path)
            print("Uploaded PDF for Tamil subtitle.")

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            submit_btn.click()
            print("Submitted with invalid Tamil subtitle.")

            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Tamil_Subtitle_Invalid", attachment_type=AttachmentType.PNG)

            # Tamil - Positive (VTT upload, no submit)
            tamizh = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.tamizh_subtitle_element))
            )
            tamizh.clear()
            time.sleep(1)
            tamizh.send_keys(self.vttfile_path)
            print("Uploaded VTT for Tamil subtitle.")

            # English Subtitle
            english = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.English_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", english)
            time.sleep(1)
            english.send_keys(self.pdfFile_path)
            print("Uploaded PDF for English subtitle.")

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            submit_btn.click()
            print("Submitted with invalid English subtitle.")

            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="English_Subtitle_Invalid", attachment_type=AttachmentType.PNG)

            english = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.English_subtitle_element))
            )
            english.clear()
            time.sleep(1)
            english.send_keys(self.vttfile_path)
            print("Uploaded VTT for English subtitle.")

            # Malayalam Subtitle
            malayalam = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.malayalam_subtitle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", malayalam)
            time.sleep(1)
            malayalam.send_keys(self.pdfFile_path)
            print("Uploaded PDF for Malayalam subtitle.")

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            submit_btn.click()
            print("Submitted with invalid Malayalam subtitle.")

            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Malayalam_Subtitle_Invalid", attachment_type=AttachmentType.PNG)

            malayalam = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.malayalam_subtitle_element))
            )
            malayalam.clear()
            time.sleep(1)
            malayalam.send_keys(self.vttfile_path)
            print("Uploaded VTT for Malayalam subtitle.")

        except Exception as e:
            print(f"General error during subtitle test: {e}")
        
        try:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All metadata was entered successfully while adding the livestream for the Regsister user",attachment_type=AttachmentType.PNG)
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print(" The Live stream was added successfully.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), "Live stream was added successfully And it was Redirected to  All live Page ",attachment_type=AttachmentType.PNG)
            time.sleep(6)
        except Exception as e:
            print(f" Error clicking submit button: {e}")    

        
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
               
                      
