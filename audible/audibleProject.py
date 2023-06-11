from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
# imports for explicity wait:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=08b836ae-73e5-4c8c-9a3d-71c5be252964&pf_rd_r=0JNSCQX47DAAF07A4ZNW&pageLoadId=CihEyrCtf4M1F3Kb&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"
path = 'introduce chromedriver path'
service = ChromeService(executable_path=path)
driver = webdriver.Chrome(options=options)

driver.get(web)
driver.maximize_window()

#pagination
pagination = driver.find_element(by='xpath',value='.//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(by='xpath',value='.//li')
last_page = int(pages[-2].text)       # one position before the right arrow is tha last page li tag
current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    # time.sleep(2)
    container = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container')))
    # container = driver.find_element(by='xpath', value='.//div[contains(@class, "adbl-impression-container")]')
    products = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'productListItem')))
    # products = container.find_elements(by='xpath', value='.//li[contains(@class,"productListItem")]')

    for product in products:
        book_title.append(product.find_element(by='xpath',value='.//h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(by='xpath',value='.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(by='xpath',value='.//li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page+1
    try:
        next_button = driver.find_element(by='xpath', value='//span[contains(@class, "nextButton")]')
        next_button.click()
    except:
        pass

driver.quit()

df = pd.DataFrame({'title':book_title,
                   'author':book_author,
                   'runtime':book_length})
df.to_csv('books_headless.csv', index=False)



# implicit wait - המתנה קבועה
# time.sleep(2) המתנה של שתי שניות

# explicit wait - המתנה מותנית, רק אם צריך מחכים
# webDriverWait(driver,10).until(EC.presence_of_element_located((By.XPath,"value")))
# the first parameter is the driver
# the second parameter how much maximum seconds you want to wait
# the third parameter is the condition we want to wait to, for what we are wating