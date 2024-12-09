from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from collections import Counter

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random

# Set up Chrome options to maximize the window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Step 1: Open the website
    driver.get("https://www.radiustheme.com/demo/wordpress/themes/zilly/")
    print("Website opened successfully.")
    
    # Step 2: Locate the "Trending Products" section
    trending_section = driver.find_element(By.XPATH, "//*[@data-id='d78b728']")
    
    # Scroll to the "Trending Products" section
    driver.execute_script("arguments[0].scrollIntoView();", trending_section)
    print("Navigated to the 'Trending Products' section.")
    
    # Step 3: Fetch items and categories
    # Locate all items in the section
    items = trending_section.find_elements(By.XPATH, ".//div[contains(@class, 'rtsb-product-content')]")
    # print(items)
    
    category_counts = Counter()
    total_count = 0
    
    for item in items:
        # Locate the category of each item
        category_element = item.find_element(By.XPATH, ".//li[contains(@class, 'rtsb-category-list-item')]")
        category = category_element.text.strip()
        # print(category)
        
        # Update counts
        category_counts[category] += 1
        total_count += 1
    
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    print(f"Total count: {total_count}")
    print("Fetched the counts of items in the 'Trending Products' Section.")
    
    # Step 4: Locate and click on the "See More" CTA
    # Scroll up a little bit, 100px
    driver.execute_script("window.scrollBy(0, -100);")
    see_more_link = driver.find_element(By.XPATH, "(//div[contains(@class, 'more-button')])[2]")
    # Wait to load the "See More" button
    time.sleep(2)
    
    # Click the "See More" CTA link
    actions = ActionChains(driver)
    actions.move_to_element(see_more_link).click().perform()
    print("Clicked 'See More'.")

    # Step 5: Click on "Load More" button unitl it disappears
    while True:
        try:
            # Locate the "Load More" button
            load_more_button = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='rtsb-load-more rtsb-pos-r']//button"))
            )
    
            # Click the "Load More" button
            actions = ActionChains(driver)
            actions.move_to_element(load_more_button).click().perform()
            print("Clicked 'Load More'.")
            
            # Scroll down to just before the end of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 900);")
        except Exception as e:
            # Break the loop if the "Load More" button is not found
            print("Reached the end of the page.")
            break
        
    # Ensure inview
    # Scroll down to just before the end of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 900);")
    time.sleep(2)
    # Scroll to the start of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    # Step 6: Fetch items and categories in the 'Shop' section
    print("Navigated to the 'Shop' section.")
    # Locate the "Shop" section
    shop_section = driver.find_element(By.XPATH, "//*[@data-id='eda8704']")
    # Locate all items in the section
    itemS = shop_section.find_elements(By.XPATH, ".//div[contains(@class, 'rt-product-block')]")
    # print(itemS)
    
    category_countS = Counter()
    total_counT = 0
    
    for item in itemS:
        # Locate the category of each item
        category_element = item.find_element(By.XPATH, ".//div[contains(@class, 'product-cat')]")
        category = category_element.text.strip()
        # print(category)
        
        # Update counts
        category_countS[category] += 1
        total_counT += 1
    
    for category, count in category_countS.items():
        print(f"{category}: {count}")
    print(f"Total count: {total_counT}")
    print("Fetched the counts of items in the 'Shop'section.") 
    
    # Step 7: Click 'Add to card' CTA for any one item
    try:
        # Locate the product section
        product_section = driver.find_element(By.XPATH, "//*[@data-id='eda8704']")
        
        # Locate all "Add to Cart" buttons within this section
        add_to_cart_buttons = product_section.find_elements(By.XPATH, "//a[@title='Add to cart']")
        
        if add_to_cart_buttons:   
            # Select a random index from the list of "Add to Cart" buttons
            random_index = random.randint(0, len(add_to_cart_buttons) - 1)
                     
            # Select the random "Add to Cart" button
            add_to_cart_button = add_to_cart_buttons[random_index]
            
            # Scroll to the button to ensure it's in view
            driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
            
            # Click the button (to avoid following the link in href)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        
            print("Clicked 'Add to Cart'.")
            time.sleep(5)
    except Exception as e:
        print(f"An error occurred while adding to cart: {e}")

    # Step 8: Click View Cart CTA to navigate to the cart page
    try:
        # Locate and Wait for the "View Cart" button to be clickable
        view_cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='button wc-forward']"))
        )
        
        # Scroll to the "View Cart" button to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView(true);", view_cart_button)
        
        # Wait briefly to ensure the scroll action completes
        time.sleep(1)

        # Click the "View Cart" button
        actions = ActionChains(driver)
        actions.move_to_element(view_cart_button).click().perform()
        print("Clicked 'View Cart' and navigated to the cart page.")

        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while navigating to the cart page: {e}")

    # Step 9: Click on plus CTA to add one more quantity
    try:
        # Locate the form
        cart_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-cart-form"))
        )
        
        # Locate the "Plus" button
        plus_button = cart_form.find_element(By.XPATH, ".//button[@class='rtsb-quantity-btn rtsb-quantity-plus']")
    
        # Scroll to the button to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
        
        # Click the "Plus" button
        plus_button.click()
        print("Clicked 'Plus'.")
        
        # Scroll down, 150px
        driver.execute_script("window.scrollBy(0, 150);")
    
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while clicking 'Plus' button: {e}")
        
    # Step 10: Remove item from cart
    try:
        # Locate the "Remove" link element
        remove_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'remove') and contains(@href, 'remove_item')]"))
        )
    
        # Extract the href attribute
        remove_url = remove_button.get_attribute("href")
    
        # Navigate to the URL to trigger item removal
        driver.get(remove_url)
    
        print("Clicked 'Remove'.")
        
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
        
    # Step 11: Click on Return to shop CTA
    try:
    # Locate the "Return to Shop" button
        return_to_shop_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'wc-backward') and contains(text(), 'Return to shop')]"))
        )
    
        # Click the button
        return_to_shop_button.click()
        print("Clicked 'Return to Shop'.")
    except Exception as e:
        print(f"An error occurred while clicking 'Return to Shop' button: {e}")

    # Step 12: Type a search term in the search box
    try:
        # Locate the search input field
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control product-search-form product-autocomplete-js']"))
        )
    
        # Type the search term
        search_term = "fresh"
        search_box.send_keys(search_term)
        print(f"Typed '{search_term}' in the search box.")
        
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while typing in the search box: {e}")
        
    # Step 13: Fetch the count of search suggestions and items full names
    try:
        # Wait for the search suggestions to load
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='result-wrap']//ul/li"))
        )

        # Get the count of search suggestions
        suggestion_count = len(search_results)
        print(f"Number of search suggestions: {suggestion_count}")

        # Extract and print the full item names of the suggestions
        for i, result in enumerate(search_results, 1):
            item_name = result.find_element(By.XPATH, ".//h3[@class='title']/a").text
            print(f"Suggestion {i}: {item_name}")

        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while fetching the suggestions: {e}")
    
    
    print("Automation Done.")
except Exception as e:
    print(f"An error occured {e}")
    
finally:
    driver.quit()
    