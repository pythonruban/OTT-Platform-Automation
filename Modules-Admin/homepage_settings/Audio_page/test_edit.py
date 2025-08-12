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
class TestEdit_Audio:
   
    driver: WebDriver

      # Define the elements
    email_element = "(//input[@name='email'])[2]"
    password_element = "//input[@name='password']"
    login_element = "//span[text()='Login']"
    dashboard_element = "//span[normalize-space()='Dashboard']" #XPATH

    home_element="//span[text()='Home Settings']"
    audio_element="//span[text()='AudioPage Settings']"

    order_audio_element="//span[text()='Order Audio Page']"

    latest_dot_element="(//span[@class='editdropdown-button'])[1]"
    latest_edit_element="(//span[text()='Edit'])[1]"
    
    # Latest Audio
    audio_header_element="(//input[@id='inputField'])[1]"
    audio_url_element="(//input[@id='inputField'])[2]"
    audio_update_element="//span[text()='Update Order']"
    audio_back_element="//p[@class=' d-inline  theme-text-color   admin-input-title d-block position-relative']"

    # Audio Album
    aual_dot_element="(//span[@class='editdropdown-button'])[2]"
    aual_edit_element="(//span[text()='Edit'])[2]"
    aual_header_element="(//input[@id='inputField'])[1]"
    aual_slug_element="(//input[@id='inputField'])[2]"
    aual_update_element="//span[text()='Update Order']"
    aual_back_element="//p[text()='Back']"

    # Artist
    art_dot_element="(//span[@class='editdropdown-button'])[3]"
    art_edit_element="(//span[text()='Edit'])[3]"
    art_header_element="(//input[@id='inputField'])[1]" 
    art_slug_element="(//input[@id='inputField'])[2]"
    art_update_element="//span[text()='Update Order']"
    art_back_element="//p[text()='Back']"

    # Audio Genre
    auge_dot_element="(//span[@class='editdropdown-button'])[4]"
    auge_edit_element="(//span[text()='Edit'])[4]"
    auge_header_element="(//input[@id='inputField'])[1]"
    auge_slug_element="(//input[@id='inputField'])[2]"
    auge_update_element="//span[text()='Update Order']"
    auge_back_element="//p[text()='Back']"

    # Audio Based On Genre
    bage_dot_element="(//span[@class='editdropdown-button'])[5]"
    bage_edit_element="(//span[text()='Edit'])[5]"
    bage_header_element="(//input[@id='inputField'])[1]"
    bage_slug_element="(//input[@id='inputField'])[2]"
    bage_update_element="//span[text()='Update Order']"
    bage_back_element="//p[text()='Back']"

    # Audio Based On Song Writer
    bawr_dot_element="(//span[@class='editdropdown-button'])[6]"
    bawr_edit_element="(//span[text()='Edit'])[6]"
    bawr_header_element="(//input[@id='inputField'])[1]"
    bawr_slug_element="(//input[@id='inputField'])[2]"
    bawr_update_element="//span[text()='Update Order']"
    bawr_back_element="//p[text()='Back']"

    
    # Audio Based On musician
    musi_dot_element="(//span[@class='editdropdown-button'])[7]"
    musi_edit_element="(//span[text()='Edit'])[7]"
    musi_name_element="(//input[@id='inputField'])[1]"
    musi_url_element="(//input[@id='inputField'])[2]"
    musi_update_element="//span[text()='Update Order']"
    musi_back_element="//p[text()='Back']"

    # Audio Based on Albums
    baalb_dot_element="(//span[@class='editdropdown-button'])[8]"
    baalb_edit_element="(//span[text()='Edit'])[8]"
    baalb_header_element="(//input[@id='inputField'])[1]"
    baalb_slug_element="(//input[@id='inputField'])[2]"
    baalb_update_element="//span[text()='Update Order']"
    baalb_back_element="//p[text()='Back']"

    # Audio Based On Language
    balan_dot_element="(//span[@class='editdropdown-button'])[9]"
    balan_edit_element="(//span[text()='Edit'])[9]"
    balan_header_element="(//input[@id='inputField'])[1]"
    balan_slug_element="(//input[@id='inputField'])[2]"
    balan_update_element="//span[text()='Update Order']"
    balan_back_element="//p[text()='Back']"

    # Recently Played
    repay_dot_element="(//span[@class='editdropdown-button'])[10]"
    repay_edit_element="(//span[text()='Edit'])[10]"
    repay_header_element="(//input[@id='inputField'])[1]"
    repay_slug_element="(//input[@id='inputField'])[2]"
    repay_update_element="//span[text()='Update Order']"
    repay_back_element="//p[text()='Back']" 

    # Latest Viewed Audios
    lavi_dot_element="(//span[@class='editdropdown-button'])[11]"
    lavi_edit_element="(//span[text()='Edit'])[11]"
    lavi_header_element="(//input[@id='inputField'])[1]"
    lavi_slug_element="(//input[@id='inputField'])[2]"
    lavi_update_element="//span[text()='Update Order']"
    lavi_back_element="//p[text()='Back']"

    # Musician
    mui_dot_element="(//span[@class='editdropdown-button'])[12]"
    mui_edit_element="(//span[text()='Edit'])[12]"
    mui_header_element="(//input[@id='inputField'])[1]"
    mui_slug_element="(//input[@id='inputField'])[2]"
    mui_update_element="//span[text()='Update Order']"
    mui_back_element="//p[text()='Back']"

    # Song Writer
    sowr_dot_element="(//span[@class='editdropdown-button'])[13]"
    sowr_edit_element="(//span[text()='Edit'])[13]"
    sowr_header_element="(//input[@id='inputField'])[1]"
    sowr_slug_element="(//input[@id='inputField'])[2]"
    sowr_update_element="//span[text()='Update Order']"
    sowr_back_element="//p[text()='Back']"

    # Music Station
    muon_dot_element="(//span[@class='editdropdown-button'])[14]"
    muon_edit_element="(//span[text()='Edit'])[14]"
    muon_header_element="(//input[@id='inputField'])[1]"
    muon_slug_element="(//input[@id='inputField'])[2]"
    muon_update_element="//span[text()='Update Order']"
    muon_back_element="//p[text()='Back']"

    # Playlist
    plst_dot_element="(//span[@class='editdropdown-button'])[15]"
    plst_edit_element="(//span[text()='Edit'])[15]"
    plst_header_element="(//input[@id='inputField'])[1]"
    plst_slug_element="(//input[@id='inputField'])[2]"
    plst_update_element="//span[text()='Update Order']"
    plst_back_element="//p[text()='Back']"
    



    def test_Edit_Audio(self,browser_setup):
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

        ro=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.audio_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ro)
        time.sleep(2)
        ro.click()

        order=WebDriverWait(self.driver, 120).until(EC.visibility_of_element_located((By.XPATH, self.order_audio_element)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", order)
        time.sleep(2)
        
        
        # Audio Album
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.aual_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.aual_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        he=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.aual_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", he) 
        time.sleep(2)
        he.clear()
        time.sleep(1)
        he.send_keys("Audio Albums")
        time.sleep(2)

        asl=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.aual_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", asl) 
        time.sleep(1)
        asl.clear()
        asl.send_keys("audio-albums")
        time.sleep(2)

        ue=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.aual_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ue)
        ue.click() 
        time.sleep(5)

        ak=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.aual_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ak)
        ak.click() 
        time.sleep(3)

        
        # # Latest Audio 

        # try:
        #     # Wait for and find the dot element
        #     dot_elem = WebDriverWait(self.driver, 30).until(
        #         EC.presence_of_element_located((By.XPATH, self.latest_dot_element))
        #     )
        #     self.driver.execute_script("arguments[0].click();", dot_elem)

        #     # Wait for and find the edit element
        #     edit_elem = WebDriverWait(self.driver, 80).until(
        #         EC.presence_of_element_located((By.XPATH, self.latest_edit_element))
        #     )
        #     self.driver.execute_script("arguments[0].click();", edit_elem)
        # except TimeoutException as e:
        #     print(f"[ERROR] Timeout while waiting for elements: {e}")
        # except Exception as e:
        #     print(f"[ERROR] Unexpected exception occurred: {e}")

        # des=WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, self.audio_header_element))
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",des) 
        # time.sleep(2)
        # des.clear()
        # time.sleep(1)
        # des.send_keys("Latest Audios")
        # time.sleep(2)

        # ur=WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, self.audio_url_element))
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ur) 
        # time.sleep(2)
        # ur.clear()
        # ur.send_keys("audios")
        # time.sleep(2)

        # up=WebDriverWait(self.driver, 120).until(
        #     EC.presence_of_element_located((By.XPATH, self.audio_update_element))
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",up)
        # up.click()
        # time.sleep(5) 

        # ba=WebDriverWait(self.driver, 120).until(
        #     EC.presence_of_element_located((By.XPATH, self.audio_back_element))
        # )
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ba)
        # ba.click() 
        # time.sleep(3)


        # Artist 
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.art_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.art_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        rd=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.art_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rd) 
        time.sleep(2)
        rd.clear()
        time.sleep(1)
        rd.send_keys("Artist")
        time.sleep(3)

        td=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.art_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", td) 
        time.sleep(1)
        td.clear()
        td.send_keys("artists")
        time.sleep(3)

        de=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.art_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",de)
        de.click() 
        time.sleep(5)

        ck=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.art_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ck)
        ck.click()
        time.sleep(3)

        # Audio Genre
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.auge_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.auge_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        es=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.auge_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", es) 
        time.sleep(1)
        es.clear()
        time.sleep(1)
        es.send_keys("Audio Genre")
        time.sleep(3)

        ru=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.auge_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ru) 
        time.sleep(2)
        ru.clear()
        time.sleep(1)
        ru.send_keys("audio-genre")
        time.sleep(3)

        pu=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.auge_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pu)
        pu.click() 
        time.sleep(5)

        ab=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.auge_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ab)
        ab.click() 
        time.sleep(2)

        # Audio Based On Genre
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.bage_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.bage_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        bg=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.bage_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bg) 
        time.sleep(2)
        bg.clear()
        time.sleep(1)
        bg.send_keys("Audio Based on Genre")
        time.sleep(3)

        ae=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.bage_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ae) 
        time.sleep(1)
        ae.clear()
        time.sleep(1)
        ae.send_keys("audio-genre/:slug")
        time.sleep(3)

        ge=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.bage_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ge)
        ge.click() 
        time.sleep(5)

        ag=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.bage_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ag)
        ag.click() 
        time.sleep(3)

        # Audio Based On Song Writer
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.bawr_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.bawr_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        bw=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.bawr_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bw) 
        time.sleep(2)
        bw.clear()
        time.sleep(1)
        bw.send_keys("Audio Based on Song Writer")
        time.sleep(3)

        ar=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.bawr_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ar) 
        time.sleep(2)
        ar.clear()
        time.sleep(1)
        ar.send_keys("")
        time.sleep(3)

        wa=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.bawr_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wa)
        wa.click() 
        time.sleep(5)

        aw=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.bawr_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", aw)
        aw.click() 
        time.sleep(3)

      
        # Audio Based On Musician
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.musi_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.musi_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        mi=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.musi_name_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",mi) 
        time.sleep(2)
        mi.clear()
        time.sleep(1)
        mi.send_keys("Audio Based On Musician")
        time.sleep(3)

        ci=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.musi_url_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ci) 
        time.sleep(2)
        ci.clear()
        time.sleep(1)
        ci.send_keys("")
        time.sleep(3)

        tr=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.musi_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",tr) 
        tr.click()
        time.sleep(5)

        rt=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.musi_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",rt) 
        rt.click()
        time.sleep(3)

        
        # Audio Based On Album
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.baalb_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.baalb_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        bl=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.baalb_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bl) 
        time.sleep(2)
        bl.clear()
        time.sleep(1)
        bl.send_keys("Audio Based on Album")
        time.sleep(3)

        sb=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.baalb_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sb) 
        time.sleep(1)
        sb.clear()
        time.sleep(1)
        sb.send_keys("")
        time.sleep(3)

        lt=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.baalb_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lt)
        lt.click() 
        time.sleep(5)

        lb=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.baalb_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",lb)
        lb.click() 
        time.sleep(3)

        # Audio Based On Language 
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.balan_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.balan_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ln=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.balan_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ln) 
        time.sleep(2)
        ln.clear()
        time.sleep(1)
        ln.send_keys("Audio Based on Language")
        time.sleep(3)

        nl=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.balan_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",nl) 
        time.sleep(2)
        nl.clear()
        nl.send_keys("")
        time.sleep(3)

        nu=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.balan_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nu)
        nu.click()
        time.sleep(5) 

        al=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.balan_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", al)
        al.click() 
        time.sleep(3)

        # Recently Played 
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.repay_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.repay_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ry=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.repay_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ry) 
        time.sleep(1)
        ry.clear()
        time.sleep(1)
        ry.send_keys("Recently Played")
        time.sleep(3)

        ay=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.repay_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ay) 
        time.sleep(1)
        ay.clear()
        ay.send_keys("")
        time.sleep(3)

        rp=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.repay_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",rp)
        rp.click() 
        time.sleep(5)

        pa=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.repay_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",pa)
        pa.click() 
        time.sleep(3)

        # Latest Viewed Audios
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.lavi_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.lavi_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        dv=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.lavi_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dv) 
        time.sleep(2)
        dv.clear()
        time.sleep(1)
        dv.send_keys("Latest Viewed Audios")
        time.sleep(3)

        cv=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.lavi_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",cv) 
        time.sleep(1)
        cv.clear()
        cv.send_keys("")
        time.sleep(3)

        av=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.lavi_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",av)
        av.click() 
        time.sleep(5)

        bv=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.lavi_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",bv)
        bv.click() 
        time.sleep(3)

        # Musician
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.mui_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.mui_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ai=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.mui_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ai) 
        time.sleep(2)
        ai.clear()
        time.sleep(1)
        ai.send_keys("Musician")
        time.sleep(3)

        bi=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.mui_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bi) 
        time.sleep(2)
        bi.clear()
        bi.send_keys("")
        time.sleep(3)

        ci=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.mui_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ci)
        ci.click() 
        time.sleep(5)

        di=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.mui_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", di)
        di.click() 
        time.sleep(3)

        # Song Writer
    
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.sowr_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.sowr_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ei=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.sowr_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ei) 
        time.sleep(2)
        ei.clear()
        time.sleep(1)
        ei.send_keys("Song Writer")
        time.sleep(3)

        fi=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.sowr_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fi) 
        time.sleep(2)
        fi.clear()
        fi.send_keys("")
        time.sleep(3)

        gi=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.sowr_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gi)
        gi.click() 
        time.sleep(5)

        hi=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.sowr_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hi)
        hi.click() 
        time.sleep(3)

        # Music Station        
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.muon_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.muon_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ii=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.muon_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ii) 
        time.sleep(1)
        ii.clear()
        time.sleep(1)
        ii.send_keys("Music Station")
        time.sleep(3)

        ji=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.muon_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ji) 
        time.sleep(1)
        ji.clear()
        ji.send_keys("")
        time.sleep(3)

        ki=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.muon_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ki)
        ki.click() 
        time.sleep(5)

        li=WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, self.muon_back_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", li)
        li.click()
        time.sleep(3) 

        # Playlist 
        
        try:
            # Wait for and find the dot element
            dot_elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, self.plst_dot_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dot_elem)
            self.driver.execute_script("arguments[0].click();", dot_elem)

            # Wait for and find the edit element
            edit_elem = WebDriverWait(self.driver, 80).until(
                EC.presence_of_element_located((By.XPATH, self.plst_edit_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_elem)
            self.driver.execute_script("arguments[0].click();", edit_elem)
        except TimeoutException as e:
            print(f"[ERROR] Timeout while waiting for elements: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected exception occurred: {e}")

        ni=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.plst_header_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ni) 
        time.sleep(2)
        ni.clear()
        time.sleep(1)
        ni.send_keys("Playlist")
        time.sleep(3)

        oi=WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.plst_slug_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", oi) 
        time.sleep(2)
        oi.clear()
        oi.send_keys("")
        time.sleep(3)

    
        save_element=WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.XPATH, self.plst_update_element))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_element) 
        time.sleep(2)  
        save_element.click()
        time.sleep(3)
        allure.attach(self.driver.get_full_page_screenshot_as_png(), name=" Audio Page Settings in Home Page Settings details Updated successfully.", attachment_type=AttachmentType.PNG)
    

                
    def teardown_class(self):
        """Close the browser"""
        try:
            self.driver.quit()
        except AttributeError:
            print("Driver was not initialized.")  
 
 
        



      



        


