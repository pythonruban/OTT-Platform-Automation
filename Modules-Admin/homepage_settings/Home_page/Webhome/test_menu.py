import time
import allure
import pytest
import os

 
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
class TestWeb_Home:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    home_element="//span[text()='Home Settings']"
    home_page_element="//span[text()='HomePage Settings']"

    web_page_element="//button[@id='nav-home-tab']"
    pagination_element="(//input[@id='inputField'])[1]"
    limit_value_element="(//input[@id='inputField'])[2]"
    submit_element="(//span[text()='Submit'])[1]"



    feature_element="(//span[@class='admin-slider position-absolute admin-round '])[1]"
    video_base_element="(//span[@class='admin-slider position-absolute admin-round '])[2]"
    artist_element="(//span[@class='admin-slider position-absolute admin-round '])[3]"
    latest_series_element="(//span[@class='admin-slider position-absolute admin-round '])[4]"
    continue_element="(//span[@class='admin-slider position-absolute admin-round '])[5]"
    video_category_element="(//span[@class='admin-slider position-absolute admin-round '])[6]"
    single_element="(//span[@class='admin-slider position-absolute admin-round '])[7]"
    choose_element="//select[@id='single_series_id']"
    save_single_element="//button[text()='Save Single Series']"
    series_genre_element="(//span[@class='admin-slider position-absolute admin-round '])[8]"
    series_based_element="(//span[@class='admin-slider position-absolute admin-round '])[9]"
    live_element="(//span[@class='admin-slider position-absolute admin-round '])[10]"
    live_cate_element="(//span[@class='admin-slider position-absolute admin-round '])[11]"
    live_stream_element="(//span[@class='admin-slider position-absolute admin-round '])[12]"
    audios_element="(//span[@class='admin-slider position-absolute admin-round '])[13]"
    audio_album_element="(//span[@class='admin-slider position-absolute admin-round '])[14]"
    audio_genre_element="(//span[@class='admin-slider position-absolute admin-round '])[15]"
    audio_base_genre_element="(//span[@class='admin-slider position-absolute admin-round '])[16]"
    latest_element="(//span[@class='admin-slider position-absolute admin-round '])[17]"
    linear_element="(//span[@class='admin-slider position-absolute admin-round '])[18]"
    publish_video_element="(//span[@class='admin-slider position-absolute admin-round '])[19]"
    pubish_live_element="(//span[@class='admin-slider position-absolute admin-round '])[20]"
    
    content_element="(//span[@class='admin-slider position-absolute admin-round '])[21]"
    channel_element="(//span[@class='admin-slider position-absolute admin-round '])[22]"
    individual_element="(//span[@class='admin-slider position-absolute admin-round '])[23]"
    individual_channel_element="(//span[@class='admin-slider position-absolute admin-round '])[24]"
    latest_view_element="(//span[@class='admin-slider position-absolute admin-round '])[25]"
    latest_view_epi_element="(//span[@class='admin-slider position-absolute admin-round '])[26]"
    latest_view_live_element="(//span[@class='admin-slider position-absolute admin-round '])[27]"
    latest_view_audio_element="(//span[@class='admin-slider position-absolute admin-round '])[28]"
    rec_video_element="(//span[@class='admin-slider position-absolute admin-round '])[29]"
    rec_video_user_element="(//span[@class='admin-slider position-absolute admin-round '])[30]"
    rec_country_element="(//span[@class='admin-slider position-absolute admin-round '])[31]"
    all_language_element="(//span[@class='admin-slider position-absolute admin-round '])[32]"
    top_element="(//span[@class='admin-slider position-absolute admin-round '])[33]"



    save_element="//span[text()='Save Web Settings']"

    
    def test_Web_Home(self,browser_setup):
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
        WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.home_element)))
        user = self.driver.find_element(By.XPATH, self.home_element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", user)
        time.sleep(2)
        user.click()

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.home_page_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        web=WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.web_page_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",web)
        time.sleep(2)
        web.click()

        des=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.pagination_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",des) 
        des.clear()
        time.sleep(1)
        des.send_keys("8")
        time.sleep(3)

        lim=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.limit_value_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",lim) 
        lim.clear()
        time.sleep(1)
        lim.send_keys("15")
        time.sleep(3)

        sub=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.submit_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sub) 
        sub.click()
        time.sleep(2)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Pagination and limit updated successfully.", attachment_type=AttachmentType.PNG)


        
        try:
            toggle1 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.feature_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle1)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle1).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle2 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.video_base_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle2)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle2).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle3 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.artist_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle3)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle3).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle4 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_series_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle4)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle4).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle5 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.continue_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle5)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle5).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle6 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.video_category_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle6)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle6).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
        try:
            toggle33 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.single_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle33)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle33).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
            # Select user role Dropdown
        drop_down1= WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.choose_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",drop_down1) 
        time.sleep(2)
        select = Select(drop_down1)
        select.select_by_visible_text("Choose a Series")


        sa=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.save_single_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",sa)
        sa.click() 

        try:
            toggle7 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.series_genre_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle7)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle7).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle8 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.series_based_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle8)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle8).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle9 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.live_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle9)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle9).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle10 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.live_cate_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle10)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle10).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle11 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.live_stream_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle11)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle11).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
            
        try:
            toggle32 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.audios_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle32)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle32).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle12 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.audio_album_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle12)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle12).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle13 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.audio_genre_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle13)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle13).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle14 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.audio_base_genre_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle14)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle14).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle15 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle15)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle15).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle16 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.linear_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle16)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle16).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle17 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.publish_video_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle17)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle17).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle18 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.pubish_live_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle18)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle18).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle19 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.content_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle19)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle19).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle20 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.channel_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle20)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle20).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle21 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.individual_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle21)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle21).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle22 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.individual_channel_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle22)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle22).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle23 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_view_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle23)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle23).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle24 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_view_epi_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle24)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle24).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle25=WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_view_live_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle25)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle25).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle26 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.latest_view_audio_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle26)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle26).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))


        try:
            toggle27 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.rec_video_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle27)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle27).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle28 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.rec_video_user_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle28)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle28).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle29 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.rec_country_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle29)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle29).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle30 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.all_language_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle30)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle30).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

        try:
            toggle31 =WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.top_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle31)
            time.sleep(2)

            # Perform double-click
            actions = ActionChains(self.driver)
            actions.double_click(toggle31).perform()
            time.sleep(2)
        except Exception as e:
            print("An unexpected error occurred:", str(e))

    
        save=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.save_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save) 
        save.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name="Home page Settings Web home page details Added successfully.", attachment_type=AttachmentType.PNG)
        
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
        


































      