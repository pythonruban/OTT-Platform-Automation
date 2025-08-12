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
class TestAdd_User:
   
    driver: WebDriver

    
       #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080.1080.jpg")

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    users_element="//span[text()='Users']"
    add_element="//span[text()='Add New User']"

    username_element="//input[@id='username']"
    lastname_element="//input[@id='last_name']"
    mail_element="//input[@id='email']"
    pass_element="//input[@name='password']"
    code_element="//select[@name='ccode']"
    mobile_element="//input[@name='mobile']"
    dob_element="//input[@id='dob']"
    gender_element="//select[@name='gender']"
    active_element="//span[@class='slider round']"
    image_element="//input[@id='fileId']"
    country_element="//input[@id='country-select']"
    suggest_element="(//div[@class='stdropdown-item false'])[102]"
    state_element="//input[@id='state-select']"
    city_element="//input[@id='city-select']"
    role_element="//select[@name='role']"
    save_element="(//span[text()='Save User'])[2]"



    
    def test_Add_User(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.users_element)))
        user = self.driver.find_element(By.XPATH, self.users_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.add_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try :
            length= 6 
            auto_name = ''.join(random.choices(string.ascii_uppercase, k=length))
            print(f"Generated name: {auto_name}")
 
            print(f"Using XPath: {self.username_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.username_element))
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
 
            print(f"Using XPath: {self.lastname_element}")
 
            # Wait for the title input to be clickable
            name = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.lastname_element))
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
            mail=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.mail_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",mail)  
            mail.send_keys("deep513@gmail.com")
            print("✅ Email is entered Successfully")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to enter email: {e}")


        try :
            pa=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.pass_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",pa)  
            pa.send_keys("Deepakraj@78")
            print("✅ Password is entered Successfully")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Password: {e}")


        
        try :
            drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.code_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("India - (91)")
            print("✅ Code is Selected Successfully") 
        except Exception as e:
            print(f" Failed to select ccode: {e}")

        try :
            number=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.mobile_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",number)  
            number.send_keys("8596526341")
            print("✅ Number is entered Successfully")
            time.sleep(3)
        except Exception as e:
            print(f" Failed to Enter Mobile Number: {e}")

        # try :
        #     dob=WebDriverWait(self.driver, 80).until(
        #         EC.presence_of_element_located((By.XPATH, self.dob_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",dob) 
        #     time.sleep(1) 
        #     dob.send_keys("2025-06-20")
        #     print("✅ DOB is entered Successfully")
        #     time.sleep(3)
        # except Exception as e:
        #     print(f" Failed to select DOB: {e}")

        try :
            drop_down3= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.gender_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down3) 
            time.sleep(2)
            select = Select(drop_down3)
            select.select_by_visible_text("Male")
            print("✅ Gender is Selected Successfully")
        except Exception as e:
            print(f" Failed to select Gender: {e}")

        toggle = self.driver.find_element(By.XPATH, self.active_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle)
        time.sleep(2)

         # Upload Image
        try:
            image = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.image_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
            time.sleep(2)
            image.send_keys(self.image_path_1)
            print("✅ Image is uploaded Successfully")
        except Exception as e:
            print(f"❌ Error uploading image: {e}")

        # try:
        #     input_element = self.driver.find_element(By.XPATH, self.country_element)

        #     # Send keys to the input field
        #     input_element.send_keys("India")

        #     # Optional: simulate Enter key press
        #     input_element.send_keys(Keys.ENTER)

           
        # except Exception as e:
        #     print("Error selecting state:", e)

        # try :
        #     country=WebDriverWait(self.driver, 30).until(
        #         EC.presence_of_element_located((By.XPATH, self.country_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",country)  
        #     time.sleep(1)
        #     country.send_keys("India")
        #     time.sleep(3)
           
        # except Exception as e:
        #     print(f" Failed to enter Country: {e}")

        # try :
        #     action = ActionChains(self.driver)
        #     category=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.country_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",category) 
        #     time.sleep(2)
        #     category.click()
        #     time.sleep(1)
        #     action.send_keys('India').perform()
        #     #action.send_keys(Keys.ENTER).perform()  
        #     time.sleep(1)
        # except Exception as e:
        #    print(f"❌ Error Entering Details: {e}")

        # try :
        #     state=WebDriverWait(self.driver, 30).until(
        #         EC.presence_of_element_located((By.XPATH, self.state_element))
        #     )
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",state)  
        #     time.sleep(1)
        #     state.send_keys("Tamil Nadu")
        #     time.sleep(3)
        # except Exception as e:
        #     print(f" Failed to enter State: {e}")

        # try :
        #     city=WebDriverWait(self.driver, 30).until(
        #         EC.presence_of_element_located((By.XPATH, self.city_element)))
        #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",city)  
        #     time.sleep(1)
        #     city.send_keys("Sivaganga")
        #     time.sleep(2)
        # except Exception as e:
        #     print(f" Failed to Enter City: {e}")


        try :
            drop_down4= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.role_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down4) 
            time.sleep(2)
            select = Select(drop_down4)
            select.select_by_visible_text(" Registered")
            print("✅ User role is Selected Successfully")
        except Exception as e:
            print(f" Failed to select Role: {e}")

               # Submit Form
        try:
            save_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.save_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
            time.sleep(2)
            save_button.click()
            time.sleep(2)
            print("✅ User added successfully!")
        except Exception as e:
            print(f"❌ Error saving user: {e}")
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="New User Added successfully!", attachment_type=AttachmentType.PNG)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 









