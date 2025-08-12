import time
import allure
import pytest
from conftest import *
from allure_commons.types import AttachmentType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.firefox.webdriver import WebDriver

from utilities.readProp import ReadConfig

import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestDeleteMenu:
    
    driver: WebDriver

    # image and video local path
    # base_dir = os.path.join(os.getcwd(), "tmp")
    # imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    # imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    # videoFile_path = os.path.join(base_dir, "sample2.mp4")
    # pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    # subFile_path = os.path.join(base_dir, "sample2.srt")
    # # video path
    # names = os.path.abspath(os.path.join(base_dir, "sample1.mp4"))

                 # *******Server Path*******#    
    base_dir = os.path.join(os.getcwd(), "/home/automationflickn/public_html/tmp")
    imageFile_path_9_16 = os.path.join(base_dir, "9_16.jpg")
    imageFile1280_720_path = os.path.join(base_dir, "1280_720 px.png")
    imageFile480_path = os.path.join(base_dir,"tmp\sample2_480.png")
    videoFile_path = os.path.join(base_dir, "sample2.mp4")
    pdfFile_path = os.path.join(base_dir, "sample2.pdf")
    subFile_path = os.path.join(base_dir, "sample2.srt")
    # video path
    names = os.path.abspath(os.path.join(base_dir, "sample1.mp4")) 

    email_element = "//div[contains(@class,'shadow border border-1 theme-border-color p-4 rounded-3 col-11 col-lg-6 col-xl-4 mx-auto')]//input[contains(@placeholder,'email')]" #XPATH
    password_element =  "//input[contains(@placeholder,'Enter Password')]" #XPATH
    login_btn_element = "//span[normalize-space()='login']" #XPATH

    users_menu_element = "//span[normalize-space()='Menu']" #XPATH
    all_menu_element = "//span[normalize-space()='All Menus']"
    add_menu_element = "//span[contains(@class,'admin-button-text text-white')]//parent::a"

    # menu_name_element = "//input[contains(@placeholder,'Enter title')]"
    # menu_item_url_element = "//select[@name='url']"
    # site_url_element = "//input[@name='select_url']"
    # dark_mode_element =  "//div[@class='rounded-3 mb-4 theme-bg-color p-3 undefined']//div[1]//div[1]//div[1]//input[1]"
    # light_mode_element =  "//div[contains(@class,'col-12 col-md-6 px-3 pe-md-0')]//div[2]//div[1]//div[1]//input[1]"
    # dropDown_for_element = "//select[@name='type']"
    # dropDown_sub_element = "//div[@class='css-19bb58m']"
    # status_element = "//span[@class='slider round']"

    submit_btn_element = "//button[@type='submit']//span[@class='undefined'][normalize-space()='Save Menu']"

    edit_menu_btn_element = "//p[text()='Shows']//ancestor::tr//span[@class='editdropdown-button']"
    delete_btn_element = "//p[text()='Shows']//ancestor::tr//span[text()='Delete']"
    cdelete_btn_element = "//span[contains(@class,'undefined')][normalize-space()='Delete']"

    result = True

    def setup_class(self):
        self.driver.get(ReadConfig.getAdminPageURL()) #Enter website url
        self.driver.maximize_window()

    def test_EditMenu(self):        

        action = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == ReadConfig.getAdminPageURL())
        
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_btn_element).click()

        time.sleep(5)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.users_menu_element)))
        user = self.driver.find_element(By.XPATH, self.users_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", user)
        time.sleep(2)
        user.click()

        all_menu = self.driver.find_element(By.XPATH, self.all_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", all_menu)
        time.sleep(2)
        all_menu.click()
        time.sleep(2)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.edit_menu_btn_element))).click()
        time.sleep(1)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.delete_btn_element))).click()
        time.sleep(3)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.cdelete_btn_element))).click()
        time.sleep(5)

        try:
            self.driver.find_element(By.XPATH, self.edit_menu_btn_element)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Failed To Deleted Menu", attachment_type= AttachmentType.PNG)  
            result = False      
        except:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Successfully Deleted Menu", attachment_type= AttachmentType.PNG)        
            result = True

        assert result


              def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 