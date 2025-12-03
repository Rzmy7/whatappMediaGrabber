import aiofiles, pathlib
import asyncio
from playwright.async_api import async_playwright,Page
from typing import Union
import os

# chat_name = "🌿🍃🎼🎙️"


async def download_image(
    page: Page, 
    image_source: Union[str, any],  # URL string or locator/element
    save_path: str,
    create_dirs: bool = True
) -> bool:
    """
    Download an image from a page and save it locally using browser's fetch API.
    
    Args:
        page: Playwright page object
        image_source: Either a direct image URL (str) or a Playwright locator/element
        save_path: Full path where the image should be saved (e.g., '/path/to/image.png')
        create_dirs: If True, creates parent directories if they don't exist
    
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        # If image_source is a locator/element, extract the src attribute
        if not isinstance(image_source, str):
            # Assume it's a locator or element handle
            image_url = await image_source.get_attribute('src')
            if not image_url:
                print("Could not find 'src' attribute on the element")
                return False
        else:
            image_url = image_source
            
        # Create directories if needed
        if create_dirs:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Get image bytes using fetch inside the browser
        img_bytes = await page.evaluate(
            """async url => {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const buffer = await response.arrayBuffer();
                return Array.from(new Uint8Array(buffer));
            }""",
            image_url,
        )
        
        # Write to file
        with open(save_path, 'wb') as file:
            file.write(bytes(img_bytes))
            
        print(f"✓ Image downloaded successfully: {save_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download image: {e}")
        return False



async def grabber(chat_name: str):
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
            
            for i in range(1, count_text+1):
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
                    await page.wait_for_selector('button[aria-label="Previous"]', timeout=15_000)
                    
                    try:
                        prev_button = page.locator('button[aria-label="Previous"]')
                        prev_button_state = await prev_button.get_attribute('aria-disabled')
                        # print("[PrevButton Status] : ",prev_button_state)
                        
                        await download_image(page, src_url, str(out_dir / f"{chat_name}_image_{i}.png"))
                        
                        if (prev_button_state == 'false') :
                            await prev_button.click()
                        elif (prev_button_state == 'true') :
                            print("End of the Images")
                            break
                            
                    except Exception as e:
                        print(f"[Image {i} Previous Button locating] Exception: {e}")
                except Exception as e:
                    print(f"[Image {i} Previous Button waiting] Exception: {e}")

                # try:
                #     await page.keyboard.press("ArrowLeft")
                # except Exception as e:
                #     print(f"[Image {i} ArrowLeft] Exception: {e}")

                # await asyncio.sleep(0.2)
                # await wait_for_image(big_img)

            # image_locator = page.locator('div[aria-label=" Image"]').first
            # await image_locator.click()

            # try:
            #     await asyncio.sleep(1000000)
            # except asyncio.CancelledError:
            #     print("[Sleep] Cancelled")
            # except Exception as e:
            #     print(f"[Sleep] Exception: {e}")
            # await asyncio.sleep(60)

            try:
                await context.close()
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
        chat_name = input("Enter the exact chat or group name (with emojis if any): ")
        await grabber(chat_name)
    elif selection==3:
        exit

if __name__ == "__main__":
    try:
        asyncio.run(menu())
    except Exception as e:
        print(f"[Asyncio Run] Exception: {e}")