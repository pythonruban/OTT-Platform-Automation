import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    # Login
    "sign_in_btn": "home-signin",  # ID
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "submit_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "tt1": "//img[@id='TT-2']",

    # New Profile Steps
    "choose_profile_btn": "choose-profile",             # ID
    "add_multi_user_btn": "add-multi-user",             # ID
    "profile_img_upload": "profileImageUpload",         # ID
    "profile_username": "profile-username",             # ID
    "profile_create_btn": "profile-create"              # ID
}

@pytest.fixture
def setup_driver():
    driver = webdriver.Firefox(service=FirefoxService())
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.feature("Home Flow with Profile Creation (No Logout)")
def test_multiple_profile_add(setup_driver: WebDriver):
    driver = setup_driver
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Open homepage
        driver.get(ReadConfig.getHomePageURL())
        time.sleep(10)
        allure.attach(driver.get_screenshot_as_png(), name="01_Homepage_Loaded", attachment_type=AttachmentType.PNG)

        # Step 2: Click sign in
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

        tt1_elem = driver.find_element(By.XPATH, xpaths["tt1"])
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tt1_elem)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["tt1"]))).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="06_Clicked_TT1", attachment_type=AttachmentType.PNG) 

        # Step 6: Click 'Choose Profile' (New Flow)
        wait.until(EC.element_to_be_clickable((By.ID, xpaths["choose_profile_btn"]))).click()
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="06_Clicked_Choose_Profile_Button", attachment_type=AttachmentType.PNG)

        # Step 7: Click 'Add Multi User'
        wait.until(EC.element_to_be_clickable((By.ID, xpaths["add_multi_user_btn"]))).click()
        time.sleep(3)
        allure.attach(driver.get_screenshot_as_png(), name="07_Clicked_Add_Multi_User", attachment_type=AttachmentType.PNG)

        # Step 8: Upload Profile Image
        img_path = "C:/vodwebsite/tmp/jithk.jpg"  # update path if needed
        driver.find_element(By.ID, xpaths["profile_img_upload"]).send_keys(img_path)
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="08_Uploaded_Profile_Image", attachment_type=AttachmentType.PNG)

        # Step 9: Enter Username
        driver.find_element(By.ID, xpaths["profile_username"]).send_keys("ruban")
        time.sleep(2)
        allure.attach(driver.get_screenshot_as_png(), name="09_Entered_Username", attachment_type=AttachmentType.PNG)

        # Step 10: Click 'Create' Button
        driver.find_element(By.ID, xpaths["profile_create_btn"]).click()
        time.sleep(5)
        allure.attach(driver.get_screenshot_as_png(), name="10_Clicked_Create_Profile", attachment_type=AttachmentType.PNG)

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="ERROR_Final_Crash", attachment_type=AttachmentType.PNG)
        print(f"❌ Exception occurred: {e}")
        raise

    @classmethod
    def teardown_class(cls):
        try:
            cls.driver.quit()
        except:
            pass
