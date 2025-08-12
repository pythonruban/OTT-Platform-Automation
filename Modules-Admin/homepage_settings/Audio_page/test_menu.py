import time
import allure
import pytest
import os

 
from conftest import *
from allure_commons.types import AttachmentType
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
 
from utilities.readProp import ReadConfig

 
@pytest.mark.usefixtures("browser_setup")
class TestAdd_Menu:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    home_element="//span[text()='Home Settings']"
    audio_element="//span[text()='AudioPage Settings']"

    enable_latest_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_genres_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_swriter_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"
    enable_basegenre_element="(//span[@class='admin-slider position-absolute admin-round '])[7]"
    enable_basealbum_element="(//span[@class='admin-slider position-absolute admin-round '])[9]"
    enable_replayed_element="(//span[@class='admin-slider position-absolute admin-round '])[11]"
    enable_mstation_element="(//span[@class='admin-slider position-absolute admin-round '])[13]"
    enable_playlist_element="(//span[@class='admin-slider position-absolute admin-round '])[15]"
    enable_basemusician_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_album_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_artist_element="(//span[@class='admin-slider position-absolute admin-round '])[6]"
    enable_musician_element="(//span[@class='admin-slider position-absolute admin-round '])[8]"
    enable_base_lang_element="(//span[@class='admin-slider position-absolute admin-round '])[10]"
    enable_vi_audios_element="(//span[@class='admin-slider position-absolute admin-round '])[12]"
    enable_songwriter_element="(//span[@class='admin-slider position-absolute admin-round '])[14]"

    update_element="//span[text()='Save Setting']"


    def test_Add_Menu(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        try:
            WebDriverWait(self.driver, 80).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e
        
           # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.home_element)))
        user = self.driver.find_element(By.XPATH, self.home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.audio_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()




        try:
            toggle1 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.enable_latest_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle1).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle2 = self.driver.find_element(By.XPATH, self.enable_genres_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle2).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle3 = self.driver.find_element(By.XPATH, self.enable_swriter_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle3).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle4 = self.driver.find_element(By.XPATH, self.enable_basegenre_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle4).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle5 = self.driver.find_element(By.XPATH, self.enable_basealbum_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle5).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle6 = self.driver.find_element(By.XPATH, self.enable_replayed_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle6).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle7 = self.driver.find_element(By.XPATH, self.enable_mstation_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle7)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle7).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle8 = self.driver.find_element(By.XPATH, self.enable_playlist_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle8)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle8).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle9 = self.driver.find_element(By.XPATH, self.enable_basemusician_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle9)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle9).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle10 = self.driver.find_element(By.XPATH, self.enable_album_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle10)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle10).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle11 = self.driver.find_element(By.XPATH, self.enable_artist_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle11)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle11).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle12 = self.driver.find_element(By.XPATH, self.enable_musician_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle12)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle12).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle13 = self.driver.find_element(By.XPATH, self.enable_base_lang_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle13)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle13).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle14 = self.driver.find_element(By.XPATH, self.enable_vi_audios_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle14)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle14).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle15 = self.driver.find_element(By.XPATH, self.enable_songwriter_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle15)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle15).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))            


        
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Menu Settings in audio page details Added successfully.", attachment_type=AttachmentType.PNG)
    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
        


