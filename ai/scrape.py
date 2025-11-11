import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

# https://techwithtim.net
# https://www.lambdatest.com/blog/automate-login-page-using-selenium-webdriver/#:~:text=the%20login%20functionality.-,Automating%20the%20Login%20page,to%20start%20the%20different%20browsers.&text=WebDriver%20driver%20=%20new%20EdgeDriver(),successfully%20logged%20into%20the%20website.


def scrape_website(url):

    print(f"Scraping URL: {url}")
    # Set up the Chrome WebDriver (make sure to specify the correct path to chromedriver)
    chromedriver_path = '.\chromedriver.exe'  # Update this path
    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Extract the page source
        page_source = driver.page_source
        time.sleep(10)  # Wait for 10 seconds to ensure the page loads completely

        return page_source
    
    finally:
        driver.quit()


def extract_body_content(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    body = soup.body
    return body.get_text() if body else ''


def clean_body_content(body_text):
    soup = BeautifulSoup(body_text, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    cleaned_text = soup.get_text(separator='\n')
    cleaned_text = '\n'.join(line.strip() for line in cleaned_text.splitlines() if line.strip())

    return cleaned_text


def split_dom_content(dom_content, chunk_size=6000):
    return [
        dom_content[i:i + chunk_size] for i in range(0, len(dom_content), chunk_size)
    ]


def login_to_sso(url, username, password):
    # Web Scrape Websites with a LOGIN - Python Basic Auth
    # https://www.youtube.com/watch?v=cV21EOf5bbA

    chromedriver_path = '.\chromedriver.exe'  # Update this path
    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        username_field = driver.find_element("name", "username")
        password_field = driver.find_element("name", "password")
        login_button = driver.find_element("name", "signin")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        time.sleep(5)  # Wait for login to complete

        return driver.page_source

    finally:
        driver.quit()