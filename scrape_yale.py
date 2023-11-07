from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
#Create Dataframe
data_frame = pd.DataFrame(columns=['Restaurant' ,'Review','Rating','Date'])

# Path for driver
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = Chrome(PATH)
# Access the webpage
driver.get('https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&sortby=review_count')
time.sleep(10)
index = 0
# Acccess only two pages of webpage
for j in range(2):
    #Select all restaurants present in webpage
    restaurants = driver.find_elements(By.XPATH , '//div[@class=" css-ady4rt"]')
    for restaurant in restaurants:

        new_tab = restaurant.find_element(By.TAG_NAME , 'a')
        new_tab.click()
        time.sleep(5)
        #information in new tab -> switch to new tab
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source , 'lxml')
        # Get Restaurant Name
        element = soup.find('h1')
        counter = 0
        next_review = True
        # Scrape at most thousand reviews
        while counter < 1000 and next_review: 
            
            try:
                for i in range(1,11):
                    # Get review
                    reviews = driver.find_element(By.XPATH ,f'//*[@id="reviews"]/section/div[2]/ul/li[{i}]/div')
                    rev= reviews.find_element(By.TAG_NAME , 'p').text
                    # Get rating
                    rating =  driver.find_element(By.XPATH ,f'//*[@id="reviews"]/section/div[2]/ul/li[{i}]/div/div[2]/div/div[1]/span/div')
                    rating_value = rating.get_attribute("aria-label") 
                    # Get date
                    date = driver.find_element(By.XPATH ,f'//*[@id="reviews"]/section/div[2]/ul/li[{i}]/div/div[2]/div/div[2]').text
                    counter += 1
                    # Save scraped data into dataframe in ordered manner
                    data_frame.loc[len(data_frame)] = [element.text,rev , rating_value , date]
                    index +=1
                # Go to next reviews : only 10 reviews available at a time
                next_review = driver.find_element(By.XPATH , '//*[@id="reviews"]/section/div[2]/div[5]/div[1]/div/div[11]')
                next_review.click()
                time.sleep(3)
            except:
                break
            

        


            
                
                
        driver.close()
        # Switch to main page
        driver.switch_to.window(driver.window_handles[0])
    

    next_page = driver.find_element(By.XPATH , '//*[@id="main-content"]/div/ul/li[21]/div/div[1]/div/div[11]/span/a')
    # Go to next page
    if next_page:
        next_page.click()
        time.sleep(4)

# Save data as csv
data_frame.to_csv('review.csv')