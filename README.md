# Classroom Harvester 🕷️

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
