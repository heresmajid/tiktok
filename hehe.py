import streamlit as st
import undetected_chromedriver as uc

def run_selenium():
    # Start the undetected Chrome WebDriver in headless mode
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    driver = uc.Chrome(options=options)

    # Example: Navigate to TikTok
    driver.get('https://www.tiktok.com')

    # Example action: Get the page title
    st.write("Page Title:", driver.title)

    # Close the driver
    driver.quit()

# Streamlit UI
st.title("TikTok Automation with Selenium")
if st.button("Run Selenium"):
    run_selenium()
