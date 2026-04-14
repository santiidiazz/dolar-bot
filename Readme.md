# 🤖 DolarBot 

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)

> **An automated Python monitor for Argentine Dollar exchange rates.** > Fetches daily rates (Blue, Oficial, Bolsa, etc.) and delivers a comprehensive daily report straight to your inbox, featuring an HTML summary and a styled Excel attachment.

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [💡 Use Cases](#-use-cases)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [💻 Usage](#-usage)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

* **📡 Real-Time Data:** Fetches the latest exchange rates directly from the public `dolarito.ar` API.
* **📊 Excel Reports:** Automatically generates clean, color-coded `.xlsx` spreadsheets tailored to different exchange types.
* **📧 Smart Email Alerts:** Sends a beautifully formatted HTML email containing a price table. Includes custom alerts if the *Blue* dollar spikes.
* **💾 Historical Tracking:** Appends daily queries to a local `.csv` file, building a database for future financial analysis.
* **⏱️ Automated Scheduling:** Set it and forget it. Can be configured to run automatically every day at 9:00 AM.

---

## 💡 Use Cases

* **⏱️ Time-Saving:** Eliminates the need to manually refresh financial portals every morning.
* **📈 Decision Making:** Get immediate alerts on your phone or email when the market experiences sudden, sharp variations.
* **🗃️ Accounting Records:** The generated Excel attachments serve as a reliable historical ledger for administration and accounting teams.

---

## 🛠️ Tech Stack

This project leverages powerful Python libraries for web scraping, data manipulation, and automation:

* **[`requests`](https://pypi.org/project/requests/)** — For handling HTTP calls to the API.
* **[`pandas`](https://pandas.pydata.org/)** — For robust data processing and CSV management.
* **[`openpyxl`](https://openpyxl.readthedocs.io/)** — To generate and format the Excel reports.
* **[`smtplib`](https://docs.python.org/3/library/smtplib.html)** — Built-in Python library for routing emails via Gmail.
* **[`schedule`](https://pypi.org/project/schedule/)** — For lightweight, human-readable daily task automation.
* **[`python-dotenv`](https://pypi.org/project/python-dotenv/)** — For secure environment variable management.

---

## 📂 Project Structure

```text
dolar_bot/
├── scraper.py           # Main entry point and data fetching
├── excel_report.py      # Handles .xlsx generation and styling
├── email_sender.py      # Crafts the HTML and dispatches the email
├── scheduler.py         # Automates the bot's daily execution
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (Ignored by Git)

Getting Started
Prerequisites
Make sure you have Python 3.8+ installed on your system.

Installation
Clone the repository:

Bash
git clone [https://github.com/santiidiazz/dolar-bot.git](https://github.com/santiidiazz/dolar-bot.git)
cd dolar-bot
Install dependencies:

Bash
pip install -r requirements.txt
Configuration
You need to set up your email credentials securely. Create a .env file in the root directory of the project:

Code snippet
EMAIL_ORIGEN=your_email@gmail.com
EMAIL_DESTINO=recipient_email@gmail.com
EMAIL_PASS="your16characterapppassword"
⚠️ IMPORTANT: About EMAIL_PASS
This should not be your regular Gmail password. You must use a Google App Password.

Go to myaccount.google.com.

Navigate to Security -> 2-Step Verification -> App Passwords.

Generate a new password. Copy the 16-character code, remove all spaces, and wrap it in quotes in your .env file.

💻 Usage
Depending on your needs, you can run DolarBot once or leave it running in the background.

Option A: Run Manually (Once) To fetch the data and send the email immediately:

Bash
python scraper.py
Option B: Schedule Daily Execution To leave the bot running so it automatically triggers every day at 9:00 AM:

Bash
python scheduler.py
🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to check out the issues page if you want to contribute.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request