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
class TestUser_custom:
   
    driver: WebDriver


     # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    roles_element="//span[text()='Roles']"
    all_role_element="//span[text()='All Roles']"

    dot_element="(//span[@class='editdropdown-button'])[1]"
    edit_element="(//span[text()='Edit'])[1]"


    name_element="//input[@id='inputField']"
    role_type_element="(//select[@id='selectField'])[1]"
    access_type_element="(//select[@id='selectField'])[2]"
   
    # Dashboard
    dash_checkbox1_element="(//input[@name='read'])[1]"
    dash_checkbox2_element="(//input[@name='add'])[1]"
    dash_checkbox3_element="(//input[@name='update'])[1]"
    dash_checkbox4_element="(//input[@name='delete'])[1]"

    # Master Video List
    master_checkbox1_element="(//input[@name='read'])[2]"
    master_checkbox2_element="(//input[@name='add'])[2]"
    master_checkbox3_element="(//input[@name='update'])[2]"
    master_checkbox4_element="(//input[@name='delete'])[2]"


    # Video Management
    video_checkbox1_element="(//input[@name='read'])[3]"
    video_checkbox2_element="(//input[@name='add'])[3]"
    video_checkbox3_element="(//input[@name='update'])[3]"
    video_checkbox4_element="(//input[@name='delete'])[3]"

    # Series
    series_checkbox1_element="(//input[@name='read'])[4]"
    series_checkbox2_element="(//input[@name='add'])[4]"
    series_checkbox3_element="(//input[@name='update'])[4]"
    series_checkbox4_element="(//input[@name='delete'])[4]"

    # Live Stream Management
    live_checkbox1_element="(//input[@name='read'])[5]"
    live_checkbox2_element="(//input[@name='add'])[5]"
    live_checkbox3_element="(//input[@name='update'])[5]"
    live_checkbox4_element="(//input[@name='delete'])[5]"

    # Audio Management 
    audio_checkbox1_element="(//input[@name='read'])[6]"
    audio_checkbox2_element="(//input[@name='add'])[6]"
    audio_checkbox3_element="(//input[@name='update'])[6]"
    audio_checkbox4_element="(//input[@name='delete'])[6]"

    # Artist Management
    artist_checkbox1_element="(//input[@name='read'])[7]"
    artist_checkbox2_element="(//input[@name='add'])[7]"
    artist_checkbox3_element="(//input[@name='update'])[7]"
    artist_checkbox4_element="(//input[@name='delete'])[7]"

    # User Management
    user_checkbox1_element="(//input[@name='read'])[8]"
    user_checkbox2_element="(//input[@name='add'])[8]"
    user_checkbox3_element="(//input[@name='update'])[8]"
    user_checkbox4_element="(//input[@name='delete'])[8]"

    # Language Management 
    lang_checkbox1_element="(//input[@name='read'])[9]"
    lang_checkbox2_element="(//input[@name='add'])[9]"
    lang_checkbox3_element="(//input[@name='update'])[9]"
    lang_checkbox4_element="(//input[@name='delete'])[9]"

    # Ads slider 
    slider_checkbox1_element="(//input[@name='read'])[10]"
    slider_checkbox2_element="(//input[@name='add'])[10]"
    slider_checkbox3_element="(//input[@name='update'])[10]"
    slider_checkbox4_element="(//input[@name='delete'])[10]"

    # Player Management
    player_checkbox1_element="(//input[@name='read'])[11]"
    player_checkbox2_element="(//input[@name='add'])[11]"
    player_checkbox3_element="(//input[@name='update'])[11]"
    player_checkbox4_element="(//input[@name='delete'])[11]"

    # Partner Management
    partner_checkbox1_element="(//input[@name='read'])[12]"
    partner_checkbox2_element="(//input[@name='add'])[12]"
    partner_checkbox3_element="(//input[@name='update'])[12]"
    partner_checkbox4_element="(//input[@name='delete'])[12]"
 
    # Page Management
    page_checkbox1_element="(//input[@name='read'])[13]"
    page_checkbox2_element="(//input[@name='add'])[13]"
    page_checkbox3_element="(//input[@name='update'])[13]"
    page_checkbox4_element="(//input[@name='delete'])[13]"

    # Plans Management
    plans_checkbox1_element="(//input[@name='read'])[14]"
    plans_checkbox2_element="(//input[@name='add'])[14]"
    plans_checkbox3_element="(//input[@name='update'])[14]"
    plans_checkbox4_element="(//input[@name='delete'])[14]"

    # Payment Management
    pay_checkbox1_element="(//input[@name='read'])[15]"
    pay_checkbox2_element="(//input[@name='add'])[15]"
    pay_checkbox3_element="(//input[@name='update'])[15]"
    pay_checkbox4_element="(//input[@name='delete'])[15]"

    # Analytics Management
    analytics_checkbox1_element="(//input[@name='read'])[16]"
    analytics_checkbox2_element="(//input[@name='add'])[16]"
    analytics_checkbox3_element="(//input[@name='update'])[16]"
    analytics_checkbox4_element="(//input[@name='delete'])[16]"

    # Settings Management
    settings_checkbox1_element="(//input[@name='read'])[17]"
    settings_checkbox2_element="(//input[@name='add'])[17]"
    settings_checkbox3_element="(//input[@name='update'])[17]"
    settings_checkbox4_element="(//input[@name='delete'])[17]"

    # ads Management 
    ads_checkbox1_element="(//input[@name='read'])[18]"
    ads_checkbox2_element="(//input[@name='add'])[18]"
    ads_checkbox3_element="(//input[@name='update'])[18]"
    ads_checkbox4_element="(//input[@name='delete'])[18]"

    # Contact Management 
    contact_checkbox1_element="(//input[@name='read'])[19]"
    contact_checkbox2_element="(//input[@name='add'])[19]"
    contact_checkbox3_element="(//input[@name='update'])[19]"
    contact_checkbox4_element="(//input[@name='delete'])[19]"

    # Logs Management 
    logs_checkbox1_element="(//input[@name='read'])[20]"
    logs_checkbox2_element="(//input[@name='add'])[20]"
    logs_checkbox3_element="(//input[@name='update'])[20]"
    logs_checkbox4_element="(//input[@name='delete'])[20]"

    # Menu Management 
    menu_checkbox1_element="(//input[@name='read'])[21]"
    menu_checkbox2_element="(//input[@name='add'])[21]"
    menu_checkbox3_element="(//input[@name='update'])[21]"
    menu_checkbox4_element="(//input[@name='delete'])[21]"

    # Storefront settings 
    store_checkbox1_element="(//input[@name='read'])[22]"
    store_checkbox2_element="(//input[@name='add'])[22]"
    store_checkbox3_element="(//input[@name='update'])[22]"
    store_checkbox4_element="(//input[@name='delete'])[22]"

    # Home Page Management 
    home_checkbox1_element="(//input[@name='read'])[23]"
    home_checkbox2_element="(//input[@name='add'])[23]"
    home_checkbox3_element="(//input[@name='update'])[23]"
    home_checkbox4_element="(//input[@name='delete'])[23]"

    # App Settings Management 
    app_checkbox1_element="(//input[@name='read'])[24]"
    app_checkbox2_element="(//input[@name='add'])[24]"
    app_checkbox3_element="(//input[@name='update'])[24]"
    app_checkbox4_element="(//input[@name='delete'])[24]"

    # Meta Setting Management 
    meta_checkbox1_element="(//input[@name='read'])[25]"
    meta_checkbox2_element="(//input[@name='add'])[25]"
    meta_checkbox3_element="(//input[@name='update'])[25]"
    meta_checkbox4_element="(//input[@name='delete'])[25]"

    # Roles Management 
    role_checkbox1_element="(//input[@name='read'])[26]"
    role_checkbox2_element="(//input[@name='add'])[26]"
    role_checkbox3_element="(//input[@name='update'])[26]"
    role_checkbox4_element="(//input[@name='delete'])[26]"

    # Registration Management
    register_checkbox1_element="(//input[@name='read'])[28]"
    register_checkbox2_element="(//input[@name='add'])[28]"
    register_checkbox3_element="(//input[@name='update'])[28]"
    register_checkbox4_element="(//input[@name='delete'])[28]"

    # Playout Management
    playout_checkbox1_element="(//input[@name='read'])[29]"
    playout_checkbox2_element="(//input[@name='add'])[29]"
    playout_checkbox3_element="(//input[@name='update'])[29]"
    playout_checkbox4_element="(//input[@name='delete'])[29]"

    # Video Category Management
    cate_checkbox1_element="(//input[@name='read'])[30]"
    cate_checkbox2_element="(//input[@name='add'])[30]"
    cate_checkbox3_element="(//input[@name='update'])[30]"
    cate_checkbox4_element="(//input[@name='delete'])[30]"

    # Video Playlist Management
    playlist_checkbox1_element="(//input[@name='read'])[31]"
    playlist_checkbox2_element="(//input[@name='add'])[31]"
    playlist_checkbox3_element="(//input[@name='update'])[31]"
    playlist_checkbox4_element="(//input[@name='delete'])[31]"

    # Live stream Category Management
    live_stream_checkbox1_element="(//input[@name='read'])[32]"
    live_stream_checkbox2_element="(//input[@name='add'])[32]"
    live_stream_checkbox3_element="(//input[@name='update'])[32]"
    live_stream_checkbox4_element="(//input[@name='delete'])[32]"

    # Audio Category Management
    audio_category_checkbox1_element="(//input[@name='read'])[33]"
    audio_category_checkbox2_element="(//input[@name='add'])[33]"
    audio_category_checkbox3_element="(//input[@name='update'])[33]"
    audio_category_checkbox4_element="(//input[@name='delete'])[33]"

    # Audio Album Management
    album_checkbox1_element="(//input[@name='read'])[34]"
    album_checkbox2_element="(//input[@name='add'])[34]"
    album_checkbox3_element="(//input[@name='update'])[34]"
    album_checkbox4_element="(//input[@name='delete'])[34]"

    # Import/Export Management  
    import_checkbox1_element="(//input[@name='read'])[35]"
    import_checkbox2_element="(//input[@name='add'])[35]"
    import_checkbox3_element="(//input[@name='update'])[35]"
    import_checkbox4_element="(//input[@name='delete'])[35]"

    submit_element="//span[text()='Update Role']"




    def test_User_Custom(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.all_role_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.dot_element))
            )
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.edit_element))
            )
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

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
        select.select_by_visible_text("Custom")

        # DashBoard
        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.dash_checkbox1_element))).click()
        self.driver.find_element(By.XPATH, self.dash_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.dash_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.dash_checkbox4_element).click()

        # Master Video List 
        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.master_checkbox1_element))).click()
        self.driver.find_element(By.XPATH, self.master_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.master_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.master_checkbox4_element).click()

        # Video Management 
        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.video_checkbox1_element))).click()
        self.driver.find_element(By.XPATH, self.video_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.video_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.video_checkbox4_element).click()

        # # Series & Episode 
        # WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.series_checkbox1_element))).click()
        # self.driver.find_element(By.XPATH, self.series_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.series_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.series_checkbox4_element).click()

        # Live stream Management 
        WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.live_checkbox1_element))).click()
        self.driver.find_element(By.XPATH, self.live_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.live_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.live_checkbox4_element).click()

        # # Audio Management 
        # aio=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.audio_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", aio)
        # aio.click()
        # self.driver.find_element(By.XPATH, self.audio_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.audio_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.audio_checkbox4_element).click()

        # Artist Management 
        art=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.artist_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", art)
        art.click()
        self.driver.find_element(By.XPATH, self.artist_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.artist_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.artist_checkbox4_element).click()

        # User Management
        use=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.user_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", use)
        use.click()
        self.driver.find_element(By.XPATH, self.user_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.user_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.user_checkbox4_element).click()

        # # Language Management
        # lan=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.lang_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lan)
        # lan.click()
        # self.driver.find_element(By.XPATH, self.lang_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.lang_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.lang_checkbox4_element).click()

        # Ads Slider
        ad=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.slider_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ad)
        ad.click()
        self.driver.find_element(By.XPATH, self.slider_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.slider_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.slider_checkbox4_element).click() 

        # # Player Management
        # pla=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.player_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pla)
        # pla.click()
        # self.driver.find_element(By.XPATH, self.player_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.player_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.player_checkbox4_element).click()

        # Partner Management 
        par=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.partner_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", par)
        par.click()
        self.driver.find_element(By.XPATH, self.partner_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.partner_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.partner_checkbox4_element).click()

        # # Page Management 
        # pag=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.page_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pag)
        # pag.click()
        # self.driver.find_element(By.XPATH, self.page_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.page_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.page_checkbox4_element).click()

        # Plans Management 
        pan=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.plans_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan)
        pan.click()
        self.driver.find_element(By.XPATH, self.plans_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.plans_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.plans_checkbox4_element).click()

        # Payment Management 
        ment=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.pay_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ment)
        ment.click()
        self.driver.find_element(By.XPATH, self.pay_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.pay_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.pay_checkbox4_element).click()

        # # Analytics Management 
        # ana=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.analytics_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ana)
        # ana.click()
        # self.driver.find_element(By.XPATH, self.analytics_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.analytics_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.analytics_checkbox4_element).click()

        # Settings Management
        set=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.settings_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", set)
        set.click()
        self.driver.find_element(By.XPATH, self.settings_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.settings_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.settings_checkbox4_element).click()

        # Ads Management 
        ds=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.ads_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ds)
        ds.click()
        self.driver.find_element(By.XPATH, self.ads_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.ads_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.ads_checkbox4_element).click()

        # Contact Management 
        tact=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.contact_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tact)
        tact.click()
        self.driver.find_element(By.XPATH, self.contact_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.contact_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.contact_checkbox4_element).click()

        # # Logs Management 
        # lg=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.logs_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lg)
        # lg.click()
        # self.driver.find_element(By.XPATH, self.logs_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.logs_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.logs_checkbox4_element).click()

        #Menu Management 
        men=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.menu_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", men)
        men.click()
        self.driver.find_element(By.XPATH, self.menu_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.menu_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.menu_checkbox4_element).click()

        # Store Front Settings
        sto=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.store_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sto) 
        sto.click()
        self.driver.find_element(By.XPATH, self.store_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.store_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.store_checkbox4_element).click()

        # # Home Page Management 
        # hom=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.home_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hom) 
        # hom.click()
        # self.driver.find_element(By.XPATH, self.home_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.home_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.home_checkbox4_element).click()

        # App Settings Management 
        setti=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.app_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", setti) 
        setti.click()
        self.driver.find_element(By.XPATH, self.app_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.app_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.app_checkbox4_element).click()

        # Meta Settings Management 
        met=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.meta_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", met)
        met.click()
        self.driver.find_element(By.XPATH, self.meta_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.meta_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.meta_checkbox4_element).click()

        # Roles Management 
        rol=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.role_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rol)
        rol.click()
        self.driver.find_element(By.XPATH, self.role_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.role_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.role_checkbox4_element).click()

        # # Registration Management 
        # reg=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.register_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reg)
        # reg.click()
        # self.driver.find_element(By.XPATH, self.register_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.register_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.register_checkbox4_element).click()

        # Playout Management 
        plout=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.playout_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plout)
        plout.click()
        self.driver.find_element(By.XPATH, self.playout_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.playout_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.playout_checkbox4_element).click()

        # Video Category Management 
        vicat=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.cate_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vicat)
        vicat.click()
        self.driver.find_element(By.XPATH, self.cate_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.cate_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.cate_checkbox4_element).click()

        # # Video Playlist Management 
        # pla=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.playlist_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pla)
        # pla.click()
        # self.driver.find_element(By.XPATH, self.playlist_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.playlist_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.playlist_checkbox4_element).click()

        # Live Stream Category Management 
        listr=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.live_stream_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", listr)
        listr.click()
        self.driver.find_element(By.XPATH, self.live_stream_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.live_stream_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.live_stream_checkbox4_element).click()

        # Audio Category Management 
        aucat=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.audio_category_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", aucat)
        aucat.click()
        self.driver.find_element(By.XPATH, self.audio_category_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.audio_category_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.audio_category_checkbox4_element).click()

        # # Audio Album Management 
        # alb=WebDriverWait(self.driver, 50).until(
        #         EC.presence_of_element_located((By.XPATH, self.album_checkbox1_element)))
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", alb)
        # alb.click()
        # self.driver.find_element(By.XPATH, self.album_checkbox2_element).click()
        # time.sleep(1)
        # self.driver.find_element(By.XPATH, self.album_checkbox3_element).click()
        # self.driver.find_element(By.XPATH, self.album_checkbox4_element).click()

        # Import/Export Management 
        im=WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.import_checkbox1_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", im)
        im.click()
        self.driver.find_element(By.XPATH, self.import_checkbox2_element).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, self.import_checkbox3_element).click()
        self.driver.find_element(By.XPATH, self.import_checkbox4_element).click()

             # update or save element
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="User permission Custom  details Updated successfully.", attachment_type=AttachmentType.PNG)
       
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 

