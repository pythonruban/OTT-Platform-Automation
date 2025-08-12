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
class TestEditMp4:
   
    driver: WebDriver
 

      #*******Local Path*******#
    base_dir = os.path.join(os.getcwd(), "tmp")
    image_path_1 = os.path.join(base_dir, "1080_1620.jpg")
    image_path_2 = os.path.join(base_dir, "1692.jpg")
    image_path_3 =  os.path.join(base_dir, "1691.jpg")
    image_path_4 =  os.path.join(base_dir, "1280_720 px.jpg")
    videoFile_path1 =  os.path.join(base_dir, "demo1.mp4")
    videoFile_path2 =  os.path.join(base_dir, "Maaman.mp4")
    pdfFile_path = os.path.join(base_dir, "dummy.pdf")
    vtt_path_1= os.path.join(base_dir, "tamil.vtt")
    vtt_path_2= os.path.join(base_dir, "english.vtt")
    vtt_path_3= os.path.join(base_dir, "malayalam.vtt")
    

    # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH


    video_element="//span[text()='Videos']"
    all_element="//span[text()='All Video']"

    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[@class='admin-slider position-absolute admin-round'])[2]"
    
    title_element="//input[@id='video-title']"
    slug_element="//input[@id='video-slug']"
    description_element="//textarea[@id='video-description']"
    detail_element="//div[@class='jodit-wysiwyg']"
    #duration_element="//input[@id='video-duration']"

    # Organize

    category_element="(//input[contains(@id, 'react-select') and @type='text'])[1]"
    age_element="//select[@id='video-age-restrict']"
    language_element="(//input[contains(@id, 'react-select') and @type='text'])[2]"
    rating_element="//select[@id='video-rating']"
    cast_element="(//input[contains(@id, 'react-select') and @type='text'])[3]"
    related_element="(//div[contains(@class, 'ValueContainer')]//input)[4]"
    playlist_element="(//div[contains(@class, 'ValueContainer')]//input)[5]"

    # Free Duration

    duration_element="//input[@id='video-duration']"
    duration_status_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    free_duration_element="//input[@id='video-free-duration-time']"
  


    # Intro Time
    skip_start_element="//input[@id='video-skip-start-time']"
    skip_end_element="//input[@id='video-skip-end-time']"
    recap_start_element="//input[@id='video-recap-start-time']"
    recap_end_element="//input[@id='video-recap-end-time']"
    start_session_element="//input[@id='video-skip-start-session']"
    end_session_element="//input[@id='video-recap-start-session']"

    # Information

    epaper_element="//input[@id='video-epaper-upload']"
    url_element="//input[@id='inputField']"
    url_start_element="//input[@id='video-url-linktym']"
    url_end_element="//input[@id='video-urlEnd-linksec']"

    # Status Setting
    enable_feature_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    enable_active_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    enable_slider_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    enable_title_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"


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
    choose_file_element="//input[@id='video-trailer-mp4-url']"
  


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
    search_element="//input[@class='rti--input w-100']"

    
    tamil_subtitle_element="(//input[@id='videoSubtitle'])[1]"
    english_element="(//input[@id='videoSubtitle'])[2]"
    malayalam_element="(//input[@id='videoSubtitle'])[3]"

    update_element="(//span[text()='Update Video'])[2]"

    


            
    def test_Edit_MP4(self,browser_setup):
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

        add_role= self.driver.find_element(By.XPATH, self.all_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_role)
        time.sleep(2)
        add_role.click()

        WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, self.dot_element))
        ).click()
    
    # Wait for edit_element to be clickable and click it
        # WebDriverWait(self.driver, 50).until(
        # EC.presence_of_element_located((By.XPATH, self.edit_element))
        # ).click()
    
        # # Hover over dot_element to reveal dropdown or submenu
        # menu = WebDriverWait(self.driver, 80).until(
        #     EC.visibility_of_element_located((By.XPATH, self.dot_element))
        # )
        
        # actions = ActionChains(self.driver)
        # actions.move_to_element(menu).perform()
        
        # # Wait for submenu (edit_element) to be visible and click it via JS
        # submenu = WebDriverWait(self.driver, 80).until(
        #     EC.visibility_of_element_located((By.XPATH, self.edit_element))
        # )
        # self.driver.execute_script("arguments[0].click();", submenu)

        try :
            length = 6
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
            length = 6
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
        des.clear()
        time.sleep(2)
        des.send_keys("A short description, often referred to as a shortdesc in documentation and technical writing, ")
        time.sleep(2)

        det=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.detail_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", det) 
        det.clear()
        time.sleep(2)
        det.send_keys("a concise summary or overview of a topic, concept, or product")
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
            category.clear()
            time.sleep(2)
            action.send_keys('Action').perform()
            action.send_keys(Keys.ENTER).perform()  
            time.sleep(1)
        except Exception as e:
           print(f"❌ Error Entering Details: {e}")


        try :
            drop_down1 = self.driver.find_element(By.XPATH, self.age_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
            # drop_down1.click()
            # time.sleep(2)
            select = Select(drop_down1)
            select.select_by_visible_text("18")
        except Exception as e:
           print(f"❌ Error selecting country code: {e}")



        lang=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.language_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",lang) 
        lang.click()
        time.sleep(2)
        lang.clear()
        time.sleep(1)
        action.send_keys('English').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)


        # Select user role Dropdown
        drop_down2 = self.driver.find_element(By.XPATH, self.rating_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down2) 
        time.sleep(2)
        select = Select(drop_down2)
        select.select_by_value("4")

      

# REACT 
       
        cast=WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.cast_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cast)
        time.sleep(2)
        cast.click()
        time.sleep(1)
        cast.clear()
        action.send_keys('Richard Roe').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)

     
       

        related=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.related_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",related) 
        related.click()
        time.sleep(2)
        related.clear()
        time.sleep(1)
        action.send_keys('Test video no Two').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)

        play=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.playlist_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play) 
        play.click()
        time.sleep(2)
        play.clear()
        time.sleep(1)
        action.send_keys('Kudumbasthan').perform()
        action.send_keys(Keys.ENTER).perform()  
        time.sleep(1)


        
# Free Duration
        try :
            dur=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.duration_element))
                )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dur)
            time.sleep(1)
            dur.clear()
            time.sleep(2)
            dur.send_keys("002431")
            time.sleep(2)
        except Exception as e:
           print(f"❌ Error Entering Details: {e}")

        toggle = self.driver.find_element(By.XPATH, self.duration_status_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle).perform()
        
        det=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.free_duration_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", det) 
        det.send_keys("000025")
        time.sleep(2)


    
 
# Intro time 
       
        star=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.skip_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",star)
        time.sleep(1)
        star.clear()
        time.sleep(2)
        star.send_keys("010400")
        time.sleep(2)

        send=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.skip_end_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",send)
        time.sleep(1)
        send.clear()
        time.sleep(2)
        send.send_keys("004000")
        time.sleep(2)

        rec=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.recap_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rec) 
        time.sleep(1)
        rec.clear()
        time.sleep(2)
        rec.send_keys("001229")
        time.sleep(2)

        rend=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.recap_end_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",rend)
        time.sleep(1)
        rend.clear()
        rend.send_keys("001830")
        time.sleep(2)

        ses=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.start_session_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ses)
        ses.clear()
        time.sleep(2) 
        ses.send_keys("002310")
        time.sleep(2)

        ssend=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.end_session_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ssend)
        time.sleep(1)
        ssend.clear()
        time.sleep(2)
        ssend.send_keys("004042")
        time.sleep(2)

                   
# Information

        pdf=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.epaper_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pdf)
        pdf.send_keys(self.pdfFile_path)
        time.sleep(2)

        ur=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ur)
        time.sleep(1)
        ur.clear()
        time.sleep(2)
        ur.send_keys("http://node-admin.webnexs.org/edit-video/83")
        time.sleep(2)

        st=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url_start_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", st) 
        time.sleep(1)
        st.clear()
        time.sleep(2)
        st.send_keys("000789")
        time.sleep(2)

        ul=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.url_end_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ul)
        time.sleep(1)
        ul.clear()
        time.sleep(2)
        ul.send_keys("000123")
        time.sleep(2)

# Status Setting

        toggle1 = self.driver.find_element(By.XPATH, self.enable_feature_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle1).perform()

         
        toggle2 = self.driver.find_element(By.XPATH, self.enable_active_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
        time.sleep(2)

        actions = ActionChains(self.driver)
        actions.double_click(toggle2).perform()
        time.sleep(2)



        toggle3 = self.driver.find_element(By.XPATH, self.enable_slider_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle3).perform()

        toggle4 = self.driver.find_element(By.XPATH, self.enable_title_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4) 
        time.sleep(2)  
        actions = ActionChains(self.driver)
        actions.double_click(toggle4).perform()


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

        
        mid=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.mid_sequence_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",mid)
        time.sleep(1)
        mid.clear()
        time.sleep(2)
        mid.send_keys("002312")
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
        time.sleep(1)
        select = Select(drop_down6)
        select.select_by_visible_text("Mp4 url")
        time.sleep(2)


        file=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.choose_file_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",file) 
        file.click()
        time.sleep(1)
        file.clear()
        file.send_keys("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4")
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
        time.sleep(2)
        select = Select(drop_down7)
        select.select_by_visible_text("2025")

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
        try :
            down8 = self.driver.find_element(By.XPATH, self.access_element)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",down8) 
            # time.sleep(2)
            # down8.click()
            # time.sleep(2)
            select = Select(down8)
            select.select_by_visible_text("Registered Users (Must register to watch)")
        except Exception as e:
            print(f"❌ Error Entering Details: {e}")


 # SEO 

        tit=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.page_title_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",tit)
        time.sleep(1)
        tit.clear()
        time.sleep(2)
        tit.send_keys("Tamilgun")
        time.sleep(2)

        web=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.website_url_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web) 
        time.sleep(1)
        web.clear()
        time.sleep(2)
        web.send_keys("https://tamilgun.group/tag/hd-movies/")
        time.sleep(2)

        dec=WebDriverWait(self.driver, 50).until(
               EC.presence_of_element_located((By.XPATH, self.descr_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dec) 
        time.sleep(1)
        dec.clear()
        time.sleep(2)
        dec.send_keys("Details. Tamilgun is a website known for offering access to the latest Tamil movies online")
        time.sleep(2)

        
# Search 

        sear=WebDriverWait(self.driver, 30).until(
               EC.presence_of_element_located((By.XPATH, self.search_element))
            )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sear)
        time.sleep(1)
        sear.clear()
        time.sleep(2)
        sear.send_keys("Movie")
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
        save_element.click()
        print("Updated successfully!")
        time.sleep(10)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="MP4 Access User details updated successfully.", attachment_type=AttachmentType.PNG)


    
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 



