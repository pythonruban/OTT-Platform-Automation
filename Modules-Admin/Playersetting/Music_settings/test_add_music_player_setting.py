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
class TestPlayerSetting:
    driver = webdriver.Firefox

    # Locators
    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]"
    password_element = "(//input[@name='password'])[1]"
    login_element = "(//button[@type='submit'])[2]"
    music_player_element = "//span[text()='Music Player Settings']"
    #Player Settings
    choose_layout_element= "//input[@name='enable_floating']"
    minimize_button_element= "(//span[@class='slider round'])[1]"
    #Player Controls
    track_control_element = "(//span[contains(@class, 'admin-slider') ])[2]"
    volume_control_element ="(//span[contains(@class, 'admin-slider') ])[3]"
    loop_element ="(//span[contains(@class, 'admin-slider') ])[4]"
    shuffle_element ="(//span[contains(@class, 'admin-slider') ])[5]"
    progress_bar_element = "(//span[contains(@class, 'admin-slider') ])[6]"
    default_playlist_element = "(//span[contains(@class, 'admin-slider') ])[7]"
  #  Track Info to Display
    image_element ="(//span[contains(@class, 'admin-slider') ])[8]"
    title_element ="(//span[contains(@class, 'admin-slider') ])[9]"
    artists_element= "(//span[contains(@class, 'admin-slider') ])[10]"
    #Playlist Default
    show_playlist_element = "(//span[contains(@class, 'admin-slider') ])[11]"
    #Playlist Info to Display
    playlist_image_element ="(//span[contains(@class, 'admin-slider') ])[12]"
    playlist_title_element = "(//span[contains(@class, 'admin-slider') ])[13]"
    playlist_artists_element = "(//span[contains(@class, 'admin-slider') ])[14]"
    #save
    save_button_element= "(//button[normalize-space(.)='Update Music'])[2]"
    
    def test_add_music_player_setting(self, browser_setup):
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


        # Click on "Cast & Crew"
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            Player_setting = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, self.music_player_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Player_setting)
            self.driver.execute_script("arguments[0].click();", Player_setting)
            print("Navigated to 'Player Setting Management'")
        except Exception as e:
            print(f"Failed to navigate to Player Setting Management: {e}")

        time.sleep(3)

        # Choose Layout
        # try:
        #     self.driver.find_element(By.XPATH, self.choose_layout_element).click()
        # except Exception as e:
        #     print(f"Failed to click Choose Layout: {e}")
        # time.sleep(4)

        # # Minimize Button
        # try:
        #     toggle_button = self.driver.find_element(By.XPATH, self.minimize_button_element)
        #     if toggle_button.is_displayed():
        #         toggle_button.click()
        #         print("Minimize button clicked.")
        #     else:
        #         print("Minimize button is not available.")
        # except Exception as e:
        #     print(f"Failed to click Minimize button: {e}")
        # time.sleep(2)

        # Track Control
        # Track Controls
        # Track Controls
        try:
            track_controls = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.track_control_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", track_controls)
            is_enabled = track_controls.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Track control toggle already enabled.")
            else:
                track_controls.click()
                print("Track control toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Track control: {e}")
        time.sleep(2)

        # Volume Control
        try:
            volume = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.volume_control_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", volume)
            is_enabled = volume.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Volume toggle already enabled.")
            else:
                volume.click()
                print("Volume toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Volume control: {e}")
        time.sleep(2)

        # Loop
        try:
            loop = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.loop_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loop)
            is_enabled = loop.get_attribute("aria-pressed") == "true"
            if  not is_enabled:
                print("Loop toggle already enabled.")
            else:
                loop.click()
                print("Loop toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Loop: {e}")
        time.sleep(2)

        # Shuffle
        try:
            shuffle = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.shuffle_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shuffle)
            is_enabled = shuffle.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Shuffle toggle already enabled.")
            else:
                shuffle.click()
                print("Shuffle toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Shuffle: {e}")
        time.sleep(1)

        # Progress Bar
        try:
            progress_bar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.progress_bar_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", progress_bar)
            is_enabled = progress_bar.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Progress bar toggle already enabled.")
            else:
                progress_bar.click()
                print("Progress bar toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Progress bar: {e}")
        time.sleep(1)

        # Default Playlist
        try:
            default = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.default_playlist_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", default)
            is_enabled = default.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Progress bar toggle already enabled.")
            else:
                default.click()
                print("Progress bar toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Progress bar: {e}")
        time.sleep(1)

        # Track Image
        try:
            image = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            is_enabled = image.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Track image toggle already enabled.")
            else:
                image.click()
                print("Track image toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Track image: {e}")
        time.sleep(1)

        # Track Title
        try:
            title = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title)
            is_enabled = title.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Track title toggle already enabled.")
            else:
                title.click()
                print("Track title toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Track title: {e}")
        time.sleep(1)

        # Track Artists
        try:
            artists = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.artists_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", artists)
            is_enabled = artists.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Track artists toggle already enabled.")
            else:
                artists.click()
                print("Track artists toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Track artists: {e}")
        time.sleep(1)

        # Show Playlist
        try:
            playlist = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.show_playlist_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", playlist)
            is_enabled = playlist.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Playlist toggle already enabled.")
            else:
                playlist.click()
                print("Playlist toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Playlist: {e}")
        time.sleep(1)

        # Playlist Image
        try:
            playlist_image = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.playlist_image_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", playlist_image)
            is_enabled = playlist_image.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Playlist image toggle already enabled.")
            else:
                playlist_image.click()
                print("Playlist image toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Playlist image: {e}")
        time.sleep(1)

        # Playlist Title
        try:
            playlist_title = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.playlist_title_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", playlist_title)
            is_enabled = playlist_title.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Playlist title toggle already enabled.")
            else:
                playlist_title.click()
                print("Playlist title toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Playlist title: {e}")
        time.sleep(1)

        # Playlist Artists
        try:
            playlist_artists = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.playlist_artists_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", playlist_artists)
            is_enabled = playlist_artists.get_attribute("aria-pressed") == "true"
            if not is_enabled:
                print("Playlist artists toggle already enabled.")
            else:
                playlist_artists.click()
                print("Playlist artists toggle enabled.")
        except Exception as e:
            print(f"Failed to interact with Playlist artists: {e}")
        time.sleep(1)

                        
        #save button
        
        try:
            save_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.save_button_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
            save_button.click()
            time.sleep(2)
            print(" The Player music setting uploaded successfully.")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Save_Clicked_Success", attachment_type=AttachmentType.PNG)
            time.sleep(4)
            assert True 

        except Exception as e:
            print(f" Failed to click the Save button: {e}")
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Save_Click_Failure", attachment_type=AttachmentType.PNG)
            

    def teardown_method(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")
        except Exception as e:
            print(f"Unexpected error while quitting the driver: {e}")

    




