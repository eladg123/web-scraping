from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


web = 'https://twitter.com/'


options = Options()
path = 'introduce chromedriver path'
service = ChromeService(executable_path=path)
driver = webdriver.Chrome(options=options)

driver.get(web)
driver.maximize_window()

login_button = driver.find_element(by='xpath', value="//a[@href='/login']")
login_button.click()

time.sleep(2)

# locating username input and write our username
username_input = driver.find_element(by='xpath', value='//input[@autocomplete="username"]')
username_input.send_keys("my username")

#locating next button
next_button = driver.find_element(by='xpath', value="//div[@role='button']//span[text()='הבא']")
next_button.click()

# wait of 2 seconds after clicking next button
time.sleep(2)

# locating the password input and write our password
password_input = driver.find_element(by='xpath',value="//input[@autocomplete='current-password']")
password_input.send_keys("my password")

# locating the login button
login_button2 = driver.find_element(by='xpath',value='//div[@role="button"]//span[text()="כניסה"]')
login_button2.click()




user_data=[]
text_data=[]
tweet_ids = set()
scrolling = True
def get_tweet(element):
    try:
        user = element.find_element(by='xpath', value='.//span[contains(text(),"@")]').text
        text = element.find_element(by='xpath', value=".//div[@lang]").text
        tweet_data = [user, text]
    except:
        tweet_data['user','text']
    return tweet_data

# Infinite scrolling
while scrolling:
    # locate the tweets with explicity wait
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(By.XPATH, '//article[@role="article"]'))
    for tweet in tweets[-15:]:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append((tweet_list[0]))
            text_data.append(" ".join(tweet_list[1].split()))
    # first, we get the initial scroll height
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        #scroll down to buttom
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #wait to load page
        time.sleep(3)
        #Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height: # if the new and the last height are equal, it means that ther is not any new content to load, so we stop scrolling
            scrolling = False
            break
        else:
            last_height = new_height



driver.quit()
df_tweets = pd.DataFrame({'user':user_data,'text':text_data})
df_tweets.to_csv('tweets.csv',index=False)
print(df_tweets)