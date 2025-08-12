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
class TestAddVideo:
    
    driver: WebDriver

    
    # videoFileall_path = os.path.join(os.getcwd(), f'tmp\\Videos')
    names = [x for x in glob.glob(f"/home/automationflickn/public_html/tmp/Videos/*.mp4")]
    fileNames = " ".join(f'"{name}"' for name in names)
    
    imageFile_path = os.path.join(os.getcwd(), f'/home/automationflickn/public_html/tmp/sample2.png')
    imageFile480_path = os.path.join(os.getcwd(), f'tmp\\sample2_480.png')
    imageFile1920_path = os.path.join(os.getcwd(), f'tmp\\sample2_1920.png')    
    videoFile_path = os.path.join(os.getcwd(), f'/home/automationflickn/public_html/tmp/sample2.mp4')
    pdfFile_path = os.path.join(os.getcwd(), f'/home/automationflickn/public_html/tmp/sample2.pdf') 
    subFile_path = os.path.join(os.getcwd(), f'/home/automationflickn/public_html/tmp/sample2.srt') 
    
    # keyboard = Controller()  

    email_element = "email" #id
    password_element = "password" #id
    login_btn_element = "//button[normalize-space()='SIGN IN']" #XPATH

    video_management_btn_element = "//span[normalize-space()='Video Management']" #XPATH
    add_new_video_btn_element = "//a[normalize-space()='Add New Video']" #XPATH
    all_video_btn_element = "//ul[@id='video']//a[contains(text(),'All Videos')]" #XPATH
    
    #All Videos
    table_element = " //tbody/*" #XPATH
    
    
    #Add Videos
    choose_video_element = "//select[@id='UploadlibraryID']" #XPATH
    uploadVideo_element = "//form[@class='dropzone dz-clickable']" #XPATH
    inputVideos_element = "//input[@accept='video/mp4,video/x-m4v,video/x-matroska,video/mkv']"
    proceed_upload_element = "//input[@id='Next']" #XPATH
    
    uploaded_video_processIndicator_element = "//form[@method='post']//span[@id='upload-percentage']"
    
    
    title_element = "title" #id
    slug_element = "slug" #id
    videoDetails_element = "//p[@class='ck-placeholder']/parent::*" #XPATH
    duration_element = "duration" #name
    year_element = "year" #name
    ageRestrict_element = "age_restrict" #id
    rating_element = "//span[@id='select2-rating-container']"
    link_and_desc_element = "//p[@data-placeholder='Link , and details']"
    
    skip_intro_Time_element = "skip_intro" #id
    intro_start_Time_element = "intro_start_time" #id
    intro_end_Time_element = "intro_end_time" #id
    recap_Time_element = "skip_recap" #id
    recap_start_Time_element = "recap_start_time" #id
    recap_end_Time_element = "recap_end_time" #id
    
    enable_freetime_element = "//div[@class='panel-body']//span[@class='slider round']"
    
    free_duration_Time_element = "free_duration"
    
    video_detail_next_btn_element = "//input[@id='next2']"
    
    
    video_category_element = "//span[@data-select2-id='3']"
    cast_and_crew_element = "//span[@data-select2-id='5']"
    lang_element = "//span[@data-select2-id='6']"
    epaper_element = "pdf_file"
    playlist_element = "//span[@data-select2-id='7']"
    reels_video_element = "enable_reel_conversion"
    reel_upload_element = "reels_videos[]"
    reel_thumnail_element = "reels_thumbnail"
    url_element = "//input[@id='url_link']"
    url_time_element = "//input[@id='url_linktym']"
    sub_en_element = "subtitle_upload_en"
    sub_de_element = "subtitle_upload_de"
    sub_es_element = "subtitle_upload_es"
    sub_hi_element = "subtitle_upload_hi"
    category_next_btn_element = "//input[@id='next3']"
    
    block_country_element = "//span[@data-select2-id='9']"
    avail_country_element = "//span[@data-select2-id='10']"  
    user_access_element = "//select[@id='access']"
    search_tag_element = "//div[@class='tags-input-wrapper']//input" 
    related_videos_element = "//span[@data-select2-id='12']" 
    user_video_access_next_btn_element = "//input[@id='nextppv']"
    
    video_thumbnail_element = "//input[@id='image']"
    player_thumbnail_element = "//input[@id='player_image']"
    video_tv_thumbnail_element = "//input[@id='video_tv_image']"
    video_title_thumbnail_element = "//input[@id='video_title_image']"
    enable_video_title_thumbnail_element = "//input[@id='enable_video_title_image']"
    video_trailer_type = "//select[@id='trailer_type']"
    upload_triler_element = "//input[@id='trailer']"
    trailer_desc_element = "//textarea[@id='trailer-ckeditor']"
    img_trailer_nxt_element = "//input[@id='next_input']"
    
    advertisement_devices = "//span[@data-select2-id='2']"
    finish_btn_element = "//button[@value='Add New Video']"
    
    # ****** User Page ***************
    
    search_btn_element = "//i[@class='ri-search-line']"
     
     
    def setup_class(self):
        self.driver.get("https://dev.e360tv.com/admin") #Enter website url
        self.driver.maximize_window()
        
    def test_addvideo(self):

        action = ActionChains(self.driver)
        
        WebDriverWait(self.driver, 15).until(lambda driver: driver.current_url == "https://dev.e360tv.com/login")
        
        self.driver.find_element(By.ID, self.email_element).send_keys('admin@admin.com')
        self.driver.find_element(By.ID, self.password_element).send_keys('Webnexs123!@#')
        self.driver.find_element(By.XPATH, self.login_btn_element).click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_management_btn_element))).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.add_new_video_btn_element).click()

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.choose_video_element))).click()
        time.sleep(3)
        select = Select(self.driver.find_element(By.XPATH, self.choose_video_element))
        select.select_by_visible_text('All Videos / Files')
        
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.uploadVideo_element)))
        time.sleep(3)
        
        for i in self.names:            
            self.driver.find_element(By.XPATH, self.inputVideos_element).send_keys(i)
        
        elements = self.driver.find_elements(By.XPATH, self.uploaded_video_processIndicator_element)
                
        while True:
            currently_uploading_number = len([ele.text for ele in elements if int(ele.text.replace('%', '')) == 100])
            if currently_uploading_number != len(self.names):
                pass
            else:
                break

        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.proceed_upload_element))).click()
        time.sleep(5)
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.ID, self.title_element))).click()
        ele = self.driver.find_element(By.ID, self.title_element)
        self.driver.find_element(By.ID, self.slug_element).send_keys('sample2')
        
        self.driver.find_element(By.ID, self.ageRestrict_element).click()        
        

        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.videoDetails_element).click()
        time.sleep(1)

        action.send_keys("This is a description for sample2 video.").perform()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.link_and_desc_element).click()

        action.send_keys("This is a Link and description for sample2 video.").perform()
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, self.rating_element).click()
        time.sleep(1)

        action.send_keys("5").perform()
        time.sleep(1)

        action.send_keys(Keys.ENTER).perform()
        
        self.driver.find_element(By.ID, self.skip_intro_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.skip_intro_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.skip_intro_Time_element).send_keys('01')
        
        self.driver.find_element(By.ID, self.intro_start_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.intro_start_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.intro_start_Time_element).send_keys('00')
        
        self.driver.find_element(By.ID, self.intro_end_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.intro_end_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.intro_end_Time_element).send_keys('60')
        
        self.driver.find_element(By.ID, self.recap_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_Time_element).send_keys('50')
        
        self.driver.find_element(By.ID, self.recap_start_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_start_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_start_Time_element).send_keys('00')
        
        self.driver.find_element(By.ID, self.recap_end_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_end_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.recap_end_Time_element).send_keys('00')
        
        self.driver.find_element(By.ID, self.year_element).send_keys('2024')
        
        self.driver.find_element(By.XPATH, self.enable_freetime_element).click()
        
        self.driver.find_element(By.ID, self.free_duration_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.free_duration_Time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.ID, self.free_duration_Time_element).send_keys('01')
        time.sleep(5)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Video Detail Session", attachment_type= AttachmentType.PNG)
        
        
        next2 = self.driver.find_element(By.XPATH, self.video_detail_next_btn_element)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next2)
        time.sleep(2)
        next2.click()
        
        time.sleep(2)
        
        top = self.driver.find_element(By.XPATH, "//a[@class='black'][normalize-space()='Add New Video']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", top)
        
        self.driver.find_element(By.XPATH, self.video_category_element).click()
        time.sleep(1)

        action.send_keys('m').perform()
        action.send_keys(Keys.ENTER).perform()
        
        
        self.driver.find_element(By.XPATH, self.cast_and_crew_element).click()
        time.sleep(1)        

        action.send_keys('e').perform()

        action.send_keys(Keys.ENTER).perform()
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, self.lang_element).click()
        time.sleep(1)

        action.send_keys('e').perform()

        action.send_keys(Keys.ENTER).perform()
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, self.playlist_element).click()
        time.sleep(1)  
        
        
        self.driver.find_element(By.NAME, self.reel_upload_element).send_keys(self.videoFile_path)
        
        self.driver.find_element(By.NAME, self.reel_thumnail_element).send_keys(self.imageFile_path)
        
        self.driver.find_element(By.XPATH, self.url_element).send_keys('https://dev.e360tv.com/admin')
        
        self.driver.find_element(By.XPATH, self.url_time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.url_time_element).send_keys('00')
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.url_time_element).send_keys('01')
        
        self.driver.find_element(By.ID, self.sub_en_element).send_keys(self.subFile_path)
        
        self.driver.find_element(By.ID, self.sub_de_element).send_keys(self.subFile_path)
 
        self.driver.find_element(By.ID, self.sub_es_element).send_keys(self.subFile_path)
        
        self.driver.find_element(By.ID, self.sub_hi_element).send_keys(self.subFile_path)
        
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Category Session", attachment_type= AttachmentType.PNG)
        
        next3 = self.driver.find_element(By.XPATH, self.category_next_btn_element)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next3)
        time.sleep(2)
        next3.click()
        
        time.sleep(10)
        top = self.driver.find_element(By.XPATH, "//a[@class='black'][normalize-space()='Add New Video']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", top)
        time.sleep(2)
        
        try:
            self.driver.find_element(By.XPATH, self.block_country_element).click()
            time.sleep(1)
        except:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next3)
            time.sleep(2)
            next3.click()
            self.driver.execute_script("arguments[0].scrollIntoView(true);", top)
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.block_country_element).click()
            time.sleep(1)
        self.driver.find_element(By.XPATH, self.block_country_element).click()
        time.sleep(1)

        action.send_keys('a').perform()
        action.send_keys(Keys.ENTER).perform()
        
        self.driver.find_element(By.XPATH, self.avail_country_element).click()
        time.sleep(1)

        action.send_keys('india').perform()

        action.send_keys(Keys.ENTER).perform()
        action.send_keys(Keys.ENTER).perform()
        
        ele = self.driver.find_element(By.XPATH, self.user_access_element)
        select = Select(ele)
        select.select_by_index(1)
        
        self.driver.find_element(By.XPATH, self.search_tag_element).send_keys("sample2")
        
        self.driver.find_element(By.XPATH, self.related_videos_element).click()
        time.sleep(1)

        action.send_keys('a').perform()

        action.send_keys(Keys.ENTER).perform()
        
        self.driver.find_element(By.XPATH, "//input[@id='featured']").click()
        
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "User Video Access Session", attachment_type= AttachmentType.PNG)
        
        nextppv = self.driver.find_element(By.XPATH, self.user_video_access_next_btn_element)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", nextppv)
        time.sleep(2)
        nextppv.click()
        
        time.sleep(3)
        
        top = self.driver.find_element(By.XPATH, "//a[@class='black'][normalize-space()='Add New Video']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", top)
        
        self.driver.find_element(By.XPATH, self.video_tv_thumbnail_element).send_keys(self.imageFile_path)
        self.driver.find_element(By.XPATH, self.video_title_thumbnail_element).send_keys(self.imageFile_path)
        
        time.sleep(1)

        action.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        
        next4 = self.driver.find_element(By.XPATH, self.img_trailer_nxt_element)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next4)
        
        time.sleep(1)
        
        ele = self.driver.find_element(By.XPATH, self.video_trailer_type)
        select = Select(ele)
        select.select_by_index(1)
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, self.upload_triler_element).send_keys(self.videoFile_path)
        
        self.driver.find_element(By.XPATH, self.trailer_desc_element).click()
        time.sleep(1)

        action.send_keys("This is a Trailer description for sample2 video.").perform()
        
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "Video Detail Session", attachment_type= AttachmentType.PNG)        
        time.sleep(2)
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next4)       
        time.sleep(2)
        next4.click()
        
        time.sleep(3)
        
        self.driver.find_element(By.XPATH, self.advertisement_devices).click()
        time.sleep(1)

        action.send_keys('w').perform()

        action.send_keys(Keys.ENTER).perform()
        time.sleep(1)        
        
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name= "ADS Management Session", attachment_type= AttachmentType.PNG)        
        
        self.driver.find_element(By.XPATH, self.finish_btn_element).click()

        time.sleep(20)

    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 