import time, random, string, pytest, allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from utilities.readProp import ReadConfig


@pytest.mark.usefixtures("browser_setup")
class TestAdvertiser:

    # ───────────── Locators ─────────────
    email_element          = "(//input[@type='email'])[2]"
    password_element       = "(//input[@name='password'])[1]"
    login_element          = "(//button[@type='submit'])[2]"

    Advertiser_category_element = "//span[text()='Ads Categories']"
    add_category_btn       = "//button[@data-bs-target='#AdsCategories' and @data-bs-toggle='modal']"

    name_input_modal       = "//input[@name='AdsCategories_name']"
    slug_element = "//input[@name='AdsCategories_slug']"
    status_slider_modal    = "//span[contains(@class,'admin-slider') and contains(@class,'admin-round')]"
    submit_modal_btn       = "//button[@type='submit' and contains(normalize-space(),'Add Category')]"

    # ───────────── Test ─────────────
    def test_add_category_and_enable_slider(self, browser_setup):
        self.driver = browser_setup
        wait        = WebDriverWait(self.driver, 30)
        actions     = ActionChains(self.driver)

        # 1️⃣ Login
        try:
            self.driver.get(ReadConfig.getAdminPageURL())
            self.driver.maximize_window()
            wait.until(EC.presence_of_element_located((By.XPATH, self.email_element))) \
                .send_keys(ReadConfig.getAdminId())
            wait.until(EC.presence_of_element_located((By.XPATH, self.password_element))) \
                .send_keys(ReadConfig.getPassword())
            wait.until(EC.element_to_be_clickable((By.XPATH, self.login_element))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="login_success", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="login_error", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Login failed: {e}")

        # 2️ Open “Ads Categories”
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            Advertiser = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.Advertiser_category_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Advertiser)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", Advertiser)
            time.sleep(2)

            
            add_Advertiser = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, self.add_category_btn))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_Advertiser)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", add_Advertiser)
            time.sleep(2)

            print("Navigated to 'ADD Advertiser'")
        except Exception as e:
            print(f"[ERROR] Clicking 'Advertiser' failed: {e}")
        # 3️⃣ Fill modal & submit
        try:
            # Generate random name
            auto_name = ''.join(random.choices(string.ascii_uppercase,
                                               k=random.randint(5, 7)))
            allure.attach(auto_name, "Generated Name", AttachmentType.TEXT)

            name_field = wait.until(EC.element_to_be_clickable((By.XPATH, self.name_input_modal)))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_field)
            name_field.clear()
            name_field.send_keys(auto_name)


            print(f"Using XPath for slug input: {self.slug_element}")
            slug = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, self.slug_element))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slug)
            time.sleep(2)
            slug.clear()
            time.sleep(2)
            slug.send_keys(auto_name)
            time.sleep(2)
            print(" Auto slug entered using the name.")

        

            # Make sure slider is ON
            slider = wait.until(EC.element_to_be_clickable((By.XPATH, self.status_slider_modal)))
            if "active" not in slider.get_attribute("class").lower():
                slider.click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, self.submit_modal_btn))).click()
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="modal_submitted", attachment_type=AttachmentType.PNG)
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="modal_submit_error", attachment_type=AttachmentType.PNG)

        # #  Toggle slider in the new table row
        # try:
        #     row_xpath      = f"//tr[td/span[normalize-space(text())='{auto_name}']]"
        #     row_slider     = wait.until(EC.element_to_be_clickable(
        #         (By.XPATH, row_xpath + "//span[contains(@class,'admin-slider')]")
        #     ))
        #     self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row_slider)
        #     time.sleep(2)
        #     row_slider.click()
        #     time.sleep(2)

        #     # Verify ON text
        #     status_text = self.driver.find_element(
        #         By.XPATH, row_xpath + "//p[contains(@class, 'indicator-on-off') and contains(@class, 'on') ]"
        #     ).text.strip().upper()
        #     assert status_text == "ON", f"Slider text is '{status_text}', expected 'ON'"
        #     time.sleep(5)
        #     allure.attach(self.driver.get_full_page_screenshot_as_png(),
        #                   name="row_slider_enabled", attachment_type=AttachmentType.PNG)
           
        except Exception as e:
            allure.attach(self.driver.get_full_page_screenshot_as_png(),
                          name="row_slider_error", attachment_type=AttachmentType.PNG)
            pytest.fail(f"Failed to enable row slider: {e}")
