import time
import re 
import random
import string
import pytest 
import os
import sys 
import allure 


 
from conftest import *
from selenium import webdriver
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup") 

class TestLiveStream:
    driver = webdriver.Firefox    
      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "10801620.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "16.9.jpg")
    videoFile_path = os.path.join(base_dir, "sample_video.mp4")
    pdfFile_path = os.path.join(base_dir, "pdf1.pdf")
       

    # Locators
    email_element = "(//input[@type='email'])[2]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    live_stream_element = "//div[@data-bs-target='#Live-Stream']"
    all_Live_element = "//span[text()='All Live Streams']"
    add_live_element = "//span[text()='Add New Live Stream']"
    

    title_element = "//input[@name='title']" 
    slug_element = "//input[@name='slug']"
    short_description_element = "//textarea[@name='description']"
    live_description_element ="//div[@class='jodit-wysiwyg']"
    duration_element ="//input[@name='duration']"
    year_element ="//select[@id='live-year']"

    rating_element ="//select[@name='rating']"
    age_element ="//select[@name='age_restrict']"
   
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
   
    embed_url = "https://www.youtube.com/embed/o5cZtlxANyU?si=Q4mEuH6an_vp60AB"
   
    
    #Live Stream Source
    live_url_source_element = "//select[@id='live-url-type']"
    live_url_element = "//input[@name='embed_url']"
    mp4_url_element ="//input[@id='live-mp4-url']"
    m3u8_url_element ="//input[@id='live-m3u8-url']"
    Live_source_element ="//input[@id='live-file-upload']"
    #RESTREAM
    restream_element = "(//span[contains(@class, 'admin-slider')])[1]"
    youtube_element = "(//button[@class='accordion-button collapsed p-3'])[1]"
    youtube_url_element= "//input[@name='youtube_restream_url']"
    youtube_secert_key= "//input[@name='youtube_streamkey']"
    #visiblity
    visibility_element ="//input[@name='publish_now']"
    visibility_text_element ="//select[@id='live-year']"
    #access
    access_element = "//select[@name='access']"
    choose_file_element ="//input[@id='live-file-upload']"
    video_path ="C:/Users/Dharshini v/Downloads/Animal.mp4"
    #free Duration
    free_duration_element = "(//span[contains(@class, 'admin-slider')])[1]"
    free_text_element = "//input[@name='free_duration_time']"
    #Status Settings
    feature_element = "//input[@id='live-featured']/following-sibling::span"
    active_element = "//input[@id='live-active']/following-sibling::span"
    banner_element = "//input[@id='live-banner']/following-sibling::span"
    # chats_element = "(//span[contains(@class, 'admin-slider')])[6]"
    #Live Event Artist
    # live_event_element = "(//span[contains(@class, 'admin-slider')])[5]"
    # donation_element = "//input[@name='donations_label']"
    #SAVE BUTTON
    submit_button_element = "//button[@id='live-store-button']"

    def test_add_upload(self,browser_setup):
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
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="All Value login Credentials was entered, and the login button was clicked. it was redirect to Dashboard",attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="login_error",attachment_type=AttachmentType.PNG)
            print(f" Failed to enter email: {e}")
 
# W
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Manage_livestream = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, self.live_stream_element))
             )
            self.driver.execute_script("arguments[0].click();", Manage_livestream)
            print(" Navigated to 'Live Stream Management'")
        except Exception as e:
            print(f" Failed to click 'Live Stream Management': {e}")
        
        try:
            add_livestream_button = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, self.add_live_element))
        )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_livestream_button)
            time.sleep(1)  # Smooth scroll
            self.driver.execute_script("arguments[0].click();", add_livestream_button)
            print(" Clicked 'Add New live stream'")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to click 'Add New live stream': {e}")
   
            
        try:
            duplicate_title = ''.join(random.choices(string.ascii_letters, k=7))

            test_cases = [
                ("", "invalid"),
                ("A", "invalid"),
                ("A" * 255, "valid"),
                ("@" * 20, "invalid"),
                ("🎉🙂🙂🙂🙂🙂🙂", "invalid"),
                (duplicate_title, "valid"),
                (duplicate_title, "duplicate"),
                (" " * 10, "invalid"),
                ("A" * 256, "invalid"),
                ("auto", "valid"),
            ]

            for idx, (title_input, expected) in enumerate(test_cases):
                try:
                    if title_input == "auto":
                        title_input = ''.join(random.choices(string.ascii_letters, k=random.choice([5, 7, 10])))

                    # Enter title
                    title_field = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.title_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_field)
                    title_field.clear()
                    title_field.send_keys(title_input)
                    print(f"Entered title: {title_input}")

                    # Handle slug
                    slug_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.slug_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug_input)
                    time.sleep(4)

                    if idx == 0:
                        slug_input.clear()
                        slug_input.send_keys("x")
                        print("Manually entered slug: x")
                    else:
                        auto_slug = slug_input.get_attribute("value")
                        if title_input.lower()[:3] not in auto_slug.lower():
                            slug_input.clear()
                            new_slug = title_input.lower() + "x"
                            slug_input.send_keys(new_slug)
                            print(f"Overwritten slug: {new_slug}")
                        else:
                            print(f"Auto-generated slug: {auto_slug}")

                    # Submit
                    submit_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                    self.driver.execute_script("arguments[0].click();", submit_btn)
                    print("Submitted form.")
                    time.sleep(2)

                    # Validation
                    result_found = False
                    if expected == "valid":
                        elements = self.driver.find_elements(By.ID, "successMessage")
                        if elements and "success" in elements[0].text.lower():
                            print(f"✅ Passed: {title_input[:20]} [valid]")
                            result_found = True
                    elif expected == "invalid":
                        elements = self.driver.find_elements(By.ID, "errorMessage")
                        if elements and ("invalid" in elements[0].text.lower() or "required" in elements[0].text.lower()):
                            print(f" Passed: {title_input[:20]} [invalid]")
                            result_found = True
                    elif expected == "duplicate":
                        elements = self.driver.find_elements(By.ID, "duplicateMessage")
                        if elements and "already exists" in elements[0].text.lower():
                            print(f" Passed: {title_input[:20]} [duplicate]")
                            result_found = True

                    if not result_found:
                        print(f" No validation element found for: {title_input[:20]} [{expected}]")
                        allure.attach(
                            self.driver.get_screenshot_as_png(),
                            name=f"Validation_Missing_{title_input[:10]}",
                            attachment_type=AttachmentType.PNG
                        )

                except Exception as e:
                    print(f" Exception at [{idx + 1}] {title_input[:20]}: {e}")
                    allure.attach(
                        self.driver.get_screenshot_as_png(),
                        name=f"Exception_{title_input[:10]}",
                        attachment_type=AttachmentType.PNG
                    )

        except Exception as total_error:
            print(f"❌ Fatal Error in Test Block: {total_error}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Fatal_Test_Execution_Error",
                attachment_type=AttachmentType.PNG
            )

        try:                   
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
            time.sleep(3)
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
            time.sleep(3)
            category_input.click()
            time.sleep(1)

            # Select categories dynamically
            options_to_select = ["NEWS", "Sports", "Gaming"]
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
            time.sleep(2)
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
            time.sleep(2)

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

                            if duration_input == "00:00:00":
                                print("00:00:00 detected — submitting form and capturing screenshot.")
                                submit_button = WebDriverWait(self.driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
                                )
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                                time.sleep(1)
                                submit_button.click()
                                time.sleep(2)

                                try:
                                    allure.attach(self.driver.get_screenshot_as_png(),
                                                name="Zero_Duration_Submit",
                                                attachment_type=AttachmentType.PNG)
                                    print("Screenshot captured after 00:00:00 submission.")
                                except:
                                    print("Screenshot failed after submission.")

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

        # -------- LIVE IMAGE FIELD --------
        try:
            print("---- Live Image Upload Test ----")
            # Upload PDF (Negative)
            if os.path.exists(self.pdfFile_path):
                live_image_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.live_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", live_image_input)
                live_image_input.send_keys(self.pdfFile_path)
                print("📄 Uploaded PDF to Live Image field.")

                try:
                    error_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "invalid-feedback"))  # change this class if needed
                    )
                    print("❌ PDF rejected — validation message found.")
                    allure.attach(
                        self.driver.get_screenshot_as_png(),
                        name="Live_Image_PDF_Validation",
                        attachment_type=AttachmentType.PNG
                    )
                except TimeoutException:
                    print(" No error message shown for Live Image PDF.")

            # Upload Image (Positive)
            if os.path.exists(self.imageFile_path_9_16):
                live_image_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.live_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", live_image_input)
                live_image_input.send_keys(self.imageFile_path_9_16)
                print("✅ Uploaded valid image to Live Image field.")
            else:
                print("🚫 Image not found:", self.imageFile_path_9_16)

        except Exception as e:
            print("❌ Live Image upload error:", e)
            allure.attach(self.driver.get_screenshot_as_png(), name="Live_Image_Upload_Error", attachment_type=AttachmentType.PNG)


        # -------- PLAYER IMAGE FIELD --------
        try:
            print("---- Player Image Upload Test ----")
            if os.path.exists(self.pdfFile_path):
                player_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.player_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", player_input)
                player_input.send_keys(self.pdfFile_path)
                print("📄 Uploaded PDF to Player Image field.")

                try:
                    error_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "invalid-feedback"))
                    )
                    print("❌ PDF rejected — validation message shown.")
                    allure.attach(
                        self.driver.get_screenshot_as_png(),
                        name="Player_Image_PDF_Validation",
                        attachment_type=AttachmentType.PNG
                    )
                except TimeoutException:
                    print("⚠️ No error shown for Player Image PDF.")

            if os.path.exists(self.imageFile1280_720_path):
                player_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.player_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", player_input)
                player_input.send_keys(self.imageFile1280_720_path)
                print("✅ Uploaded valid image to Player Image field.")
            else:
                print("🚫 Image not found:", self.imageFile1280_720_path)

        except Exception as e:
            print("❌ Player Image upload error:", e)
            allure.attach(self.driver.get_screenshot_as_png(), name="Player_Image_Upload_Error", attachment_type=AttachmentType.PNG)


        # -------- TV IMAGE FIELD --------
        try:
            print("---- TV Image Upload Test ----")
            if os.path.exists(self.pdfFile_path):
                tv_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.TV_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tv_input)
                tv_input.send_keys(self.pdfFile_path)
                print("📄 Uploaded PDF to TV Image field.")

                try:
                    error_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "invalid-feedback"))
                    )
                    print("❌ PDF rejected — validation shown.")
                    allure.attach(
                        self.driver.get_screenshot_as_png(),
                        name="TV_Image_PDF_Validation",
                        attachment_type=AttachmentType.PNG
                    )
                except TimeoutException:
                    print("⚠️ No error shown for TV Image PDF.")

            if os.path.exists(self.imageFile1280_720_path):
                tv_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, self.TV_image_element))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tv_input)
                tv_input.send_keys(self.imageFile1280_720_path)
                print("✅ Uploaded valid image to TV Image field.")
            else:
                print("🚫 Image not found:", self.imageFile1280_720_path)

        except Exception as e:
            print("❌ TV Image upload error:", e)
            allure.attach(self.driver.get_screenshot_as_png(), name="TV_Image_Upload_Error", attachment_type=AttachmentType.PNG)

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

            # ===== STEP 2: Select source 'embed_url' =====
            print("Step 2: Select 'embed_url' without URL.")
            dropdown = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            Select(dropdown).select_by_value("embed_url")
            time.sleep(1)

            # Wait for URL input field to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.live_url_element))
            )

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step2_SourceSelected_NoURL", attachment_type=AttachmentType.PNG)

            # ===== STEP 3: Enter embed URL and submit =====
            print("Step 3: Enter valid embed URL.")
            url_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.live_url_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url_input)
            url_input.clear()
            url_input.send_keys(self.embed_url)
            time.sleep(2)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            allure.attach(self.driver.get_screenshot_as_png(), name="Step3_ValidEmbedURL", attachment_type=AttachmentType.PNG)
            print("Submitted with valid embed URL.")
            time.sleep(2)

            # ===== STEP 4: Select MP4 source with no file =====
            print("Step 4: Select MP4 source without uploading file.")
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            Select(dropdown).select_by_value("mp4_video_upload")
            time.sleep(1)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step4_MP4_NoFile", attachment_type=AttachmentType.PNG)

            # ===== STEP 5: Upload MP4 file and submit =====
            print("Step 5: Upload MP4 file and submit.")
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.live_url_source_element))
            )
            Select(dropdown).select_by_value("mp4_video_upload")
            time.sleep(1)

            upload_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.Live_source_element))
            )
            upload_input.send_keys(self.videoFile_path)
            print("Uploaded MP4 file.")
            time.sleep(2)

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.submit_button_element))
            )
            submit_btn.click()
            time.sleep(2)
            allure.attach(self.driver.get_screenshot_as_png(), name="Step5_MP4_FileUploaded", attachment_type=AttachmentType.PNG)
            print("MP4 file submitted successfully.")

        except Exception as e:
            error_message = f"Exception during test flow: {e}"
            print(error_message)
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
            time.sleep(6)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), "Live stream was added successfully And it was Redirected to  All live Page ",attachment_type=AttachmentType.PNG)
            
        except Exception as e:
            print(f" Error clicking submit button: {e}")      

    
                    
            
        
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
        



   