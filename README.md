# 🕵️‍♂️ AI-Powered Web Scraping Legality Checker

A Python script that helps you determine whether it is **legal or potentially illegal** to scrape a given website.  
It analyzes `robots.txt`, Terms of Service, Privacy Policy, anti-bot headers, login protection, and API docs — then uses **OpenAI GPT-4o** to provide a legal opinion.

---

## ✅ Features

- Analyze `robots.txt` access rules
- Auto-discover Terms and Privacy pages
- Scrape and extract legal text from the site
- Detect login barriers
- Detect anti-bot headers (e.g., `X-Robots-Tag`)
- Discover common API documentation endpoints
- Uses GPT-4o for legal analysis
- Lightweight and CLI-based

---

⚠️ This tool is an AI-powered early warning system — it helps you assess risk, but does not replace professional legal advice. Use it to stay informed and responsible.


## 📦 Requirements

- Python 3.8 or higher
- OpenAI API key (GPT-4o access)

---

## 🧪 Libraries Used

- `requests`  
- `beautifulsoup4`  
- `python-dotenv`  

Install dependencies using:

```bash
pip install -r requirements.txt


🔐 Setup Instructions
Clone the repository


git clone https://github.com/your-username/legal-scraper-checker.git
cd legal-scraper-checker
Create a .env file


OPENAI_API_KEY=sk-proj-your-key-here
Install required packages


pip install -r requirements.txt

🚀 Usage
Run the script to analyze a website:


python legal_test.py
By default, it checks:


check_website_legality("https://www.yourwebsite.com")
You can replace that URL in legal_test.py to check any site.

🧠 How It Works
Downloads and reads /robots.txt

Auto-detects and fetches Terms of Service / Privacy Policy

Scrapes legal content using BeautifulSoup

Checks for login prompts, API paths, and suspicious headers

Builds a full legal context prompt

Sends it to OpenAI GPT-4o for a clear legal recommendation

Displays the result in your terminal

🛡️ Disclaimer
This tool provides an AI-generated opinion for educational and compliance awareness purposes only.
Always seek professional legal advice for final decisions on web scraping.

📜 License
MIT License - Free for personal and commercial use.

🌟 Contribute
Contributions, feedback, and pull requests are welcome!
If this tool helps you, give it a ⭐ on GitHub.
