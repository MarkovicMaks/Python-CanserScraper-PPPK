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
urlbase = 'https://xenabrowser.net/datapages/'
urlOne = urlbase + '?hub=https://tcga.xenahubs.net:443'
driver.get(urlOne)
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
            full_link = urlbase + link  # Create the full URL
            print(f"Visiting: {full_link}")

            driver.get(full_link)
            time.sleep(5) 
            
            new_page_html = driver.page_source
            new_page_soup = BeautifulSoup(new_page_html, 'html.parser')

            
            pancan_link_tag = new_page_soup.find('a', string=lambda text: text and text.endswith('pancan normalized'))
            if pancan_link_tag:
                pancan_link = pancan_link_tag['href']
                pancan_link_Full = urlbase + pancan_link
                print(f"Found pancan normalized link: {pancan_link_Full}")

                driver.get(pancan_link_Full)
                time.sleep(5)  # Wait for the pancan normalized page to load
                
                # Scrape the desired data from the pancan normalized page
                pancan_page_html = driver.page_source
                pancan_page_soup = BeautifulSoup(pancan_page_html, 'html.parser')

                # span_tag = soup.find('span', string=lambda text: text and 'download' in text.lower())

                # if span_tag:
                #     # Now find the <a> tag following this span (or within the same parent) to get the download link
                #     a_tag = span_tag.find_next('a', href=True)  # find the next <a> tag after the span
                #     if a_tag:
                #         download_link = a_tag['href']
                #         print(f"Found download link: {download_link}")
                #     else:
                #         print("No <a> tag found near the 'download' span.")
                # else:
                #     print("No 'download' span found.")
                
            else:
                print("No pancan normalized link found on this page.")
            driver.back()
            time.sleep(2)  # Wait for the main page to reload
else:
    print("The <ul> element was not found.")

# Close the driver
driver.quit()
