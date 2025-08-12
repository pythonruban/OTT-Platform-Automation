import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "live_tab": "//li[@id='header-Live']",
    "categories": "//div[@class='card-image-container']",
    "videos": "//div[@class='homeListImage active']",
    "ppv_button": "//button[contains(@id,'rent-now-role')]",
    "signup_button": "//a[@class='border-0 bg-transparent theme-button-tab-color']",

    # Signup form
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "search_box": "//input[@class='search-box']",
    "country_result": "//span[@class='country-name' and text()='India']",
    "mobile": "//input[@type='tel']",
    "password": "//input[@id='signup-password']",
    "confirm_password": "//input[@id='confirmPassword']",
    "accept_terms": "//input[@id='signup-accept']",
    "submit_signup": "//button[@id='signup-submit']",
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest PPV with Signup on Redirect")
@allure.title("Verify Guest User is Prompted for Signup on PPV and Flow Completes")
class TestGuestPPVSignupFlow:

    def click_element(self, by, path, label, wait_time=30):
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.element_to_be_clickable((by, path)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            element.click()
            print(f"✅ Clicked: {label}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Clicked", attachment_type=AttachmentType.PNG)
            time.sleep(2)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{label}_Error", attachment_type=AttachmentType.PNG)
            raise AssertionError(f"❌ Failed to click {label}: {e}")

    def test_guest_ppv_signup_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        self.driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.click_element(By.XPATH, xpaths["live_tab"], "Live Tab")

        categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
        for cat_index in range(len(categories)):
            categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
            categories[cat_index].click()
            print(f"➡️ Category {cat_index+1} opened")
            time.sleep(3)

            videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
            for vid_index in range(len(videos)):
                videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[vid_index])
                videos[vid_index].click()
                print(f"🎥 Video {vid_index+1} clicked")
                time.sleep(3)

                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                    self.click_element(By.XPATH, xpaths["ppv_button"], "PPV Button")

                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["signup_button"])))
                    self.click_element(By.XPATH, xpaths["signup_button"], "Signup Button")

                    # Fill Signup Form
                    rand_email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                    self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                    self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Kumar")
                    self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(rand_email)

                    # Country selection
                    self.click_element(By.XPATH, xpaths["country_dropdown"], "Country Dropdown")
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["search_box"])))
                    self.driver.find_element(By.XPATH, xpaths["search_box"]).send_keys("India")
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["country_result"])))
                    self.click_element(By.XPATH, xpaths["country_result"], "India Option")

                    # Mobile number typing
                    mobile_field = self.driver.find_element(By.XPATH, xpaths["mobile"])
                    for digit in "9876543210":
                        mobile_field.send_keys(digit)
                        time.sleep(0.1)

                    # Password
                    self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                    self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("program12@12A")

                    # Accept terms and submit
                    self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()
                    self.click_element(By.XPATH, xpaths["submit_signup"], "Submit Signup")

                    # After signup, retry the same flow
                    self.driver.get(base_url)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    self.click_element(By.XPATH, xpaths["live_tab"], "Live Tab Retry")

                    categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                    categories[cat_index].click()
                    time.sleep(2)
                    videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                    videos[vid_index].click()
                    time.sleep(2)
                    self.click_element(By.XPATH, xpaths["ppv_button"], "PPV Button After Signup")

                    print("✅ PPV video clicked after signup, test passed.")
                    allure.attach(self.driver.get_screenshot_as_png(), name="PPV_After_Signup", attachment_type=AttachmentType.PNG)
                    return  # End test here

                except Exception as e:
                    print(f"⚠️ Skipping Video {vid_index+1} due to error: {e}")
                    self.driver.back()
                    time.sleep(2)

            # Go back to home to try next category
            self.driver.get(base_url)
            self.click_element(By.XPATH, xpaths["live_tab"], "Live Tab for Next Category")

        raise AssertionError("❌ No PPV video found or signup failed in all categories")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            print("⚠️ Driver already closed")
