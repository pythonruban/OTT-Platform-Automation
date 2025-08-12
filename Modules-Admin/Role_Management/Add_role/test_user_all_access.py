import time
import allure
import pytest
import os
import random
import string
 
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
class TestUser_Access:
   
    driver: WebDriver


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    roles_element="//span[text()='Roles']"
    add_role_element="(//span[text()='Add Role'])[1]"

    name_element="//input[@id='inputField']"
    role_type_element="(//select[@id='selectField'])[1]"
    access_type_element="(//select[@id='selectField'])[2]"

    dash_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    master_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    video_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    series_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    live_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"
    audio_element="(//span[@class='admin-slider position-absolute admin-round '])[6]"
    artist_element="(//span[@class='admin-slider position-absolute admin-round '])[7]"
    user_element="(//span[@class='admin-slider position-absolute admin-round '])[8]"
    language_element="(//span[@class='admin-slider position-absolute admin-round '])[9]"
    slider_element="(//span[@class='admin-slider position-absolute admin-round '])[10]"
    player_element="(//span[@class='admin-slider position-absolute admin-round '])[11]"
    partner_element="(//span[@class='admin-slider position-absolute admin-round '])[12]"
    page_element="(//span[@class='admin-slider position-absolute admin-round '])[13]"
    plans_element="(//span[@class='admin-slider position-absolute admin-round '])[14]"
    payment_element="(//span[@class='admin-slider position-absolute admin-round '])[15]"
    analytics_element="(//span[@class='admin-slider position-absolute admin-round '])[16]"
    settings_element="(//span[@class='admin-slider position-absolute admin-round '])[17]"
    ads_element="(//span[@class='admin-slider position-absolute admin-round '])[18]"
    contact_element="(//span[@class='admin-slider position-absolute admin-round '])[19]"
    logs_element="(//span[@class='admin-slider position-absolute admin-round '])[20]"
    menu_element="(//span[@class='admin-slider position-absolute admin-round '])[21]"
    store_element="(//span[@class='admin-slider position-absolute admin-round '])[22]"
    home_element="(//span[@class='admin-slider position-absolute admin-round '])[23]"
    app_element="(//span[@class='admin-slider position-absolute admin-round '])[24]"
    meta_element="(//span[@class='admin-slider position-absolute admin-round '])[25]"
    rol_element="(//span[@class='admin-slider position-absolute admin-round '])[26]"
    registration_element="(//span[@class='admin-slider position-absolute admin-round '])[28]"
    playout_element="(//span[@class='admin-slider position-absolute admin-round '])[29]"
    category_element="(//span[@class='admin-slider position-absolute admin-round '])[30]"
    playlist_element="(//span[@class='admin-slider position-absolute admin-round '])[31]"
    Live_category_element="(//span[@class='admin-slider position-absolute admin-round '])[32]"
    audio_category_element="(//span[@class='admin-slider position-absolute admin-round '])[33]"
    audio_album_element="(//span[@class='admin-slider position-absolute admin-round '])[34]"
    import_element="(//span[@class='admin-slider position-absolute admin-round '])[35]"
    super_element="(//span[@class='admin-slider position-absolute admin-round '])[36]"

    submit_element="(//span[text()='Add Role'])[2]"



    def test_User_Access(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.roles_element)))
        user = self.driver.find_element(By.XPATH, self.roles_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_role_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try :
            length= 6 
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.name_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.name_element))
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
        
        

        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.role_type_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("User Permission")

        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.access_type_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        # time.sleep(2)
        # drop_down1.click()
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("All Access")
        time.sleep(3)

        toggle1 = self.driver.find_element(By.XPATH, self.dash_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.master_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)

        toggle3 = self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle3)
        time.sleep(2)

        toggle4 = self.driver.find_element(By.XPATH, self.series_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle4)
        time.sleep(2)

        toggle5 = self.driver.find_element(By.XPATH, self.live_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle5)
        time.sleep(2)

        toggle6 = self.driver.find_element(By.XPATH, self.audio_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle6)
        time.sleep(2)

        toggle7 = self.driver.find_element(By.XPATH, self.artist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle7) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle7)
        time.sleep(2)

        toggle8 = self.driver.find_element(By.XPATH, self.user_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle8) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle8)
        time.sleep(2)

        toggle9 = self.driver.find_element(By.XPATH, self.language_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle9) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle9)
        time.sleep(2)

        toggle10 = self.driver.find_element(By.XPATH, self.slider_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle10) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle10)
        time.sleep(2)

        toggle11 = self.driver.find_element(By.XPATH, self.player_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle11) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle11)
        time.sleep(2)

        toggle12 = self.driver.find_element(By.XPATH, self.partner_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle12) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle12)
        time.sleep(2)

        toggle13 = self.driver.find_element(By.XPATH, self.page_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle13) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle13)
        time.sleep(2)

        toggle14 = self.driver.find_element(By.XPATH, self.plans_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle14) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle14)
        time.sleep(2)

        toggle15 = self.driver.find_element(By.XPATH, self.payment_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle15) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle15)
        time.sleep(2)

        toggle16 = self.driver.find_element(By.XPATH, self.analytics_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle16) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle16)
        time.sleep(2)

        toggle17 = self.driver.find_element(By.XPATH, self.settings_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle17) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle17)
        time.sleep(2)

        toggle18 = self.driver.find_element(By.XPATH, self.ads_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle18) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle18)
        time.sleep(2)

        toggle19 = self.driver.find_element(By.XPATH, self.contact_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle19) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle19)
        time.sleep(2)

        toggle20 = self.driver.find_element(By.XPATH, self.logs_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle20) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle20)
        time.sleep(2)

        toggle21 = self.driver.find_element(By.XPATH, self.menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle21) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle21)
        time.sleep(2)

        toggle22 = self.driver.find_element(By.XPATH, self.store_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle22) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle22)
        time.sleep(2)

        toggle23 = self.driver.find_element(By.XPATH, self.home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle23) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle23)
        time.sleep(2)

        toggle24 = self.driver.find_element(By.XPATH, self.app_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle24) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle24)
        time.sleep(2)

        toggle25 = self.driver.find_element(By.XPATH, self.meta_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle25) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle25)
        time.sleep(2)

        toggle26 = self.driver.find_element(By.XPATH, self.rol_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle26) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle26)
        time.sleep(2)

        toggle27 = self.driver.find_element(By.XPATH, self.registration_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle27) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle27)
        time.sleep(2)

        toggle28 = self.driver.find_element(By.XPATH, self.playout_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle28) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle28)
        time.sleep(2)

        toggle29 = self.driver.find_element(By.XPATH, self.category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle29) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle29)
        time.sleep(2)

        toggle30 = self.driver.find_element(By.XPATH, self.playlist_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle30) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle30)
        time.sleep(2)

        toggle31 = self.driver.find_element(By.XPATH, self.Live_category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle31) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle31)
        time.sleep(2)

        toggle32 = self.driver.find_element(By.XPATH, self.audio_category_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle32) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle32)
        time.sleep(2)

        toggle33 = self.driver.find_element(By.XPATH, self.audio_album_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle33) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle33)
        time.sleep(2)

        toggle34 = self.driver.find_element(By.XPATH, self.import_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle34) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle34)
        time.sleep(2)
        
        toggle35 = self.driver.find_element(By.XPATH, self.super_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle35) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle35)
        time.sleep(2)

          # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="User permission all access details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




























