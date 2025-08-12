import time
import allure
import pytest
import os
import glob
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
class TestAddEmbed:
   
    driver: WebDriver
 

      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1692.jpg")
    image_path_2 = os.path.join(base_dir, "9.16.jpg")
    image_path_3 =  os.path.join(base_dir, "9.16.jpg")
    image_path_4 =  os.path.join(base_dir, "9.16.jpg")
    videoFile_path1 =  os.path.join(base_dir, "demo1.mp4")
    videoFile_path2 =  os.path.join(base_dir, "Maaman.mp4")
    pdfFile_path = os.path.join(base_dir, "Book1.xlsx")
    vtt_path_1= os.path.join(base_dir, "dummy.pdf")
    vtt_path_2= os.path.join(base_dir, "dummy.pdf")
    vtt_path_3= os.path.join(base_dir, "dummy.pdf")
    

    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH


    video_element="//span[text()='Videos']"
    add_video_element="//span[text()='Add Video']"

    # radiobutton xpath
    embed_element="(//input[@id='videoTypeOptionRadio'])[4]"
    url_element="//input[@id='video-embed-code']"
    submit_element="//span[text()='Submit']"

    proceed_element="//span[text()='Proceed Next']"

    title_element="//input[@id='video-title']"
    slug_element="//input[@id='video-slug']"
    description_element="//textarea[@id='video-description']"
    detail_element="//div[@class='jodit-wysiwyg']"
    

    # Organize

    category_element="(//input[contains(@id, 'react-select') and @type='text'])[1]"
    age_element="//select[@id='video-age-restrict']"
    language_element="(//input[contains(@id, 'react-select') and @type='text'])[2]"
    rating_element="//select[@id='video-rating']"
    cast_element="(//input[contains(@id, 'react-select') and @type='text'])[3]"
    related_element="(//input[contains(@id, 'react-select') and @type='text'])[4]"
    playlist_element="(//input[contains(@id, 'react-select') and @type='text'])[5]"

    # Free Duration

    duration_element="//input[@id='video-duration']"
  
    # Intro Time
    skip_start_element="//input[@id='video-skip-start-time']"
    skip_end_element="//input[@id='video-skip-end-time']"
    recap_start_element="//input[@id='video-recap-start-time']"
    recap_end_element="//input[@id='video-recap-end-time']"
    start_session_element="//input[@id='video-skip-start-session']"
    end_session_element="//input[@id='video-recap-start-session']"

    # Information

    epaper_element="//input[@id='video-epaper-upload']"
    url1_element="//input[@id='inputField']"
    url_start_element="//input[@id='video-url-linktym']"
    url_end_element="//input[@id='video-urlEnd-linksec']"

    # Status Setting
    enable_feature_element="(//span[@class='admin-slider position-absolute admin-round'])[1]"
    enable_active_element="(//span[@class='admin-slider position-absolute admin-round'])[2]"
    enable_slider_element="(//span[@class='admin-slider position-absolute admin-round'])[3]"
    enable_title_element="(//span[@class='admin-slider position-absolute admin-round'])[4]"


    # Advertisment

    pre_ad_element="//select[@id='video-pre-ads-select']"
    post_ad_element="//select[@id='video-post-ads-select']"
    mid_ad_element="//select[@id='video-category-select']"
    mid_sequence_element="//input[@id='video-category-sequence']"


    # Thumbnail
    video_thumb_element="//input[@id='video-thumbnail-image']"
    player_thumb_element="//input[@id='video-plyer-image']"
    tv_thum_element="//input[@id='video-tv-image']"
    video_title_element="//input[@id='video-title-image']"

    # Trailer Upload
     
    trailer_type_element="//select[@id='video-trailer-type']"
    trailer_embed_element="//input[@id='video-trailer-embed-code']"
    


    # Publish Type
    publish_now_element="//input[@id='video-publish-now']"
    year_element="//select[@id='video-year']"
    #publish_later_element="//input[@id='video-publish-later']"
    #publish_time_element="//input[@id='video-publish-time']"

    # User Access
    access_element="//select[@id='video-access']"


    # SEO 
    page_title_element="//input[@id='video-website-page-title']"
    website_url_element="//input[@id='video-website-url']"
    descr_element="//textarea[@id='video-meta-description']"

    # Search 
    search_element="//input[@name='search_tags']"

    
    tamil_subtitle_element="//input[@id='videoSubtitle'][1]"
    english_element="(//input[@id='videoSubtitle'])[2]"
    malayalam_element="(//input[@id='videoSubtitle'])[3]"

    update_element="(//span[text()='Update Video'])[2]"

    
       
    def test_Add_Embed(self,browser_setup):
        self.driver = browser_setup
        self.driver.maximize_window()
        self.driver.get(ReadConfig.getAdminPageURL())

        # Login to the application
        self.driver.find_element(By.XPATH, self.email_element).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, self.password_element).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, self.login_element).click()

        
        try:
            WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.dashboard_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login was successful and the UI elements have been loaded.", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Login successful and the UI elements have not loaded due to timeout", attachment_type=AttachmentType.PNG)
            raise e

        

        # Scroll to ensure all elements are loaded
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.video_element)))
        user = self.driver.find_element(By.XPATH, self.video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        add_role= self.driver.find_element(By.XPATH, self.add_video_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()


      # single click using WebDriverWait
          
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.embed_element))
            ).click()
        time.sleep(2)


        
        WebDriverWait(self.driver, 80).until(
               EC.presence_of_element_located((By.XPATH, self.url_element))
            ).send_keys("https://www.youtube.com/embed/dvWdFMCC1-I?si=duPpMtwqQqihJAMa")
        time.sleep(2)
           
        WebDriverWait(self.driver, 250).until(
               EC.presence_of_element_located((By.XPATH, self.submit_element))
        ).click()
        time.sleep(2)

        WebDriverWait(self.driver, 250).until(
               EC.presence_of_element_located((By.XPATH, self.proceed_element))
        ).click()
        time.sleep(2)

        try :
            tit=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, self.title_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tit) 
            tit.clear()
            time.sleep(1)
            tit.send_keys("")
            time.sleep(2)
            
        except Exception as e:
            print(f" Failed to enter title: {e}")
        
        try :
            slug=WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.slug_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug) 
            slug.clear()
            time.sleep(1)
            slug.send_keys("")
            time.sleep(2)
        except Exception as e:
            print(f" Failed to enter Slug: {e}")



        des=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.description_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", des) 
        des.send_keys("")
        time.sleep(2)

        det=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.detail_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", det) 
        det.send_keys("")
        time.sleep(2)


      
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
            action.send_keys('Horror').perform()
            action.send_keys(Keys.ENTER).perform()  
            time.sleep(1)
        except Exception as e:
           print(f"❌ Error Entering Details: {e}")


        try :
            drop_down1 = self.driver.find_element(By.XPATH, self.age_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            drop_down1.click()
            time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("Choose an age")
        except Exception as e:
           print(f"❌ Error selecting country code: {e}")



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


        # Select user role Dropdown
        drop_down2 = self.driver.find_element(By.XPATH, self.rating_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        drop_down2.click()
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_visible_text("Choose an rating")

      

# REACT 
       
        cast=WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.cast_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cast)
        time.sleep(2)
        cast.click()
        time.sleep(1)
        action.send_keys('Prabakar').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)

     
       

        related=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.related_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",related) 
        time.sleep(2)
        related.click()
        time.sleep(1)
        action.send_keys('Retro TV').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)

        play=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.playlist_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play) 
        time.sleep(2)
        play.click()
        time.sleep(1)
        action.send_keys('Beast').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)


        
# Free Duration
        try :
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.duration_element))
                ).send_keys("")
            time.sleep(2)
        except Exception as e:
           print(f"❌ Error Entering Details: {e}")
        
 
# Intro time 
       
        star=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.skip_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",star)
        star.send_keys("")
        time.sleep(2)

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.skip_end_element))
            ).send_keys("")
        time.sleep(2)

        rec=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.recap_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rec) 
        rec.send_keys("")
        time.sleep(2)

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.recap_end_element))
            ).send_keys("")
        time.sleep(2)

        ses=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.start_session_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ses) 
        ses.send_keys("")
        time.sleep(2)

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.end_session_element))
            ).send_keys("")
        time.sleep(2)

                   
# Information

        pdf=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.epaper_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pdf)
        pdf.send_keys(self.pdfFile_path)
        time.sleep(2)

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url1_element))
            ).send_keys("")
        time.sleep(2)

        ur=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ur) 
        ur.send_keys("http")
        time.sleep(2)

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url_end_element))
            ).send_keys("")
        time.sleep(2)

# Status Setting

        toggle1 = self.driver.find_element(By.XPATH, self.enable_feature_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle1)
        time.sleep(2)

        toggle2 = self.driver.find_element(By.XPATH, self.enable_active_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
        time.sleep(2)

        actions = ActionChains(self.driver)
        actions.double_click(toggle2).perform()
        time.sleep(2)

        toggle3 = self.driver.find_element(By.XPATH, self.enable_slider_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle3)
        time.sleep(2)

        toggle4 = self.driver.find_element(By.XPATH, self.enable_title_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", toggle4)
        time.sleep(2)


    # Advertisement

    #    # Select user role Dropdown
    #     drop_down3 = self.driver.find_element(By.XPATH, self.pre_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down3) 
    #     drop_down3.click()
    #     time.sleep(2)
    #     select = Select(drop_down3)
    #     select.select_by_visible_text("8")

    #        # Select user role Dropdown
    #     drop_down4 = self.driver.find_element(By.XPATH, self.post_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down4) 
    #     drop_down4.click()
    #     time.sleep(2)
    #     select = Select(drop_down4)
    #     select.select_by_visible_text("8")

    #        # Select user role Dropdown
    #     drop_down5 = self.driver.find_element(By.XPATH, self.mid_ad_element)
    #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down5) 
    #     drop_down5.click()
    #     time.sleep(2)
    #     select = Select(drop_down5)
    #     select.select_by_visible_text("8")

        
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.mid_sequence_element))
            ).send_keys("")
        time.sleep(2)




    # Image  

        image1 =WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.video_thumb_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image1)
        image1.send_keys(self.image_path_1)
        time.sleep(2)

        
        image2=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.player_thumb_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image2)
        image2.send_keys(self.image_path_2)
        time.sleep(2)

        
        image3=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.tv_thum_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image3)
        image3.send_keys(self.image_path_3)
        time.sleep(2)

        
        image4=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.video_title_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image4)
        image4.send_keys(self.image_path_4)
        time.sleep(2)

    # Trailer Upload
        
        drop_down6= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.trailer_type_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down6) 
        # time.sleep(2)
        # drop_down6.click()
        time.sleep(2)
        select = Select(drop_down6)
        select.select_by_visible_text("Embed url")

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.trailer_embed_element))
            ).send_keys("http")
        time.sleep(2)

     

 # Visibility

#publish Now
        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.publish_now_element))
            )
        time.sleep(2)

# Select user role Dropdown
        drop_down7= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.year_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down7) 
        # time.sleep(2)
        # drop_down7.click()
        time.sleep(2)
        select = Select(drop_down7)
        select.select_by_visible_text("Choose publish year")

# # Publish Later
#         WebDriverWait(self.driver, 30).until(
#                EC.presence_of_element_located((By.XPATH, self.publish_later_element))
#             ).click()
#         time.sleep(2)

#         WebDriverWait(self.driver, 30).until(
#                EC.presence_of_element_located((By.XPATH, self.publish_time_element))
#             ).send_keys("2025-05-11T10:39")
#         time.sleep(2)
        

# User Access
              
# Select user role Dropdown
        down8 = self.driver.find_element(By.XPATH, self.access_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",down8) 
        # time.sleep(2)
        # down8.click()
        time.sleep(2)
        select = Select(down8)
        select.select_by_visible_text("Choose an user access")

 # SEO 

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.page_title_element))
            ).send_keys("")
        time.sleep(2)

        web=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.website_url_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web) 
        web.send_keys("http")
        time.sleep(2)

        dec=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.descr_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dec) 
        dec.send_keys("")
        time.sleep(2)

        
# Search 

        WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.search_element))
            ).send_keys("")
        time.sleep(2)

# Subtitle 
        vtt =WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.tamil_subtitle_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vtt)
        vtt.send_keys(self.vtt_path_1)
        time.sleep(2)

        vtt1 =WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.english_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vtt1)
        vtt1.send_keys(self.vtt_path_2)
        time.sleep(2)

        vtt2 =WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.malayalam_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vtt2)
        vtt2.send_keys(self.vtt_path_3)
        time.sleep(2)

          
          # update or save element
        save_element=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        self.driver.execute_script("arguments[0].click();", save_element)
       
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Embed Access User details Added successfully.", attachment_type=AttachmentType.PNG)


    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 


