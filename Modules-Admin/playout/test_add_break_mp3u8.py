import pytest
import allure
import os
import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utilities.readProp import ReadConfig

xpaths = {
    "email_input": "(//input[@name='email'])[2]",
    "password_input": "//input[@name='password']",
    "login_button": "//span[text()='Login']",
    "dashboard_check": "//span[normalize-space()='Dashboard']",
    "tv_playout": "//span[text()='TV Playout']",
    "create_button": "//button[@id='adminButton']",
    "name_input": "//input[@id='create-name']",
    "select_type": "//select[@id='create-select-type']",
    "option_schedule_stream": "//option[@id='Schedule stream']",
    "submit_btn": "(//button[@id='adminButton'])[2]",
    "input_title": "//input[@id='playout-title']",
    "playout_mode": "//select[@id='playout_types']",
    "playout_select": "//option[@id='schedule']",
    "select_live": "//select[@id='destination_title']",
    "live_select": "//option[@id='9']",
    "substitute_video": "//select[@id='substitute_title']",
    "substitute_select": "//option[@id='52']",
    "taggle_button": "//span[@class='admin-slider position-absolute admin-round ']",
    "thumbnail_image": "//input[@id='playout-thumbnail-image']",
    "player_image": "//input[@id='playout-plyer-image']",
    "submit_button": "(//button[@id='adminButton'])[1]",

    # Remaining flows:
    "tab_home_1": "//button[@id='pills-home-tab']",
    "Break_Time" : "//td[@class='p-0']",
    "Break_url" : "//input[@id='inputField']",
    "Break_submit": "//span[@class='undefined labelLoader square   ']",
    "search_input_1": "(//input[@id='video-search-input col-3'])[1]",
    "search_result_1": "//td[@class='live-wrapper']",
    

    "tab_home_2": "//button[@id='pills-profile-tab']",
    "search_input_2": "(//input[@id='video-search-input col-3'])[2]",
    "search_result_2": "//td[@class='video-wrapper']",
    
    "Back_button": "//a[@id='backArrow']"
}


@pytest.mark.usefixtures("browser_setup")
@allure.feature("TV Playout - Create New Stream with Thumbnail Valid")
@allure.title("Create Schedule Stream and Validate Search")
class Test_createbreak_m3u8:

    def click(self, by, locator, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.element_to_be_clickable((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            time.sleep(0.5)
            try:
                elem.click()
            except Exception:
                print(f"⚠️ JS click fallback for {label}")
                self.driver.execute_script("arguments[0].click();", elem)
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def enter_text(self, by, locator, value, label):
        try:
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", elem)
            elem.clear()
            elem.send_keys(value)
            print(f"✅ Entered: {label} = {value}")
            allure.attach(self.driver.get_screenshot_as_png(), name=label, attachment_type=AttachmentType.PNG)
        except Exception as e:
            raise AssertionError(f"❌ Failed to enter text in {label}: {e}")

    def test_createbreak_m3u8(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(ReadConfig.getAdminPageURL())
        self.driver.maximize_window()

        # Login
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email_input"]))).send_keys(ReadConfig.getAdminId())
        self.driver.find_element(By.XPATH, xpaths["password_input"]).send_keys(ReadConfig.getPassword())
        self.driver.find_element(By.XPATH, xpaths["login_button"]).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["dashboard_check"])))
        allure.attach(self.driver.get_screenshot_as_png(), name="01_Login_Success", attachment_type=AttachmentType.PNG)

        # Navigate to Create Stream
        self.click(By.XPATH, xpaths["tv_playout"], "02_TV_Playout")
        self.click(By.XPATH, xpaths["create_button"], "03_Create_Button")

        # Fill initial fields
        self.enter_text(By.XPATH, xpaths["name_input"], "Test Stream", "04_Stream_Name")
        self.click(By.XPATH, xpaths["select_type"], "05_Select_Type")
        self.click(By.XPATH, xpaths["option_schedule_stream"], "06_Option_Schedule")
        self.click(By.XPATH, xpaths["submit_btn"], "07_Submit_Intermediate")

        # Fill schedule details
        wait.until(EC.presence_of_element_located((By.XPATH, xpaths["input_title"])))
        self.enter_text(By.XPATH, xpaths["input_title"], "Test Title", "08_Playout_Title")
        self.click(By.XPATH, xpaths["playout_mode"], "09_Playout_Mode")
        self.click(By.XPATH, xpaths["playout_select"], "10_Select_Schedule")
        self.click(By.XPATH, xpaths["select_live"], "11_Select_Live")
        self.click(By.XPATH, xpaths["live_select"], "12_Live_Option")
        self.click(By.XPATH, xpaths["substitute_video"], "13_Select_Substitute")
        self.click(By.XPATH, xpaths["substitute_select"], "14_Substitute_Option")

        # Toggle
        self.click(By.XPATH, xpaths["taggle_button"], "15_Toggle_1")
        time.sleep(1)
        self.click(By.XPATH, xpaths["taggle_button"], "16_Toggle_2")

        # Upload thumbnail & player image
        thumb_path = os.path.abspath(r"C:/Users/Picnexs/Desktop/website/vodwebsite/tmp/ajithk.jpg")
        player_path = os.path.abspath(r"C:/Users/Picnexs/Desktop/website/vodwebsite/tmp/1280_720 px.png")
        if not os.path.exists(thumb_path) or not os.path.exists(player_path):
            raise AssertionError(f"❌ Missing images:\n{thumb_path}\n{player_path}")
        self.driver.find_element(By.XPATH, xpaths["thumbnail_image"]).send_keys(thumb_path)
        self.driver.find_element(By.XPATH, xpaths["player_image"]).send_keys(player_path)
        print("✅ Uploaded both images")
        allure.attach(self.driver.get_screenshot_as_png(), name="17_Images_Uploaded", attachment_type=AttachmentType.PNG)
        time.sleep(2)

        # Final Submit
        try:
            self.click(By.XPATH, xpaths["submit_button"], "18_Final_Submit")
            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="19_Submit_Success", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="19_Submit_Click_Failed", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Final Submit Failed: {e}")
        
        self.click(By.XPATH, xpaths["tab_home_1"], "20_Home_Tab")
        self.click(By.XPATH, xpaths["Break_Time"], "Break_time_click")
        self.enter_text(By.XPATH, xpaths["Break_url"], "http://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8", "Url_add_break")
        self.click(By.XPATH, xpaths["Break_submit"], "Break_submit")
        self.enter_text(By.XPATH, xpaths["search_input_1"], "Live Test Video", "21_Search_Term")
        time.sleep(2)
        self.click(By.XPATH, xpaths["search_result_1"], "22_Search_Result_Click")
        allure.attach(self.driver.get_screenshot_as_png(), name="23_Search_Result_Page", attachment_type=AttachmentType.PNG)
        

        # 🔁 NEW FLOW: Click home tab → search → click result
        self.click(By.XPATH, xpaths["tab_home_2"], "20_Home_Tab")
        self.click(By.XPATH, "//input[@id='Schedule-date']", "21_Duration_Entry")
        self.enter_text(By.XPATH, xpaths["search_input_2"], "Nagada Sang Dho", "21_Search_Term")
        time.sleep(2)  # Let search result load
        self.click(By.XPATH, xpaths["search_result_2"], "22_Search_Result_Click")
        allure.attach(self.driver.get_screenshot_as_png(), name="23_Search_Result_Page", attachment_type=AttachmentType.PNG)
   
        self.click(By.XPATH, "//input[@name='scheduleDuration-0']", "28_Duration_Entry")
        self.click(By.XPATH, "//select[@style='padding: 5px; margin-right: 5px;']", "29_Fallback_Dropdown")
        self.click(By.XPATH, "//option[@value='05']", "30_Select_Fallback_Option")

        self.click(By.XPATH, "(//button[contains(@style, 'background: rgb(0, 123, 255)')])[1]", "31_Submit_Video")
        allure.attach(self.driver.get_screenshot_as_png(), name="32_Video_Submitted", attachment_type=AttachmentType.PNG)

        self.click(By.XPATH, xpaths["Back_button"], "33_back_button")
        time.sleep(5)
        allure.attach(self.driver.get_screenshot_as_png(), name="33_back_button", attachment_type=AttachmentType.PNG)
