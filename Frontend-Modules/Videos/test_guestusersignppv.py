import pytest
import allure
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig


xpaths = {
    "Categories_tab": "//li[@id='header-Categories']",
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
class TestGuestPPVSignupFlow:

    def test_guest_ppv_signup_flow(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 30)
        base_url = ReadConfig.getHomePageURL()

        def click(by, path, label):
            try:
                element = wait.until(EC.element_to_be_clickable((by, path)))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
                time.sleep(1)
                element.click()
                print(f"✅ Clicked: {label}")
                time.sleep(2)
            except Exception as e:
                raise AssertionError(f"❌ Failed to click {label}: {e}")

        self.driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        click(By.XPATH, xpaths["Categories_tab"], "Categories Tab")
        view_all_xpath = "(//a[contains(text(), 'View All')])[1]"
        wait.until(EC.element_to_be_clickable((By.XPATH, view_all_xpath))).click()

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
                    click(By.XPATH, xpaths["ppv_button"], "PPV Button")

                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["signup_button"])))
                    click(By.XPATH, xpaths["signup_button"], "Signup Link")

                    # 🔒 Fill Signup Form
                    rand_email = f"ruban{random.randint(1000,9999)}@webnexs.in"
                    self.driver.find_element(By.XPATH, xpaths["first_name"]).send_keys("Ruban")
                    self.driver.find_element(By.XPATH, xpaths["last_name"]).send_keys("Kumar")
                    self.driver.find_element(By.XPATH, xpaths["email"]).send_keys(rand_email)

                    # 🌍 Country Dropdown
                    click(By.XPATH, xpaths["country_dropdown"], "Country Dropdown")
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["search_box"])))
                    self.driver.find_element(By.XPATH, xpaths["search_box"]).send_keys("India")
                    wait.until(EC.presence_of_element_located((By.XPATH, xpaths["country_result"])))
                    click(By.XPATH, xpaths["country_result"], "India Country Option")

                    # 📱 Mobile (slowly enter digits)
                    mobile_input = self.driver.find_element(By.XPATH, xpaths["mobile"])
                    for digit in "9876543210":
                        mobile_input.send_keys(digit)
                        time.sleep(0.1)
                    time.sleep(1)

                    # 🔐 Scroll to Password Field
                    password_input = wait.until(EC.presence_of_element_located((By.XPATH, xpaths["password"])))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", password_input)
                    time.sleep(1)

                   
                    # 🔑 Password
                    self.driver.find_element(By.XPATH, xpaths["password"]).send_keys("program12@12A")
                    self.driver.find_element(By.XPATH, xpaths["confirm_password"]).send_keys("program12@12A")
                    self.driver.find_element(By.XPATH, xpaths["accept_terms"]).click()

                    # 🧾 Submit
                    click(By.XPATH, xpaths["submit_signup"], "Submit Signup")

                    # ✅ Go back and retry PPV
                    self.driver.get(base_url)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    click(By.XPATH, xpaths["Categories_tab"], "Categories Tab Again")
                    categories = self.driver.find_elements(By.XPATH, xpaths["categories"])
                    categories[cat_index].click()
                    time.sleep(3)
                    videos = self.driver.find_elements(By.XPATH, xpaths["videos"])
                    videos[vid_index].click()
                    time.sleep(3)
                    click(By.XPATH, xpaths["ppv_button"], "PPV Button After Signup")

                    print("✅ Guest user signed up and clicked PPV after login")
                    return

                except Exception as e:
                    print(f"❌ PPV failed at video {vid_index+1} → {str(e)}")
                    self.driver.back()
                    time.sleep(2)

            self.driver.get(base_url)
            click(By.XPATH, xpaths["Categories_tab"], "Categories Tab for next Category")

        raise AssertionError("❌ No PPV video found or signup failed in all categories")

    def teardown_class(self):
        try:
            self.driver.quit()
        except:
            pass
