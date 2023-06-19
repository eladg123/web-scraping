
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
from selenium.webdriver.support.ui import Select
import time


website='https://www.adamchoi.co.uk/overs/detailed'
path = 'introduce chromedriver path'
service = ChromeService(executable_path=path)
options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=options)

driver.get(website)

# locate "all matches" button
all_matches_button = driver.find_element(by='xpath',value="//label[@analytics-event='All matches']")
all_matches_button.click()

# dropdown select automatic
dropdown = Select(driver.find_element(by='id',value='country'))
dropdown.select_by_visible_text('Spain')
time.sleep(3)

matches = driver.find_elements(by='xpath',value='//tr')
date = []
home_team = []
score = []
away_team = []

for match in matches:
    date.append(match.find_element(by='xpath',value='./td[1]').text)
    home_team.append(match.find_element(by='xpath', value='./td[2]').text)
    score.append(match.find_element(by='xpath', value='./td[3]').text)
    away_team.append(match.find_element(by='xpath', value='./td[4]').text)

driver.quit()

df = pd.DataFrame({'date':date,
                   'home_team':home_team,
                   'score':score,
                   'away_team':away_team})
df.to_csv('football_data.csv',index=False)