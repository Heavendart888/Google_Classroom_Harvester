# Google Classroom Harvester 🕷️

**Classroom Harvester** is a Selenium-based automation tool designed to scrape, extract, and download all educational materials (PDFs, ZIPs, Code) from a Google Classroom feed.

Unlike basic downloaders, this tool includes "Topic Drill" logic to identify and expand nested "View More" pagination buttons, ensuring hidden or archived files are not missed.

## 🚀 Features
- **Stealth Mode:** Uses Selenium options to mask automation flags (`--disable-blink-features`).
- **Deep Harvesting:** Automatically clicks "View more" buttons inside specific topics to load older files.
- **Session Hijacking:** Reuses browser cookies to authenticate direct downloads from Google Drive.
- **Duplicate Handling:** Automatically renames duplicate filenames (e.g., `Notes (1).pdf`) instead of skipping them.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/heavendart888/Classroom-Harvester.git](https://github.com/heavendart888/Classroom-Harvester.git)
   cd Classroom-Harvester

```

2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Setup WebDriver**
* Download the [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) matching your browser version.
* Place `msedgedriver.exe` in the project folder.



## ⚡ Usage

1. Run the script:
```bash
python harvester.py

```


2. A browser window will open. **Log in** to your Google Account manually.
3. Navigate to the **Classwork** tab of your desired class.
4. Press `ENTER` in the terminal.
5. The bot will scroll, expand topics, and download all files to the `Classroom_Downloads/` folder.

## ⚠️ Disclaimer

This tool is for educational and personal archiving purposes only. Use responsibly.
