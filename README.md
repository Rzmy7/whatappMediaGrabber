# WhatsApp Media Grabber (Playwright Python)

A simple **Python + Playwright** script to **download all images** from a specific WhatsApp chat or group using WhatsApp Web.

Perfect for backing up photos from family groups, work chats, or meme channels — without manually clicking hundreds of times!

---

## Features
- Log in once using your WhatsApp Web QR code (saved in persistent profile)
- Search and open any chat/group by exact name (supports emojis)
- Automatically opens the Media section and downloads **every image**
- Saves images as `ChatName_image_1.png`, `ChatName_image_2.png`, etc.
- Smart navigation using the "Previous" button in the image viewer
- Fully async with proper error handling
- Works on Windows, macOS, and Linux

---

## Requirements

- Python 3.8+
- Playwright (`pip install playwright`)
- Chromium browser (installed automatically by Playwright)

---

## Installation

```bash
# Clone or download this script
git clone https://github.com/yourusername/whatsapp-image-grabber.git
cd whatsapp-image-grabber

# Install playwright
pip install playwright

# Install chromium
playwright install chromium

```



---
## Usage

### Run the Script
```bash
python main.py
```

### Choose an Option
```bash
1. Sync or Login
2. Grab some images from a whatsapp chat or Group
3. Exit
Choose what you want?
```

### Option 1 - Sync/Login
This will:
- Launch WhatsApp Web
- Allow you to scan QR code
- Save the login session to playwright_profile/
- Close the browser only when you press Enter

Use this the first time you run the tool.


### Option 2 - Download Images
You will be asked :
```
Enter the exact group name (with emojis if any):
```

Example:
```
Family❤️
```

The script will then:

1. Open WhatsApp Web

2. Search for the chat

3. Open the profile sidebar

4. Read total media count

5. Open the first/last image

6. Walk backward through all images


Save them to:
```
whatsappImages/<ChatName>_image_<index>.png
```

### Saved Example:
```
whatsappImages/
  ├── Family ❤️_image_1.png
  ├── Family ❤️_image_2.png
  └── Family ❤️_image_3.png
```

---

## Notes and Tips
- Keep the chat name EXACT (emojis, punctuation, capital letters).

- If WhatsApp changes its UI, some selectors may need adjustments.

- The script works best on stable internet.

- Large groups with thousands of images may take time.


