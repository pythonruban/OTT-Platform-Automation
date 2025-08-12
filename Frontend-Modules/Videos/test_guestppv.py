import pytest
import allure
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

xpaths = {
    "Categories_tab": "//li[@id='header-Categories']",
    "categories": "//div[@class='card-image-container']",
    "videos": "//div[@class='homeListImage active']",
    "ppv_button": "//button[contains(@id,'rent-now-role')]",
    "signup_button": "//button[@id='no-account-signup']",
    "first_name": "//input[@id='signup-username']",
    "last_name": "//input[@id='signup-lastname']",
    "email": "//input[@id='signup-email']",
    "country_dropdown": "//div[@role='button']",
    "india_option": "//li[@data-country-code='in']",
    "mobile": "//input[@type='tel']",
    "dob": "//input[@id='signup-dob']",
    "gender": "//select[@id='signup-gender']",
    "country": "//input[@id='signup-country']",
    "state": "//input[@id='signup-state']",
    "city": "//input[@id='signup-city']",
    "password": "//input[@id='signup-password']",
    "confirm_password": "//input[@id='confirmPassword']",
    "accept_terms": "//input[@id='signup-accept']",
    "submit_signup": "//button[@id='signup-submit']",
}

@pytest.mark.usefixtures("browser_setup")
@allure.feature("Guest PPV with Signup on Redirect")
class TestGuestPPVSignupFlow:

    def test_guest_ppv_signup_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, path, label):
            try:
                element = wait.until(EC.element_to_be_clickable((by, path)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                element.click()
                allure.attach(self.driver.get_screenshot_as_png(), name=f"Click_{label}", attachment_type=AttachmentType.PNG)
            except Exception as e:
                raise AssertionError(f"Failed to click {label}: {e}")

        self.driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        click(By.XPATH, xpaths["Categories_tab"], "Categories_Tab")
        view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
        wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

        categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
        for cat_index, category in enumerate(categories):
            categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
            categories[cat_index].click()
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Category_{cat_index+1}_Opened", attachment_type=AttachmentType.PNG)

            videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
            for vid_index, video in enumerate(videos):
                videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", videos[vid_index])
                videos[vid_index].click()
                allure.attach(self.driver.get_screenshot_as_png(), name=f"Video_{vid_index+1}_Clicked", attachment_type=AttachmentType.PNG)

                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["ppv_button"])))
                    click(By.XPATH, xpaths["ppv_button"], "PPV_Button")

                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["signup_button"])))
                    click(By.XPATH, xpaths["signup_button"], "Signup_Button")

                    rand_email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                    self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                    self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Kumar")
                    self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(rand_email)
                    click(By.XPATH, xpaths["country_dropdown"], "Country_Dropdown")
                    click(By.XPATH, xpaths["india_option"], "India_Option")
                    self.driver.find_element(By.XPATH, xpaths["mobile"]).send_keys("9876543210")
                    self.driver.find_element(By.XPATH, xpaths["dob"]).send_keys("2000-01-01")
                    self.driver.find_element(By.XPATH, xpaths["gender"]).send_keys("Male")
                    self.driver.find_element(By.XPATH, xpaths["country"]).send_keys("India")
                    self.driver.find_element(By.XPATH, xpaths["state"]).send_keys("TN")
                    self.driver.find_element(By.XPATH, xpaths["city"]).send_keys("Chennai")
                    self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                    self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("program12@12A")
                    self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()
                    click(By.XPATH, xpaths["submit_signup"], "Submit_Signup")

                    # After signup, go back and retry PPV
                    self.driver.get(base_url)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    click(By.XPATH, xpaths["Categories_tab"], "Categories_Tab_After_Signup")
                    categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                    categories[cat_index].click()
                    videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                    videos[vid_index].click()
                    click(By.XPATH, xpaths["ppv_button"], "PPV_After_Signup")

                    allure.attach(self.driver.get_screenshot_as_png(), name="PPV_Confirmed_After_Signup", attachment_type=AttachmentType.PNG)
                    return  # Test success

                except Exception:
                    self.driver.back()

            self.driver.get(base_url)
            click(By.XPATH, xpaths["Categories_tab"], "Categories_Tab_Next_Category")

        raise AssertionError("No PPV video found or signup flow failed")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
