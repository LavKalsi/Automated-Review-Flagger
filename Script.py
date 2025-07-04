import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import hashlib

def human_typing(element, text, delay_range=(0.1, 0.3)):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))

# Setup undetected Chrome
driver = uc.Chrome(options=uc.ChromeOptions())
wait = WebDriverWait(driver, 20)

try:
    # 1. Open Google and search for 'gmail'
    driver.get("https://www.google.com")
    time.sleep(2)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    human_typing(search_box, "gmail")
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)

    # 2. Click the Gmail link (search result)
    gmail_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/h3')))
    gmail_link.click()

    # 2.1 Click the button on the Gmail landing page before proceeding
    special_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/header/div/div[5]/a[2]')))
    special_btn.click()

    # 3. Enter email in the identifier input
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    human_typing(email_input, "your_mail@gmail.com")  # <-- Replace with your email

    # 4. Click the Next button after email
    next_btn_email = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button/span')))
    next_btn_email.click()

    # 5. Enter password in the password input
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    human_typing(password_input, "your_password")  # <-- Replace with your password

    # 6. Click the Next button after password
    next_btn_password = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button/span')))
    next_btn_password.click()

    # 7. Go back to Google home page
    driver.get("https://www.google.com")

    # --- Begin review reporting automation using the same driver ---
    # Search for the company
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    ActionChains(driver).move_to_element(search_box).click().perform()
    time.sleep(1)
    human_typing(search_box, "Cuilsoft")
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)

    # Click the "X reviews" link in the knowledge panel (right side)
    try:
        reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="bkaPDb"]//span[text()="Reviews"]/ancestor::a')
            )
        )
        reviews_button.click()
        print("Clicked the correct Reviews button below the image.")
    except Exception as e:
        print(f"Could not click the Reviews button: {e}")
        driver.quit()
        exit()

    time.sleep(4)

    # Click the "More user reviews" button if present
    try:
        more_reviews_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "PBBEhf") and contains(@class, "JGD2rd") and .//span[contains(text(), "More user reviews")]]')
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_reviews_btn)
        time.sleep(1)
        more_reviews_btn.click()
        print("Clicked 'More user reviews' button.")
        time.sleep(5)
        # Debug: print first 20 divs' classes and text after clicking
        debug_divs = driver.find_elements(By.XPATH, '//div')[:20]
        print("[DEBUG] First 20 divs after clicking 'More user reviews':")
        for idx, div in enumerate(debug_divs):
            try:
                print(f"[DEBUG] Div {idx}: class='{div.get_attribute('class')}', text='{div.text.strip()[:100]}'")
            except Exception:
                continue
        time.sleep(3)
    except Exception as e:
        print(f"Could not click the 'More user reviews' button: {e}")

    # Scroll down and try to click the "More user reviews" button (by text only)
    for _ in range(10):  # Try up to 10 scrolls
        try:
            more_reviews_btn = driver.find_element(By.XPATH, '//*[text()="More user reviews"]')
            if more_reviews_btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_reviews_btn)
                time.sleep(1)
                more_reviews_btn.click()
                print("Clicked 'More user reviews' button.")
                time.sleep(3)
                break
        except Exception:
            pass
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(0.7)
    else:
        print("Could not find or click the 'More user reviews' button after scrolling.")

    # --- NEW LOGIC: Loop through review blocks and report low ratings ---
    processed_reviews = set()
    reported_count = 0  # Counter for reported reviews
    while True:
        review_blocks = driver.find_elements(By.XPATH, '//div[contains(@class, "bwb7ce")]')
        print(f"{len(review_blocks)} review blocks found.")
        report_handled = False  # Track if a report was handled this cycle
        for block in review_blocks:
            try:
                # Extract reviewer name and review text for unique ID
                try:
                    reviewer_name = block.find_element(By.XPATH, './/span[contains(@class, "TSUbDb")]').text.strip()
                except Exception:
                    reviewer_name = ''
                try:
                    review_text = block.find_element(By.XPATH, './/span[contains(@class, "review-full-text")]').text.strip()
                except Exception:
                    try:
                        review_text = block.find_element(By.XPATH, './/span[contains(@class, "review-snippet")]').text.strip()
                    except Exception:
                        review_text = ''
                review_id = hashlib.sha256((reviewer_name + review_text).encode('utf-8')).hexdigest()
                if review_id in processed_reviews:
                    continue  # Skip already processed reviews
                rating_div = block.find_element(By.XPATH, './/div[contains(@class, "dHX2k")]')
                aria_label = rating_div.get_attribute('aria-label')
                rating = None
                if aria_label and 'Rated' in aria_label:
                    rating_str = aria_label.split('Rated')[1].split('out')[0].strip()
                    try:
                        rating = float(rating_str)
                    except Exception:
                        pass
                if rating is not None:
                    print(f"Block rating: {rating}")
                    if rating < 3:
                        print("Low rating found, attempting to click report button.")
                        try:
                            # Find the report button by jsname and click its parent button
                            report_btn = block.find_element(By.XPATH, './/div[@jsname="s3Eaab"]/parent::button')
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", report_btn)
                            time.sleep(0.5)
                            report_btn.click()
                            print("Clicked report button for low rating.")
                            time.sleep(2)
                            # --- Find the "Report review" link using KgoSse class and open in a new tab ---
                            try:
                                links = driver.find_elements(By.XPATH, '//a[contains(@class, "KgoSse")]')
                                for link in links:
                                    if link.is_displayed() and link.text.strip() == "Report review":
                                        report_url = link.get_attribute('href')
                                        if report_url:
                                            driver.execute_script("window.open(arguments[0]);", report_url)
                                            print("Opened report link in new tab.")
                                            time.sleep(2)
                                            # Switch to new tab
                                            driver.switch_to.window(driver.window_handles[-1])
                                            # Click the 'Not helpful' button (new XPATH)
                                            try:
                                                not_helpful_btn = WebDriverWait(driver, 10).until(
                                                    EC.element_to_be_clickable((
                                                        By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz/div/ul/li[7]/a'
                                                    ))
                                                )
                                                not_helpful_btn.click()
                                                print("Clicked 'Not helpful' in report tab.")
                                                time.sleep(1)
                                                # Click the next button (confirmation)
                                                confirm_btn = WebDriverWait(driver, 10).until(
                                                    EC.element_to_be_clickable((
                                                        By.XPATH,
                                                        '//*[@id="yDmH0d"]/c-wiz[2]/div/div[4]/div/div/button/span'
                                                    ))
                                                )
                                                confirm_btn.click()
                                                print("Clicked confirmation button in report tab.")
                                            except Exception as e:
                                                print(f"Could not complete report actions: {e}")
                                            time.sleep(1)
                                            driver.close()
                                            driver.switch_to.window(driver.window_handles[0])
                                            print("Closed report tab and returned to main tab.")
                                            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                                            # Mark as processed and increment counter
                                            processed_reviews.add(review_id)
                                            reported_count += 1
                                            print(f"[PROGRESS] Reported {reported_count} reviews so far.")
                                        break  # Only process the first visible "Report review" link
                            except Exception as e:
                                print(f"Could not open report link: {e}")
                            report_handled = True
                            break  # Stop after handling one report
                        except Exception as e:
                            print(f"Could not click report button: {e}")
            except Exception as e:
                print(f"Error processing block: {e}")
        if report_handled:
            continue  # Go back to the top of the while loop to refresh blocks and process one at a time

        # Try to load more reviews if available
        try:
            more_reviews_btn = driver.find_element(
                By.XPATH,
                '//*[@id="kp-wp-tab-LocalPoiReviews"]/div[16]/div/div/div/div/div/div/div[2]/c-wiz/div/div[6]/div/div[2]/div/div/span[1]'
            )
            if more_reviews_btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_reviews_btn)
                time.sleep(0.5)
                more_reviews_btn.click()
                print("Clicked 'More user reviews' button (using provided XPath).")
                time.sleep(2)

                # --- Find and process the "Report review" link before continuing ---
                try:
                    links = driver.find_elements(By.XPATH, '//a[contains(@class, "KgoSse")]')
                    for link in links:
                        if link.is_displayed() and link.text.strip() == "Report review":
                            report_url = link.get_attribute('href')
                            if report_url:
                                driver.execute_script("window.open(arguments[0]);", report_url)
                                print("Opened report link in new tab.")
                                time.sleep(2)
                                driver.switch_to.window(driver.window_handles[-1])
                                try:
                                    not_helpful_btn = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((
                                            By.XPATH,
                                            '//span[contains(text(), "Not helpful") or contains(text(), "not helpful") or contains(text(), "Not Useful") or contains(text(), "not useful")]'
                                        ))
                                    )
                                    not_helpful_btn.click()
                                    print("Clicked 'Not helpful' in report tab.")
                                except Exception as e:
                                    print(f"Could not click 'Not helpful': {e}")
                                time.sleep(1)
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                print("Closed report tab and returned to main tab.")
                            break  # Only process the first visible "Report review" link
                except Exception as e:
                    print(f"Could not open report link: {e}")

                continue  # Only continue after reporting process is done
        except Exception:
            print("No more 'More user reviews' button found (using provided XPath).")
        break  # Exit loop if no more reviews to load
    print(f"\nAll done! Total reviews reported: {reported_count}")
finally:
    try:
        driver.quit()
        print("Browser closed cleanly.")
    except Exception as e:
        print(f"Error closing browser: {e}")

