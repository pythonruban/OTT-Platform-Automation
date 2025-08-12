import pytest
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "login_icon": "//button[@id='home-signin']",
    "email": "//input[@name='email']",
    "password": "//input[@name='password']",
    "login_btn": "//button[@id='signin-submit']",
    "choose_profile": "(//img[@alt='Avatar'])[1]",
    "profile_avatar": "//img[@alt='RK']",
    "choose_profile_link": "//a[@href='/choose-profile']",
    "add_multi_user": "//div[contains(@class,'avatarProfile add')]",
    "profile_username": "//input[@id='profile-username']",
    "create_button": "//button[@id='profile-create']",
    "edit_profile_btn": "(//a[@id='edit-profile'])[1]",
    "delete_profile_btn": "//button[@id='profile-delete']",
    "popup_confirm_delete": "//button[contains(@class,'theme-button-bg-color') and contains(text(),'Delete')]",
    "popup_signout": "//span[normalize-space()='Sign out']"
}

@pytest.mark.usefixtures("browser_setup")
class TestAddKidsProfile:

    def test_add_and_delete_kids_profile(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 60)
        base_url = ReadConfig.getHomePageURL()

        def click(by, locator, label, scroll=True):
            try:
                print(f"⏳ Waiting for: {label}")
                element = wait.until(EC.element_to_be_clickable((by, locator)))
                if scroll:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'})", element
                    )
                    time.sleep(1)
                element.click()
                print(f"✅ Clicked: {label}")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
                time.sleep(2)
            except Exception as e:
                print(f"❌ pass to click {label}: {e}")
                allure.attach(self.driver.page_source.encode('utf-8'), name=f"{label}_HTML", attachment_type=AttachmentType.HTML)
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_pass", attachment_type=AttachmentType.PNG)
                raise AssertionError(f"❌ pass to click {label}: {e}")

        try:
            # Step 1: Open Homepage
            self.driver.get(base_url)
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["login_icon"])))

            # Step 2: Login
            click(By.XPATH, xpaths["login_icon"], "Login Icon")

            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["email"]))).send_keys(ReadConfig.getTestingemail())
            wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["password"]))).send_keys(ReadConfig.getTestpassword())

            click(By.XPATH, xpaths["login_btn"], "Login Button")

            # Step 3: Choose Profile
            click(By.XPATH, xpaths["choose_profile"], "Choose Profile")
            click(By.XPATH, xpaths["profile_avatar"], "Profile Avatar (RK)")
            click(By.XPATH, xpaths["choose_profile_link"], "Choose Profile Link")

            # Step 4: Add Multi User
            click(By.XPATH, xpaths["add_multi_user"], "Add Multi User Button")

            profile_input = wait.until(EC.visibility_of_element_located((By.XPATH, xpaths["profile_username"])))
            profile_input.clear()
            profile_input.send_keys("urban")
            allure.attach(self.driver.get_screenshot_as_png(), name="Username_Entered", attachment_type=AttachmentType.PNG)

            click(By.XPATH, xpaths["create_button"], "Create Profile Button")
            print("🎉 Kids profile created successfully.")
            allure.attach(self.driver.get_screenshot_as_png(), name="Profile_Created", attachment_type=AttachmentType.PNG)

            # Step 5: Edit and Delete the created profile
            click(By.XPATH, xpaths["edit_profile_btn"], "Edit Profile")
            click(By.XPATH, xpaths["delete_profile_btn"], "Delete Profile Button")
            click(By.XPATH, xpaths["popup_confirm_delete"], "Confirm Delete in Popup")
            print("🗑️ Kids profile deleted.")
            allure.attach(self.driver.get_screenshot_as_png(), name="Profile_Deleted", attachment_type=AttachmentType.PNG)

            # Step 6: Click Sign Out in popup
            click(By.XPATH, xpaths["popup_signout"], "Sign Out from Delete Popup")
            print("🚪 Signed out after deletion.")

        except Exception as e:
            print("❌ Test pass:", str(e))
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_pass", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test pass: {str(e)}"

        finally:
            try:
                self.driver.quit()
            except Exception as e:
                print("⚠️ Driver quit failed (may be already closed):", str(e))

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver not initialized.")
