import aiofiles, pathlib
import asyncio
from playwright.async_api import async_playwright

chat_name = "All in One"


async def wait_for_image(img_loc, timeout=15_000):
    """Wait until <img> is visible AND its bitmap loaded."""
    await img_loc.wait_for(state='visible', timeout=timeout)
    await img_loc.wait_for_function(
        "el => el.complete && el.naturalWidth > 0",
        timeout=timeout
    )

async def main():
    async with async_playwright() as p:

        user_data_dir = "./playwright_profile"
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--start-maximized"]  # optional: start browser maximized
        )

        page = await context.new_page()
        page.set_default_timeout(60000)
        await page.goto("https://web.whatsapp.com/" , wait_until="networkidle" , timeout=10000000)
        print("Loaded WhatsApp…")

        await page.wait_for_selector('div[aria-label="Search input textbox"]')
        await page.wait_for_timeout(200)

        search_box = page.locator('div[aria-label="Search input textbox"]')
        await search_box.click()
        print("clicked search box")

        await page.keyboard.type(chat_name)
        await asyncio.sleep(1.2)

        chat_locator = page.locator('span[title="All in one"]')
        await chat_locator.click()
        print(f"opned \"{chat_name}\" chat")
        await asyncio.sleep(1.2)

        profile_locator = page.locator('div[title="Profile details"]')
        await profile_locator.click()
        await asyncio.sleep(1.2)

        no_of_media_locator = page.locator(
            '//*[@id="app"]/div/div/div[3]/div/div[6]/span/div/span/div/div/div/section/div[4]/div[1]/div/div[2]/div/div')
        count_text = await no_of_media_locator.text_content()
        print(f"no of media is {count_text}")

        try:
            count_text = int(count_text)
        except ValueError:
            print("value is not an integer")


        out_dir = pathlib.Path("whatsappImages").resolve()
        out_dir.mkdir(exist_ok=True)

        await page.wait_for_selector('div[aria-label=" Image"]')
        image_locator = page.locator('div[aria-label=" Image"]').first
        await image_locator.click()

        for i in range(1,count_text):
            await page.wait_for_selector('img[src]', timeout=15_000)
            await page.wait_for_load_state("networkidle")
            big_img = page.locator('img[src]').nth(1)

            try:
                await big_img.click()
                # await asyncio.sleep(0.01)
                await big_img.click()
            except Exception as e:
                print(e)


            # await asyncio.sleep(0.2)
            # await wait_for_image(big_img)
            src_url = await big_img.get_attribute("src")
            print("Found image URL:", src_url)

            await page.keyboard.press("ArrowLeft")







        # image_locator = page.locator('div[aria-label=" Image"]').first
        # await image_locator.click()



        await asyncio.sleep(1000000)

        # try:
        #     while True:
        #         await asyncio.sleep(1)
        # except KeyboardInterrupt:
        #     print("Browser closed.")

        context.close()
        print("Browser closed")


if __name__ == "__main__":
    asyncio.run(main())


