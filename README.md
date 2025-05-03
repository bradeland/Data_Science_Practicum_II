# Data_Science_Practicum_II - Regis University, Denver Colorado

# 🔍 LinkedIn Experience Scraper

A Python-based tool to extract key details from the **Experience** section of public LinkedIn profiles. Built to help students and researchers save time manually gathering employment data.

## ✨ Features

- Extracts structured data from the Experience section of LinkedIn profiles
- Supports scraping multiple profiles in a loop
- Randomized delays to reduce risk of being flagged-I would try like a minute or two random sleeps!
- Saves output as `.csv` for easy analysis
- Has a section where you can QA your results and iterate between 2 tabs in a browser

## 📌 What It Extracts

From the most recent or all listed jobs:
- ✅ Job Title
- ✅ Company Name
- ✅ Employment Type (Full-time, Part-time, Internship, etc.)
- ✅ Employed or assumption of not employed if "present" is not in the first record of the experience
- ✅ LinkedIn URL for the person
- ✅ Location of the person being seearched (City, State)

## ⚙️ Requirements

- Python 3.9+
- Google Chrome + ChromeDriver (Installed on your project!)
- Gmail for sending the email to various recipients
- Packages:
  - `selenium`
  - `beautifulsoup4`
  - `pandas`
  - `time`, `random`
  - `email.message`
  - `dotenv`
  - `csv`
  - `smtplib`

