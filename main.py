import aiofiles, pathlib
import asyncio
from playwright.async_api import async_playwright

chat_name = "🌿🍃🎼🎙️"


async def wait_for_image(img_loc, timeout=15_000):
    """Wait until <img> is visible AND its bitmap loaded."""
    try:
        await img_loc.wait_for(state='visible', timeout=timeout)
        await img_loc.wait_for_function(
            "el => el.complete && el.naturalWidth > 0",
            timeout=timeout
        )
    except Exception as e:
        print(f"[wait_for_image] Exception: {e}")
        raise


async def main():
    try:
        async with async_playwright() as p:

            try:
                user_data_dir = "./playwright_profile"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False,
                    args=["--start-maximized"]  # optional: start browser maximized
                )
            except Exception as e:
                print(f"[Launch Context] Exception: {e}")
                return
            
            try:
                page = await context.new_page()
                page.set_default_timeout(60000)
                await page.goto("https://web.whatsapp.com/ ", wait_until="networkidle", timeout=10000000)
                print("Loaded WhatsApp…")
            except Exception as e:
                print(f"[Goto WhatsApp] Exception: {e}")
                await context.close()
                return
            
            try:
                await page.wait_for_selector('div[aria-label="Search input textbox"]')
                await page.wait_for_timeout(200)

                search_box = page.locator('div[aria-label="Search input textbox"]')
                await search_box.click()
                print("clicked search box")
            except Exception as e:
                print(f"[Search Box] Exception: {e}")
                await context.close()
                return
            
            try:
                await page.keyboard.type(chat_name)
                await asyncio.sleep(1.2)
            except Exception as e:
                print(f"[Type Chat Name] Exception: {e}")
                await context.close()
                return
            
            try:
                chat_locator = page.locator('span[title="' + chat_name + '"]').first
                await chat_locator.click()
                print(f"opned \"{chat_name}\" chat")
                await asyncio.sleep(1.2)
            except Exception as e:
                print(f"[Open Chat] Exception: {e}")
                await context.close()
                return
            
            try:
                profile_locator = page.locator('div[title="Profile details"]')
                await profile_locator.click()
                await asyncio.sleep(1.2)
                await page.wait_for_load_state("networkidle")
            except Exception as e:
                print(f"[Open Profile] Exception: {e}")
                await context.close()
                return
            
            try:
                no_of_media_locator = page.locator(
                    '//*[@id="app"]/div/div/div[3]/div/div[6]/span/div/span/div/div/div/section/div[4]/div[1]/div/div[2]/div/div')
                count_text = await no_of_media_locator.text_content()
                print(f"no of media is {count_text}")
            except Exception as e:
                print(f"[Get Media Count] Exception: {e}")
                await context.close()
                return
            
            try:
                count_text = int(count_text)
            except ValueError:
                print("value is not an integer")
            except Exception as e:
                print(f"[Convert Count] Exception: {e}")
            
            try:
                out_dir = pathlib.Path("whatsappImages").resolve()
                out_dir.mkdir(exist_ok=True)
            except Exception as e:
                print(f"[Create Directory] Exception: {e}")
            
            try:
                await page.wait_for_selector('div[aria-label=" Image"]')
                image_locator = page.locator('div[aria-label=" Image"]').first
                await image_locator.click(timeout=2_000)
            except Exception as e:
                print(f"[Click First Image] Exception: {e}")
                await context.close()
                return
            
            for i in range(1, count_text):
                try :
                    await page.wait_for_selector('img[src]', timeout=15_000)

                    try:
                        await page.wait_for_load_state("networkidle", timeout=6_000)
                        big_img = page.locator('img[src]').nth(1)

                        try:
                            await big_img.dblclick()
                            src_url = await big_img.get_attribute("src")
                            # await asyncio.sleep(3)
                            print("(" ,i," of ", count_text, ") Found image URL:", src_url)

                            # await page.keyboard.press("ArrowLeft")

                        except Exception as e:
                            print(f"[Image {i} Processing] Exception: {e}")

                    except Exception as e:
                        print(f"[Image {i} Load State] Exception: {e}")

                except Exception as e:
                    print(f"[Image {i} Selector] Exception: {e}")

                try:
                    await page.keyboard.press("ArrowLeft")
                except Exception as e:
                    print(f"[Image {i} ArrowLeft] Exception: {e}")

                # await asyncio.sleep(0.2)
                # await wait_for_image(big_img)

            # image_locator = page.locator('div[aria-label=" Image"]').first
            # await image_locator.click()

            try:
                await asyncio.sleep(1000000)
            except asyncio.CancelledError:
                print("[Sleep] Cancelled")
            except Exception as e:
                print(f"[Sleep] Exception: {e}")

            try:
                context.close()
                print("Browser closed")
            except Exception as e:
                print(f"[Context Close] Exception: {e}")

    except Exception as e:
        print(f"[Main] Fatal exception: {e}")


async def syncer():
    try:
        async with async_playwright() as p:

            try:
                user_data_dir = "./playwright_profile"
                context = await p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False,
                    args=["--start-maximized"]  # optional: start browser maximized
                )
            except Exception as e:
                print(f"[Launch Context] Exception: {e}")
                return
            
            try:
                page = await context.new_page()
                page.set_default_timeout(60000)
                await page.goto("https://web.whatsapp.com/ ", wait_until="networkidle", timeout=0)
                print("Loaded WhatsApp…")
                await asyncio.sleep(10000)
            except Exception as e:
                print(f"[Goto WhatsApp] Exception: {e}")
                await context.close()
                return
            
            try:
                ent = input("Press Enter to close browser...")  
                await context.close()
                print("Browser closed")
            except Exception as e:
                print(f"[Context Close] Exception: {e}")
            
    except Exception as e:
        print(f"[Syncer] Fatal exception: {e}")

async def menu():
    print("1.Sync or Login")
    print("2.Grab some images from a whatsapp chat or Group")
    print("3.Exit")
    print("Choose what you want?")
    selection = int(input("Enter the Number : "))
    if selection == 1:
        await syncer()
    elif selection == 2:
        await main()
    elif selection==3:
        exit

if __name__ == "__main__":
    try:
        asyncio.run(menu())
    except Exception as e:
        print(f"[Asyncio Run] Exception: {e}")