import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto("https://node-admin.webnexs.org/", timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"Error loading page: {e}")
            await browser.close()
            return
        # Wait for any visible email input field
        try:
            await page.wait_for_selector('input[type="email"]:visible', timeout=20000)
        except Exception as e:
            print(f"Email input not found: {e}")
            await browser.close()
            return
        # Fill the first visible email and password fields
        try:
            await page.fill('input[type="email"]:visible', "admin@admin.com")
            await page.fill('input[type="password"]:visible', "Webnexs123!@#")
        except Exception as e:
            print(f"Could not fill login fields: {e}")
            await browser.close()
            return
        # Try to find and click the first visible submit button
        try:
            await page.click('button[type="submit"]:visible, input[type="submit"]:visible')
        except Exception as e:
            print(f"Login button not found or not clickable: {e}")
        await asyncio.sleep(5)
        # Take screenshot after login and save to Reports
        screenshot_path = "Reports/login_screenshot.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
