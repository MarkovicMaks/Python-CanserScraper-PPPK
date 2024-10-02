from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options
options = Options()
options.headless = True

# Path to your ChromeDriver
chrome_driver_path = 'C:/Users/Korisnik/Desktop/chromedriver-win64/chromedriver.exe'

# Start the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Main URL to scrape
url = 'https://tcga.xenahubs.net'
driver.get(url)
time.sleep(5)  # Wait for the page to load

# Get the page source
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find the <ul> element and then all <li> within it
ul_element = soup.find('ul')

if ul_element:
    # Extract all <li> elements
    li_elements = ul_element.find_all('li')
    for li in li_elements:
        # Find the <a> tag within each <li>
        a_tag = li.find('a')
        if a_tag:
            link = a_tag['href']
            full_link = url + link  # Create the full URL
            print(f"Visiting: {full_link}")

            # Navigate to the link
            driver.get(full_link)
            time.sleep(5)  # Wait for the new page to load
            
            # Scrape the data from the new page
            new_page_html = driver.page_source
            new_page_soup = BeautifulSoup(new_page_html, 'html.parser')

            # Look for the link with title "pancan normalized"
            pancan_link_tag = new_page_soup.find('a', string=lambda text: text and text.endswith('pancan normalized'))
            if pancan_link_tag:
                pancan_link = pancan_link_tag['href']
                print(f"Found pancan normalized link: {pancan_link}")

                # Navigate to the pancan normalized link
                driver.get(pancan_link)
                time.sleep(5)  # Wait for the pancan normalized page to load
                
                # Scrape the desired data from the pancan normalized page
                pancan_page_html = driver.page_source
                pancan_page_soup = BeautifulSoup(pancan_page_html, 'html.parser')

                # Example: Scrape some specific data from the pancan page
                # Update this selector to match what you need from the pancan normalized page
                data_element = pancan_page_soup.find('div', class_='your-target-class')  # Update with the actual class or tag you need
                if data_element:
                    print(data_element.text.strip())  # Print or process the scraped data
                else:
                    print("Desired data not found on the pancan normalized page.")
            else:
                print("No pancan normalized link found on this page.")

            # Go back to the main page
            driver.back()
            time.sleep(5)  # Wait for the main page to reload
else:
    print("The <ul> element was not found.")

# Close the driver
driver.quit()
