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
class TestAddGuest:
   
    driver: WebDriver

       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "916.jpg")
    image_path_2 = os.path.join(base_dir, "1691.jpg")
    image_path_3 =  os.path.join(base_dir, "1692.jpg")



    
    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    series_element="(//span[text()='Series & Episodes'])[2]"
    all_new_element="//span[text()='Add New Series']"


    # Create Series
    title_element="//input[@id='series-title']"
    slug_element="//input[@id='series-slug']"
    description_element="//textarea[@id='series-description']"
    details_element="//div[@class='jodit-wysiwyg']"
    publish_element="//select[@id='series-custom-select']"

    # Organize
    category_element="(//div[@class=' css-qbdosj-Input'])[1]"
    language_element="(//input[contains(@id, 'react-select') and @type='text'])[2]"
    rating_elemeent="//select[@id='series-rating']"
    cast_element="(//input[contains(@id, 'react-select') and @type='text'])[3]"


    search_element="//input[@name='search_tag']"

    # Thumbnails

    series_image_element="//input[@id='series-image-url']"
    player_image_element="//input[@id='series-player-image-url']"
    tv_image_element="//input[@id='series-image-upload-selectfile2']"

    # Access

    user_access_element="//select[@id='series-user-access']"

    # Status Setting

    enable_featured_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    enable_series_active_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    #enable_slider_element="(//span[@class='admin-slider position-absolute admin-round'])[3]"
    
    #SEO
    web_title_element="//input[@id='series-website-title']"
    web_url_element="//input[@id='series-website-url']"
    meta_description_element="//textarea[@id='series-website-meta-description']"

    submit_element="(//span[text()='Create Series'])[2]"



    
        
    def test_Add_Guest(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.series_element)))
        user = self.driver.find_element(By.XPATH, self.series_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        add_role= self.driver.find_element(By.XPATH, self.all_new_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()

            
        try :
            length= 6 
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
            
        try :
            length= 6 
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.slug_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
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
        
        
        
    
       

        des=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.description_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", des) 
        des.send_keys("A short description, often referred to as a shortdesc in documentation and technical writing, ")
        time.sleep(2)

        det=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.details_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", det) 
        det.send_keys("a concise summary or overview of a topic, concept, or product")
        time.sleep(2)

        
# Select user role Dropdown
        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.publish_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        # time.sleep(2)
        # drop_down1.click()
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("2020")

            
    # Organize  
        try :
            action = ActionChains(self.driver)
            category=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",category) 
            time.sleep(2)
            category.click()
            time.sleep(1)
            action.send_keys('Test').perform()
            action.send_keys(Keys.ENTER).perform()  
            time.sleep(1)
        except Exception as e:
           print(f"âŒ Error Entering Details: {e}")


        lang=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.language_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",lang) 
        time.sleep(2)
        lang.click()
        time.sleep(1)
        action.send_keys('Tamil').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)


        drop_down2= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.rating_elemeent))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        time.sleep(2)
        drop_down2.click()
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text('8')
      
        cast=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.cast_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cast) 
        time.sleep(2)
        cast.click()
        time.sleep(1)
        action.send_keys('John Doe').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)

          
# Search 

        sea = WebDriverWait(self.driver, 30).until( EC.presence_of_element_located((By.XPATH, self.search_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sea)
        time.sleep(1)
        sea.send_keys("Movie" + Keys.ENTER)
        time.sleep(2)

          # Image  

        image1 =WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.series_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
        image1.send_keys(self.image_path_1)
        time.sleep(2)

        
        image2=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.player_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image2)
        image2.send_keys(self.image_path_2)
        time.sleep(2)

        
        image3=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.tv_image_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image3)
        image3.send_keys(self.image_path_3)
        time.sleep(2)

        #User Access
              
# Select user role Dropdown
        down3 = self.driver.find_element(By.XPATH, self.user_access_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",down3) 
        time.sleep(2)
        down3.click()
        time.sleep(2)
        select = Select(down3)
        select.select_by_visible_text("Guest (everyone)")

        toggle1 = self.driver.find_element(By.XPATH, self.enable_featured_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_series_active_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle2)
        time.sleep(2)

        # toggle3 = self.driver.find_element(By.XPATH, self.enable_slider_element)
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        # time.sleep(2)  
        # self.driver.execute_script("arguments[0].click();", toggle3)
        # time.sleep(2)

        
 # SEO 

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.web_title_element))
            ).send_keys("Moviesda")
        time.sleep(2)

        web=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.web_url_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web) 
        web.send_keys("https://www.moviesda.run/")
        time.sleep(2)

        dec=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.meta_description_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dec) 
        dec.send_keys("It includes a snapshot of what the overall plot structure and story for the film will be.")
        time.sleep(2)

        
          # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Series Guest User details Added successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 




 