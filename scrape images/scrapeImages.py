import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import io
from PIL import Image
import time

wd = webdriver.Chrome()

# define function that scrape more than one photos
def get_images_from_Google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    url = "https://www.google.com/search?q=cats&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
    wd.get(url)
    image_urls = set()
    skips = 0

    while len(image_urls) +skips < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for image in thumbnails[len(image_urls)+skips: max_images]:
            try:
                image.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")

            for img in images:
                if img.get_attribute('src') in image_urls:
                    max_images +=1
                    skips+=1
                    break
                if img.get_attribute('src') and 'http'  in image.get_attribute('src'):
                    image_urls.add(img.get_attribute('src'))
    return image_urls




# define function that can download image
def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
    except Exception as e:
        print('Failed - ', e)


urls = get_images_from_Google(wd, 1, 5)

for i , url in enumerate(urls):
    download_image('imgs/', url , str(i)+".jpg")
print(urls)
wd.quit()