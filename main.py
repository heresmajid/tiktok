import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import pandas as pd
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import streamlit as st

# In[2]:

st.title("TikTok Scrolling...")
link_file = st.file_uploader("Choose Link Excel File", type=['csv', 'xlsx'])
output_filename = st.text_input("Output File Name")

while True:
    time.sleep(1)
    if link_file:
        break

if link_file:
    if link_file.name.endswith('.xlsx'):
        data_file = pd.read_excel(link_file)
    elif link_file.name.endswith('.csv'):
        data_file = pd.read_csv(link_file)

if link_file:
    starting_link = st.number_input('Starting Link Number:', min_value=0, value=0, step=1)
    ending_link = st.number_input('Ending Link Number:', min_value=0, value=len(data_file), step=1)

if ending_link > len(data_file):
    ending_link = len(data_file)

min_time = st.number_input("Minimum Time to Wait", min_value=0, value=5, step=1)
max_time = st.number_input("Maximum Time to Wait", min_value=0, value=10, step=1)

no_of_scrolls = st.number_input('Number of Times You want to scroll the page', min_value=0, value=100000, step=1)

# generating fake user-agent
ua = UserAgent()
user_agent = ua.random


# reading links.xlsx file
sound_links = data_file['links']
domain_link = "https://www.tiktok.com/"

if st.button("Start Scraping") and output_filename:
    # initializing bot instance
    options = ChromeOptions()
    options.binary_location = os.path.abspath('chromedriver.exe')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-blink-features=AutomationControlled")  # Remove the automation flag
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    driver = uc.Chrome(driver_executable_path=os.path.abspath('chromedriver.exe'), options=options, headless=False) # if you don't want to see Graphical User Interface, You can use headless=True
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.maximize_window()

    current_user_agent = driver.execute_script("return navigator.userAgent;")

    print("Fake User-Agent set by `fake_useragent`:", user_agent)
    print("User-Agent currently in use by the browser:", current_user_agent)

    # Verify if the user agent matches
    if user_agent == current_user_agent:
        print("Fake User-Agent is successfully applied!")
    else:
        print("Fake User-Agent was not applied correctly.")

    data = []
    # In[9]:
    try:
        for s in range(starting_link, ending_link):
            sound_link = sound_links[s]
            
            driver.get(sound_link)
            time.sleep(random.uniform(min_time, max_time))

            last_height = driver.execute_script("return document.body.scrollHeight")
            
            for _ in range(no_of_scrolls): # how many times should it scroll down
                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')

                try:
                    ul = soup.find('div', {"data-e2e": "music-item-list"})
                    lis = ul.find_all('div')
                    for l in range(len(lis)):
                        li = lis[l]
                        try:
                            username = li.find('p', {"data-e2e": "music-item-username"}).text
                            profile_link = f"{domain_link}@{username}"
                        except:
                            username = ''
                            profile_link = ''
                        if username:
                            temp = {"sound_link": sound_link, "profile_link": profile_link, "username": username}
                            if temp not in data:
                                data.append(temp)
                                print(temp, '\n')
                                st.json(temp)
                except Exception as e:
                    with open('logs.txt', 'w') as file:
                        file.write(str(e))
                        print(e)
                
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(random.uniform(min_time, max_time))
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                # if new_height == last_height:
                #     break
                
                last_height = new_height
    except Exception as e:
        st.write(str(e))
        df = pd.DataFrame(data)
        df.to_csv(f'{output_filename}.csv')
        driver.quit()


    df = pd.DataFrame(data)
    df.to_csv(f'{output_filename}.csv')

    driver.quit()
else:
    st.write('Fill Output Filename')
