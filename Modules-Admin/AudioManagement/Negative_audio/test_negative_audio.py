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

    audio_upload_element = "//input[@value='mp3_audio_upload']" 
    audio_field_element = "//input[@type='file' and @accept='audio/*']"
    up_arrow_element = "(//button[@type='button' and contains(@class, 'bg-transparent') and contains(@class, 'p-0')])[2]"
    audio_upload_url_element = "//input[@value='mp3_url']" 
    audio_field_url_element = "//input[@type='text' and @name='mp3_url']"
    submit_url_elemnt="//button[@id='audio-submit-mp3-url']"
    audio_upload_live_element = "//input[@value='mp3_live_url']" 
    audio_field_live_element = "//input[@type='text' and @name='mp3_live_url']"
    submit_live_elemnt="//button[@id='audio-mp3-live-url']"
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
    


    def test_negative_audio(self,browser_setup):
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

        try:
            # Step 1: Select "Audio URL" radio button
            audio_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.audio_upload_url_element))
            )
            audio_radio.click()
            print("Selected Audio URL option")

            # Step 2: Enter invalid audio URL (.mp4)
            audio_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_field_url_element))
            )
            audio_input.clear()
            audio_input.send_keys("https://example.com/invalid_audio.mp4")
            print("Entered invalid Audio URL (.mp4)")

            proceed_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_url_elemnt))
            )
            proceed_button.click()
            print("Clicked proceed with invalid audio URL")
            time.sleep(2)

            # Allure screenshot for invalid Audio URL
            allure.attach(self.driver.get_screenshot_as_png(), name="Invalid_Audio_URL", attachment_type=allure.attachment_type.PNG)

            # Step 3: Re-locate and enter valid audio URL (.mp3)
            audio_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_field_url_element))
            )
            audio_input.clear()
            audio_input.send_keys("https://onlinetestcase.com/wp-content/uploads/2023/06/10-MB-MP3.mp3")
            print("Entered valid Audio URL (.mp3)")

            proceed_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_url_elemnt))
            )
            proceed_button.click()
            print("Proceeded with valid audio URL")
            time.sleep(2)

            # Step 4: Select "Live URL" radio button
            live_radio = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.audio_upload_live_element))
            )
            live_radio.click()
            print("Selected Live URL option")

            # Step 5: Enter invalid live URL (.mp4)
            live_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_field_live_element))
            )
            live_input.clear()
            live_input.send_keys("https://example.com/invalid_live.mp4")
            print("Entered invalid Live URL (.mp4)")

            proceed_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_live_elemnt))
            )
            proceed_button.click()
            print("Clicked proceed with invalid live URL")
            time.sleep(2)

            # Allure screenshot for invalid Live URL
            allure.attach(self.driver.get_screenshot_as_png(), name="Invalid_Live_URL", attachment_type=allure.attachment_type.PNG)

            # Step 6: Re-locate and enter valid live URL (.m3u8)
            live_input = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.audio_field_live_element))
            )
            live_input.clear()
            live_input.send_keys("https://onlinetestcase.com/wp-content/uploads/2023/06/10-MB-MP3.mp3")
            print("Entered valid Live URL (.m3u8)")

            proceed_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_live_elemnt))
            )
            proceed_button.click()
            print("Proceeded with valid live URL")

            # Step 7: Final proceed button (if any confirmation step)
           

            proceed_next = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.upload_next_element))
            )
            proceed_next.click()
            print("Clicked next to continue to upload confirmation")

        except Exception as e:
            print(f" Failed during Audio/Live URL input flow: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="Unexpected_Failure", attachment_type=allure.attachment_type.PNG)


        try:
            test_data = [
                ("Test 1: 1-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase, k=1))),
                ("Test 2: 102-char (Negative Title)", ''.join(random.choices(string.ascii_uppercase + string.digits, k=102))),
                ("Test 3: Auto Title (Valid)", ''.join(random.choices(string.ascii_uppercase, k=random.randint(5, 7))))
            ]

            for test_name, title_value in test_data:
                print(f"\n{test_name} started")

                # === TITLE FIELD ===
                try:
                    title_input = WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, self.title_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(title_value)
                    print(f"Title entered: {title_value[:30]}")

                    if len(title_value) < 3 or len(title_value) > 100:
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Negative_Title_Length_{len(title_value)}",
                            attachment_type=allure.attachment_type.PNG
                        )
                except Exception as title_error:
                    print(f"Error entering title: {title_error}")
                    continue

                # === SLUG FIELD ===
                try:
                    slug_input = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, self.slug_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                    time.sleep(1)
                    slug_input.clear()
                    slug_input.send_keys(title_value)
                    print(f"Slug entered: {title_value[:30]}")

                    if len(title_value) < 3 or len(title_value) > 100:
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Negative_Slug_Length_{len(title_value)}",
                            attachment_type=allure.attachment_type.PNG
                        )
                except Exception as slug_error:
                    print(f"Error entering slug: {slug_error}")
                    continue

                # === SUBMIT FORM ===
                try:
                    submit_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, self.add_album_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    time.sleep(1)
                    submit_button.click()
                    time.sleep(2)
                    print(f"Form submitted for: {test_name}")
                except Exception as submit_error:
                    print(f"Error during form submission: {submit_error}")

        except Exception as outer_error:
            print(f" Outer script failure: {outer_error}")


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
                print(" Could not attach error screenshot.")\
                              
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
            Album = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.album_element))
            )
            Select(Album).select_by_value("1")
            time.sleep(2)
        except Exception as e:
            print(f" Error while selecting artist(s): {e}")

                
        try:
            duration_inputs = ["00:00:00", "24:00:00", "01:45:33"]
            pattern = r"^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$"
            max_allowed_seconds = 24 * 3600 + 24 * 60 + 24  # 24h 24m 24s

            for duration_input in duration_inputs:
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

                            # Scroll back to field after submit
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", duration_field)
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
            # ===== STEP 1: Submit with no source & no URL =====
            print("Step 1: Submit without selecting source or entering URL.")
            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step1_NoSource_NoURL", attachment_type=AttachmentType.PNG)

            # ===== STEP 2: Select source only =====
            print("Step 2: Select 'embed_url' without URL.")
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            Select(dropdown).select_by_value("embed_url")
            time.sleep(1)

            # Click submit again
            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step2_SourceSelected_NoURL", attachment_type=AttachmentType.PNG)

            # ===== STEP 3: Provide valid embed URL =====
            print("Step 3: Enter valid embed URL.")
            url_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.live_url_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url_input)
            url_input.clear()
            url_input.send_keys(self.embed_url)
            time.sleep(1)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            print("Submitted with valid embed URL.")
            allure.attach(self.driver.get_screenshot_as_png(), name="Step3_ValidEmbedURL", attachment_type=AttachmentType.PNG)
            time.sleep(2)

            # ===== STEP 4: Select MP4 source but no file (NEGATIVE) =====
            print("Step 4: Select MP4 source without uploading file.")
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            Select(dropdown).select_by_value("mp4_video_upload")
            time.sleep(1)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step4_MP4_NoFile", attachment_type=AttachmentType.PNG)

            # ===== STEP 5: Select MP4 source and upload file (POSITIVE) =====
            print("Step 5: Upload MP4 file and submit.")
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            Select(dropdown).select_by_value("mp4_video_upload")
            time.sleep(1)

            upload_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.Live_source_element))
            )
            upload_input.send_keys(self.videoFile_path)
            print("Uploaded MP4 file.")
            time.sleep(2)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step5_MP4_FileUploaded", attachment_type=AttachmentType.PNG)
            print("MP4 file submitted successfully.")

        except Exception as e:
            error_message = f"Exception during test flow: {e}"
            print(error_message)
            allure.attach(error_message, name="FatalError", attachment_type=AttachmentType.TEXT)
            allure.attach(self.driver.get_screenshot_as_png(), name="FatalErrorScreenshot", attachment_type=AttachmentType.PNG)

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

        try:
            visibility = self.driver.find_element(By.XPATH, self.visibility_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", visibility)
            time.sleep(1)
            visibility.click()
            time.sleep(1)
            print(" Visibility toggled.")
            year = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.year_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", year)
            Select(year).select_by_value("2025")
            time.sleep(3)
            print(" Year selected: 2025")
        except Exception as e:
            print(f" Error toggling visibility: {e}")
                    
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
        try:
            print(" Checking 'Active' toggle state...")
            Active = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.active_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Active)
            time.sleep(1)
            active_class = Active.get_attribute("class")
            if "active"  in active_class.lower():
                 print(" 'Active' toggle already ON. Skipped.")
            else:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, self.active_element))
                )
                self.driver.execute_script("arguments[0].click();", Active)
                print(" 'Active' toggle was OFF, now turned ON.")
               
        except Exception as e:
            print(f" Error handling 'Active' toggle: {e}")
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

      
    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
        


        

        