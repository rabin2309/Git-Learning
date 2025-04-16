import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver with Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:/Users/HP/AppData/Local/Google/Chrome/User Data')
options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://tutorialsninja.com/demo/")
    time.sleep(3)

    # Get cookies from the browser session
    cookies = driver.get_cookies()

    # Set up a session for the API request/server
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Search for "Iphone" on the website
    driver.find_element(By.NAME, "search").send_keys("Iphone")
    driver.find_element(By.CLASS_NAME, "btn-default").click()
    time.sleep(3)

    # Get product names from the frontend
    frontend_products = [product.text for product in driver.find_elements(By.XPATH, "//a[normalize-space()='iPhone']")]
    print("Frontend Products:", frontend_products)

    # Request backend data from the API
    response = session.get("https://dummyjson.com/products", params={"limit": 10})

    if response.status_code == 200:
        backend_data = response.json()
        product_names = [product["title"] for product in backend_data["products"]]

        print("Backend Products:", product_names)

        # Validation
        if "MacBook Air" in product_names:
            print("Validation Success: 'MacBook Air' exists in the API response.")
        else:
            print("Validation Failed: 'MacBook Air' not found.")
    else:
        print(f"API request failed: {response.status_code}")

finally:
    driver.quit()