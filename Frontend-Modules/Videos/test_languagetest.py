import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.readProp import ReadConfig

@allure.feature("Guest - Artist Auto Redirection")
@allure.title("Redirect to James Cameron Artist Page from Video Category")
@pytest.mark.usefixtures("browser_setup")
class TestGuestVideoAutoRedirectToArtist:

    def test_video_category_redirect_to_artist(self, browser_setup):
        self.driver = browser_setup
        wait = WebDriverWait(self.driver, 25)
        base_url = ReadConfig.getHomePageURL()
        expected_url = f"{base_url}artist/james-cameron/videos"  # ✅ Handles dynamic base URL

        try:
            with allure.step("Step 1: Open Home Page"):
                self.driver.get(base_url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                allure.attach(self.driver.get_screenshot_as_png(), name="Homepage_Loaded", attachment_type=AttachmentType.PNG)

            with allure.step("Step 2: Click VIDEO header"):
                video_header = wait.until(EC.element_to_be_clickable((By.ID, "header-Videos")))
                video_header.click()
                allure.attach(self.driver.get_screenshot_as_png(), name="Clicked_Video_Header", attachment_type=AttachmentType.PNG)

            with allure.step("Step 3: Find James Cameron Card and Click"):
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-image-container")))
                cards = self.driver.find_elements(By.CLASS_NAME, "card-image-container")

                print(f"🔍 Found {len(cards)} cards")
                clicked = False

                for i, card in enumerate(cards):
                    try:
                        link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                        print(f"🔗 Card {i} link: {link}")

                        if "/artist/james-cameron/videos" in link:
                            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", card)
                            wait.until(EC.element_to_be_clickable(card)).click()
                            clicked = True
                            allure.attach(self.driver.get_screenshot_as_png(), name=f"Card_{i}_Clicked", attachment_type=AttachmentType.PNG)
                            print("✅ Clicked James Cameron card")
                            break
                    except Exception as e:
                        print(f"⚠️ Skipped card {i} due to: {str(e)}")

                if not clicked:
                    allure.attach(self.driver.get_screenshot_as_png(), name="No_James_Cameron_Card", attachment_type=AttachmentType.PNG)
                    raise AssertionError("❌ Test Failed: James Cameron artist card not found.")

            with allure.step("Step 4: Verify Redirection"):
                wait.until(EC.url_contains("/artist/james-cameron/videos"))
                actual_url = self.driver.current_url
                print(f"🌐 Current URL: {actual_url}")
                assert actual_url == expected_url, f"❌ URL mismatch. Expected: {expected_url}, Got: {actual_url}"
                allure.attach(self.driver.get_screenshot_as_png(), name="Redirect_Success", attachment_type=AttachmentType.PNG)

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Test_Failed", attachment_type=AttachmentType.PNG)
            assert False, f"❌ Test Failed: {str(e)}"
