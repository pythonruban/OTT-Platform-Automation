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
class TestAddFooterMenu:
    
    driver: WebDriver

    # # image and video local path
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

    email_element = "//input[@name='email']"
    password_element = "//input[@name='password']"
    signin_BTN_element = "//button[@type='submit']"

    all_menu_element = "//span[normalize-space()='Menu']"
    footer_menu_element = "//span[normalize-space()='Footer Menus']"

    add_footer_element = "//button[normalize-space()='Add Footer Menu']"

    footer_menu_name_element = "//div[@class=' text-start']//input[1]"
    menu_item_url_element = "//input[@id='link']"
    column_position_element = "//select[@id='column_position']"

    submit_btn_element = "//button[@class='btn btn-primary']"

    check_add_element = "//p[normalize-space()='Test Footer']"

    def test_Add_Footer(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())
             

        action = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == ReadConfig.getAdminPageURL())
        
        ele = self.driver.find_elements(By.XPATH, self.email_element)
        ele[1].send_keys("admin@admin.com")
        self.driver.find_element(By.XPATH, self.password_element).send_keys("Webnexs123!@#")
        ele = self.driver.find_elements(By.XPATH, self.signin_BTN_element)
        ele[1].click()

        time.sleep(3)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.all_menu_element)))
        allmenu = self.driver.find_element(By.XPATH, self.all_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", allmenu)
        time.sleep(2)
        allmenu.click()

        footer_menu = self.driver.find_element(By.XPATH, self.footer_menu_element)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", footer_menu)
        time.sleep(2)
        footer_menu.click()
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.add_footer_element).click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.footer_menu_name_element)))
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.footer_menu_name_element).send_keys("Test Footer")
        self.driver.find_element(By.XPATH, self.menu_item_url_element).send_keys("Test Footer Url")


        column = self.driver.find_element(By.XPATH, self.column_position_element)
        column.click()
        time.sleep(2)
        select = Select(column)
        select.select_by_index(2)

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Add Footer Menu Page", attachment_type= AttachmentType.PNG)

        self.driver.find_element(By.XPATH, self.submit_btn_element).click()
        time.sleep(10)

        try:
            WebDriverWait(self.driver, 25).until(EC.visibility_of_element_located((By.XPATH, self.check_add_element)))
            time.sleep(5)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "New Footer Menu Created Successfully", attachment_type= AttachmentType.PNG)     
            assert True                
        except:
            time.sleep(5)
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Bug: New Footer Menu Is Not Created", attachment_type= AttachmentType.PNG)     
            assert False 
        

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 