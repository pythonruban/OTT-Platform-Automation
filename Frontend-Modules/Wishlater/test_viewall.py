import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

# XPath and ID mappings
xpaths = {
    # Login
    "sign_in_btn": "home-signin",  # ID
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "submit_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",

    # Action steps
    "continue_watching": "//a[@class='homeListButton m-0 px-2 py-2 bgButton d-flex align-items-center justify-content-center bannerButton position-relative']",
    "video_wishlist": "//button[@id='video-wishlist']",
    "tt1": "//img[@id='TT-2']",
    "wishlist": "//a[@id='wishlist']",
    
}

@pytest.fixture
def setup_driver():
    driver = webdriver.Firefox(service=FirefoxService())
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.feature("Manual Step-by-Step Home Flow with Firefox + Scroll + Wait")
def test_wishlistremove(setup_driver):
    driver = setup_driver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open homepage
        driver.get(ReadConfig.getHomePageURL())
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="01_Homepage_Loaded", attachment_type=AttachmentType.PNG)
        

        # Step 2: Click sign in (ID)
        wait.until(EC.element_to_be_clickable((By.ID, xpaths["sign_in_btn"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="02_Clicked_SignIn", attachment_type=AttachmentType.PNG)
        

        # Step 3: Enter credentials
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
        driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="03_Entered_Credentials", attachment_type=AttachmentType.PNG)
        

        # Step 4: Click login
        driver.find_element(By.XPATH, xpaths["submit_btn"]).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="04_Submit_Login", attachment_type=AttachmentType.PNG)
        

        # Step 5: Choose profile
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["choose_profile"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="05_Selected_Profile", attachment_type=AttachmentType.PNG)
        

        # Step 6: Wait for homepage to load (based on continue watching element)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["continue_watching"])))
            time.sleep(10)
            allure.attach(driver.get_screenshot_as_png(), name="06_Homepage_Ready", attachment_type=AttachmentType.PNG)
            
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="06_Home_Not_Ready", attachment_type=AttachmentType.PNG)
            raise Exception("❌ Homepage content not loaded in time.")

        # Step 7: Click Continue Watching
        elem = driver.find_element(By.XPATH, xpaths["continue_watching"])
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["continue_watching"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="07_Clicked_Continue_Watching", attachment_type=AttachmentType.PNG)
        

        # Step 8: Click Video Wishlist
        elem = driver.find_element(By.XPATH, xpaths["video_wishlist"])
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["video_wishlist"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="08_Clicked_Video_Wishlist", attachment_type=AttachmentType.PNG)
        

        # Step 9: Click TT-2
        elem = driver.find_element(By.XPATH, xpaths["tt1"])
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["tt1"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="09_Clicked_TT1", attachment_type=AttachmentType.PNG)
        

        # Step 10: Click Wishlist
        elem = driver.find_element(By.XPATH, xpaths["wishlist"])
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["wishlist"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="10_Clicked_Wishlist", attachment_type=AttachmentType.PNG)
        

       

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="ERROR_Final_Crash", attachment_type=AttachmentType.PNG)
        print(f"❌ Exception occurred: {e}")
        raise

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver not initialized.")