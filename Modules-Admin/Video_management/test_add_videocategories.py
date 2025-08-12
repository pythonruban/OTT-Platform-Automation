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

import glob
import os

@pytest.mark.usefixtures("browser_setup")
class TestVideocategories:
    
    driver: WebDriver

    imageFile_path = os.path.join(os.getcwd(), f'tmp\\sample2.png')

    email_element = "email" #id
    password_element = "password" #id
    login_btn_element = "//button[normalize-space()='SIGN IN']" #XPATH

    video_management_btn_element = "//span[normalize-space()='Video Management']" #XPATH
    manage_videocategorie_btn_element = "//li[contains(@class,'')]//a[contains(text(),'Manage Video Categories')]" #XPATH
    addnew_btn_element = "//i[@class='fa fa-plus-circle']"
    # sendkeys element
    NVC_name_btn_element = "//input[@id='name']"
    NVC_slug_btn_element = "//input[@id='slug']"
    homepage_genrename_btn_element = "//input[@id='home_genre']"

    # Radio btn element 
    display_homepage_yes_btn_element = "//input[@id='in_home' and @value='1']" 
    display_homepage_no_btn_element = "//input[@id='in_home' and @value='0']"
    display_menu_yes_btn_element = "//input[@id='in_menu' and @value='1']"
    display_menu_no_btn_element = "//input[@id='in_menu' and @value='0']"

    image_element = "//input[@id='image']"
    banner_element = "//input[@id='banner_image']"

    genre_element = "//select[@id='parent_id']"

    display_in_home_banner_checkbox_element = "//input[@id='banner']"

    close_btn_element = "//button[contains(text(),'Close')]"
    save_changes_btn_element = "//button[@id='submit-new-cat']"

    def setup_class(self):
        self.driver.get("https://dev.e360tv.com/admin") #Enter website url
        self.driver.maximize_window()
    
    def test_add_videocategorie(self):

        action = ActionChains(self.driver)

        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == "https://dev.e360tv.com/login")
        
        self.driver.find_element(By.ID, self.email_element).send_keys('admin@admin.com')
        self.driver.find_element(By.ID, self.password_element).send_keys('Webnexs123!@#')
        self.driver.find_element(By.XPATH, self.login_btn_element).click()
        time.sleep(5)

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_management_btn_element))).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.manage_videocategorie_btn_element).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.addnew_btn_element).click()
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, self.NVC_name_btn_element).send_keys("Action")
        self.driver.find_element(By.XPATH, self.NVC_slug_btn_element).send_keys("test")
        self.driver.find_element(By.XPATH, self.homepage_genrename_btn_element).send_keys("test")
       
        # radio buttons (yes)
        self.driver.find_element(By.XPATH, self.display_homepage_yes_btn_element).click()
        
        # radio buttons (no)        
        # self.driver.find_elements(By.XPATH, self.display_homepage_no_btn_element).click()
        

        # radio buttons (yes)
        self.driver.find_element(By.XPATH, self.display_menu_yes_btn_element).click()
        
        # radio buttons (no)        
        # self.driver.find_elements(By.XPATH, self.display_menu_no_btn_element).click()
        

        self.driver.find_element(By.XPATH, self.image_element).send_keys(self.imageFile_path)

        self.driver.find_element(By.XPATH, self.banner_element).send_keys(self.imageFile_path)

        ele = self.driver.find_element(By.XPATH, self.genre_element)
        select = Select(ele)
        select.select_by_index(2)
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.display_in_home_banner_checkbox_element).click()

        # allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "New Video Category Created Successfully", attachment_type= AttachmentType.PNG)        
        # time.sleep(2)

        # Save Button
        self.driver.find_element(By.XPATH, self.save_changes_btn_element).click()
        time.sleep(3)

        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "New Video Category Created Successfully", attachment_type= AttachmentType.PNG)        
        time.sleep(2)

        # Close Button
        # self.driver.find_element(By.XPATH, self.close_btn_element).click()

        assert True

    def teardown_class(self):
        self.driver.quit()