import asyncio
from playwright.async_api import async_playwright

SESSION_ID = "PASTE_YOUR_SESSIONID_HERE"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Inject Instagram session cookie
        await context.add_cookies([
            {
                "name": "sessionid",
                "value": SESSION_ID,
                "domain": ".instagram.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }
        ])

        page = await context.new_page()
        await page.goto("https://www.instagram.com/", timeout=60000)
        await page.wait_for_load_state("networkidle")

        # Save FULL Playwright session
        await context.storage_state(path="ig_session.json")

        print("✅ ig_session.json created successfully")

        await browser.close()

asyncio.run(main())
