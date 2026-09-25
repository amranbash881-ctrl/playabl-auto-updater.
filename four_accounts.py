import os
import asyncio
from playwright.async_api import async_playwright

# قراءة الحسابات بشكل آمن تماماً من متغيرات البيئة (GitHub Secrets)
ACCOUNTS_DATA = [
    {
        "email": os.environ.get("PLAYABL_EMAIL_1", "").strip(),
        "password": os.environ.get("PLAYABL_PASSWORD_1", "").strip(),
        "games": [
            "https://playabl.ai/en/projects/6aa468aa67f18075706fab9d",
            "https://playabl.ai/en/projects/6aa59f5a610218ef35db0c35",
            "https://playabl.ai/en/projects/6aa5a146c25f11aece345dde",
            "https://playabl.ai/en/projects/6aa30351eb9d46ddbc3e3c99",
            "https://playabl.ai/en/projects/6aaae93feb9d46ddbc6ef13c"
        ]
    },
    {
        "email": os.environ.get("PLAYABL_EMAIL_2", "").strip(),
        "password": os.environ.get("PLAYABL_PASSWORD_2", "").strip(),
        "games": [
            "https://playabl.ai/en/projects/6aa6ef09eb9d46ddbc5a573d",
            "https://playabl.ai/en/projects/6aa5aeaa9ee607ae96a378e2",
            "https://playabl.ai/en/projects/6aa5abec67f1807570797038",
            "https://playabl.ai/en/projects/6aa9a7b167f180757090bedc",
            "https://playabl.ai/en/projects/6aa468e467f18075706faea0",
            "https://playabl.ai/en/projects/6aab007ed8979ed5cd11f906",
            "https://playabl.ai/en/projects/6aab0039eb9d46ddbc6f63a0"
        ]
    },
    {
        "email": os.environ.get("PLAYABL_EMAIL_3", "").strip(),
        "password": os.environ.get("PLAYABL_PASSWORD_3", "").strip(),
        "games": [
            "https://playabl.ai/en/projects/6ab18d5c1d148414505dbc6a",
            "https://playabl.ai/en/projects/6ab17f4beda3e2b3c167ab46",
            "https://playabl.ai/en/projects/6a39079ffaacd369736694af",
            "https://playabl.ai/en/projects/6a2edb4c269429b15569ebeb",
            "https://playabl.ai/en/projects/6a2b11236ccc1bedcbe67a8d",
            "https://playabl.ai/en/projects/6a2b0e816ccc1bedcbe64696"
        ]
    },
    {
        "email": os.environ.get("PLAYABL_EMAIL_4", "").strip(),
        "password": os.environ.get("PLAYABL_PASSWORD_4", "").strip(),
        "games": [
            "https://playabl.ai/en/projects/6aa6f09bbddf69057fb6069c",
            "https://playabl.ai/en/projects/6aa6eecbc25f11aece3d4232",
            "https://playabl.ai/en/projects/6aa46921eb9d46ddbc482493",
            "https://playabl.ai/en/projects/6aa5afe567f180757079af5e",
            "https://playabl.ai/en/projects/6aab07a8eda3e2b3c15323ca",
            "https://playabl.ai/en/projects/6aab07002135567cdcb774cb"
        ]
    },
    {
        "email": os.environ.get("PLAYABL_EMAIL_5", "").strip(),
        "password": os.environ.get("PLAYABL_PASSWORD_5", "").strip(),
        "games": [
            "https://playabl.ai/en/projects/6aa5b21beda3e2b3c1353688",
            "https://playabl.ai/en/projects/6aa46993eda3e2b3c12b1a85",
            "https://playabl.ai/en/projects/6aa6f0819ee607ae96aba68c",
            "https://playabl.ai/en/projects/6aa6f37ceb9d46ddbc5a8793",
            "https://playabl.ai/en/projects/6aab0ada4c0ea21ea6447132",
            "https://playabl.ai/en/projects/6aab0a4667f18075709749c5"
        ]
    }
]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )

        for index, acc in enumerate(ACCOUNTS_DATA, start=1):
            email = acc["email"]
            password = acc["password"]
            
            if not email or not password:
                print(f"[!] Warning: Skipping Account {index} because credentials are missing from environment variables.")
                continue

            print(f"\n==========================================")
            print(f"[+] Processing Account {index}: {email}")
            print(f"==========================================")

            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1366, "height": 768}
            )
            page = await context.new_page()

            try:
                games = acc["games"]
                if not games:
                    continue
                    
                first_game_url = games[0]
                await page.goto(first_game_url, wait_until="domcontentloaded", timeout=35000)
                await page.wait_for_timeout(2000)

                if await page.locator('input[type="email"], input[name="email"]').count() > 0:
                    print("  [+] Logging in with account credentials...")
                    email_input = page.locator('input[type="email"], input[name="email"]').first
                    await email_input.wait_for(state="visible", timeout=10000)
                    await email_input.fill(email)

                    password_input = page.locator('input[type="password"], input[name="password"]').first
                    await password_input.fill(password)

                    submit_btn = page.locator('button[type="submit"]').first
                    if await submit_btn.is_visible():
                        await submit_btn.click()
                    else:
                        await password_input.press("Enter")

                    await page.wait_for_timeout(6000)

                for g_index, url in enumerate(games, start=1):
                    print(f"  [{g_index}/{len(games)}] Updating game: {url}")
                    await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                    
                    try:
                        update_btn = page.locator('button:has-text("Update"), [role="button"]:has-text("Update")').first
                        await update_btn.wait_for(state="visible", timeout=8000)
                        await update_btn.click()
                        
                        await page.wait_for_timeout(500)

                        popup_btn = page.locator('button:has-text("Update"), [role="button"]:has-text("Update")').last
                        await popup_btn.click()
                        
                        await page.wait_for_timeout(2500)
                        print("    [✓] Updated successfully.")
                    except Exception as sub_e:
                        print(f"    [!] Skip or direct update note: {sub_e}")

            except Exception as e:
                print(f"  [X] Failed for account {email}: {str(e)}")
            
            finally:
                await context.close()

        await browser.close()
        print("\n[+] All accounts processed completely with isolated sessions!")

if __name__ == "__main__":
    asyncio.run(run())
