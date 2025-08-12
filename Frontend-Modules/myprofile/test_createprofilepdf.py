import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig  # ✅ Use config reader

# ✅ Local profile image path
PROFILE_IMAGE_PATH = r"C:\workspace\vodwebsites\tmp\vulnerability_logs.pdf"

xpaths = {
    "login_icon": "//button[@id='home-signin']",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "profile_avatar": "//img[@alt='RK']",
    "my_profile_link": "//a[@id='my-profile']",
    "manage_profiles_link": "(//a[@href='/myprofile/profiles'])[2]",
    "create_profile_btn": "//a[@href='/multi-profile/create']",
    "profile_name_input": "//input[@id='profile-username']",
    "profile_image_upload": "//input[@type='file']",
    "create_button": "//button[@id='profile-create']",
    "new_profile_avatar": "//span[text()='ruban']",
    "toast": "//div[contains(@class,'Toastify__toast-body')]"
}

@pytest.mark.usefixtures("browser_setup")
class TestCreateMultiProfile:

    def test_create_profile(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, locator, label, scroll=True):
            try:
                elem = wait.until(EC.element_to_be_clickable((by, locator)))
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", elem)
                    time.sleep(1)
                elem.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_FAILED", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to click {label} — {str(e)}")

        try:
            # Step 1: Open Homepage
            self.driver.get(base_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            # Step 2: Login
            wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["login_icon"]))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            self.driver.find_element(By.XPATH, xpaths["password"]).send_keys(ReadConfig.getTestpassword())
            self.driver.find_element(By.XPATH, xpaths["login_btn"]).click()
            print("✅ Logged in successfully")
            allure.attach(self.driver.get_screenshot_as_png(), name="01_LoggedIn", attachment_type=AttachmentType.PNG)

            # Step 3: Choose Current Profile
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")

            # Step 4: Navigate to Profile Settings
            click(By.XPATH, xpaths["profile_avatar"], "Profile Avatar RK")
            click(By.XPATH, xpaths["my_profile_link"], "My Profile Link")
            click(By.XPATH, xpaths["manage_profiles_link"], "Manage Profiles")
            click(By.XPATH, xpaths["create_profile_btn"], "Create New Profile")

            # Step 5: Fill Profile Name
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["profile_name_input"]))).send_keys("ruban")
            allure.attach(self.driver.get_screenshot_as_png(), name="ProfileName_Entered", attachment_type=AttachmentType.PNG)

            # Step 6: Upload Profile Image
            try:
                image_elem = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["profile_image_upload"])))
                self.driver.execute_script("arguments[0].style.display = 'block';", image_elem)
                image_elem.send_keys(PROFILE_IMAGE_PATH)
                allure.attach(self.driver.get_screenshot_as_png(), name="Image_Uploaded", attachment_type=AttachmentType.PNG)
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Upload_Failed", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ Failed to upload image — {str(e)}")

            # Step 7: Click Create Profile
            click(By.XPATH, xpaths["create_button"], "Create Profile Button")

            # Step 8: Select New Profile
            click(By.XPATH, xpaths["new_profile_avatar"], "New Profile 'ruban'")

            # Step 9: Toast Confirmation
            wait.until(EC.presence_of_element_located((By.XPATH, xpaths["toast"])))
            print("✅ Profile creation toast appeared.")
            allure.attach(self.driver.get_screenshot_as_png(), name="Profile_Creation_Confirmed", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test failed: {str(e)}"

    def teardown_class(self):
        try:
            self.driver.quit()
        except AttributeError:
            print("⚠️ Driver not initialized.")
