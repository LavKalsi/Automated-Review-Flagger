# Automated-Review-Flagger

This project automates the process of logging into Gmail, searching for a business on Google, and reporting Google reviews with a rating less than 3 using Selenium and undetected-chromedriver.

## Features

- Automated Gmail login (using provided XPaths)
- Google search for a business (e.g., "Cuilsoft")
- Navigates to the business reviews page
- Loads all reviews and reports those with a rating less than 3
- Handles popups, tabs, and avoids duplicate reporting
- Tracks and prints the number of reviews reported

## Requirements

- Python 3.8+
- Google Chrome browser
- ChromeDriver (handled automatically by undetected-chromedriver)
- The following Python packages (install with pip):

## Usage

1. **Clone the repository** and navigate to the project folder.

2. **Install dependencies:**
    ```
    pip install -r [requirements.txt](http://_vscodecontentref_/1)
    ```

3. **Edit the script:**
    - Open `Script.py` (or `testfile.py` if you use that name).
    - Replace the placeholder email and password with your own Gmail credentials:
      ```python
      human_typing(email_input, "your_mail@gmail.com")  # <-- Replace with your email
      human_typing(password_input, "your_password")      # <-- Replace with your password
      ```
    - Optionally, change the business name in the search step.

4. **Run the script:**
    ```
    python [Script.py](http://_vscodecontentref_/2)
    ```

5. **What the script does:**
    - Logs into Gmail via Google search.
    - Searches for the specified business.
    - Opens the reviews page and loads more reviews as needed.
    - Reports reviews with a rating less than 3, one at a time, and prints progress.
    - Closes the browser cleanly when done.

## Notes

- This script is for educational and research purposes only. Use responsibly and in accordance with Google's terms of service.
- If you encounter issues with element XPaths, update them as needed (Google may change their page structure).
- For best results, use a dedicated Gmail account for automation.

## License

MIT License
