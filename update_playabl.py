import os
import asyncio
from playwright.async_api import async_playwright

PROJECT_IDS = [
    "6a1fba5b90c2439ef7636d92", "6a2e4c1e6da504efb412a02d", "6a39a5f4d7d4691c2a55d189",
    "6a2fb1d1bb026a03dd9f67bc", "6a9bbfafdc40d3538384fd54", "6a9bf36af4132c4da4e29e76",
    "6a25c76bf1e23d9eb0ff08f6", "6a9a62fc45815cbad5c27377", "6a359f55e12f6315158ac255",
    "6a2bb9177af4f50dd438d406", "6a30f0582ed63812faad0459", "6a1fc64cd805ddc3cc0de771",
    "6a31b06360150c324337a0e3", "6a28fad69dad6b6633e5d244", "6a47565b0f9279f40744dc23",
    "6a23cf9bf2e543e870a4da38", "6a2cf81488b43be183780fc4", "6a27b43c40fec7972ff037c3",
    "6a53fa6a32c007d476d81ace", "6a3e6053baee73b0788b08dd", "6a330c0dea0658012837bbcb",
    "6a384b17792fbe1ac5d03e2a", "6a42275b0f100de767869d49", "6a4ff6b6172a11262ac53edf",
    "6a3ecd75dce3a247f159bc22", "6a2a86d54c9e431f1f217cd8", "6a9947cd9c0fa418e6ec6b46",
    "6a22669f72906c5041bc994a", "6a9fd89ea8c120772377bab5", "6a9ff6b653f9b65c6e30fd1e",
    "6a9fd82778d7d92569075b39", "6a9fd8ef53f9b65c6e3080ab", "6a44cb6d19f28ce904b644c6",
    "6aa262339643b52cb20d90d7", "6aa26244573a756607b35103", "6aa3ac1aeb9d46ddbc41a1d4",
    "6aa4e406eda3e2b3c12ec238", "6aa64f04bddf69057fb22186", "6aa643b7eda3e2b3c1397625",
    "6aa7d848fa4e605768f8891f", "6aa7d86dd1587f9d3b359466", "6aa7cf61bddf69057fbb7d0a",
    "6aa7ce9a9ee607ae96b0e595", "6aa7cfb067f1807570879120", "6aa7c7be91601f95d2662b04",
    "6aa7c387bddf69057fbb45fa", "6aa7c33791601f95d2660ee9", "6aa6925beda3e2b3c13ab508",
    "6aaa7295594931f3ee832aab", "6aaa4550610218ef35f60a72", "6aaa3bb9bddf69057fc7ca22",
    "6aaa3af4eb9d46ddbc6be0a6", "6aa93524eb9d46ddbc662711", "6aab10fd1d148414504a9a41"
]

EMAIL = os.environ.get("PLAYABL_EMAIL", "").strip()
PASSWORD = os.environ.get("PLAYABL_PASSWORD", "").strip()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        page = await context.new_page()

        print("[+] Navigating to login page...")
        try:
            first_project_url = f"https://playabl.ai/en/projects/{PROJECT_IDS[0]}"
            await page.goto(first_project_url, wait_until="domcontentloaded", timeout=35000)
            await page.wait_for_timeout(2000)

            email_input = page.locator('input[type="email"], input[name="email"]').first
            await email_input.wait_for(state="visible", timeout=15000)
            await email_input.fill(EMAIL)

            password_input = page.locator('input[type="password"], input[name="password"]').first
            await password_input.fill(PASSWORD)

            submit_btn = page.locator('button[type="submit"]').first
            if await submit_btn.is_visible():
                await submit_btn.click()
            else:
                await password_input.press("Enter")

            await page.wait_for_timeout(7000)

            if "login" in page.url:
                print("[X] Login Failed. Extracting visible text on page to inspect error:")
                body_text = await page.inner_text("body")
                print("--- PAGE TEXT START ---")
                print(body_text[:800].replace('\n', ' '))
                print("--- PAGE TEXT END ---")
                await browser.close()
                return

            print(f"[+] Login successful! Reached: {page.url}")

        except Exception as e:
            print(f"[X] Exception during login: {e}")
            await browser.close()
            return

        for index, project_id in enumerate(PROJECT_IDS, start=1):
            url = f"https://playabl.ai/en/projects/{project_id}"
            print(f"[{index}/{len(PROJECT_IDS)}] Processing project: {project_id}")

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                
                update_btn = page.locator('button:has-text("Update"), [role="button"]:has-text("Update")').first
                await update_btn.wait_for(state="visible", timeout=10000)
                await update_btn.click()
                
                await page.wait_for_timeout(500)

                popup_btn = page.locator('button:has-text("Update"), [role="button"]:has-text("Update")').last
                await popup_btn.click()
                
                await page.wait_for_timeout(3000)
                print("   [✓] Updated successfully.")

            except Exception as e:
                print(f"   [X] Failed: {str(e)}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())    
