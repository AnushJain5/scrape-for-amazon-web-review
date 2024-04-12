from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

item_title = []
item_price = []
item_image_url = []
item_sku = []
keyword = input("Enter keyword: ")

client = MongoClient('loalhost') 
db = client["Dragon"]
collection = db['data']

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# url = f"https://www.amazon.in/s?k={keyword}"
# driver.get(url)

def title_all(box_main, title):
    title_h1 = box_main.find("div", attrs={"class": "puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right"})
    title_h2 = title_h1.find("div", attrs={"class": "a-section a-spacing-none puis-padding-right-small s-title-instructions-style"})
    title_h3 = title_h2.find("h2", attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
    title_h4 = title_h3.find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"})
    item_title.append(title_h4.string.strip())

def price_all(box_main, price):
    price_h1 = box_main.find("div", attrs={"class": "a-section a-spacing-none a-spacing-top-micro puis-price-instructions-style"})
    price_h2 = price_h1.find("div", attrs={"class": "a-row a-size-base a-color-base"})
    price_h3 = price_h2.find("div", attrs={"class": "a-row"})
    price_h4 = price_h3.find("span", attrs={"class": "a-offscreen"})
    str1 = price_h4.string.strip()
    str2 = str1[1:]
    spe_cha = ['$', ',']
    str3 = str2
    for i in spe_cha:
        str3 = str3.replace(i, "")
    item_price.append(float(str3))

def image_url_all(box_main, image_url):
    image_h1 = box_main.find("div", attrs={"class": "puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24 puis-list-col-left"})
    image_h2 = image_h1.find("img", attrs={"class": "s-image"})
    image_h3 = image_h2.get('src')
    item_image_url.append(image_h3)

def sku_all(box_main, sku):
    str1 = box_main.get('data-csa-c-item-id')
    str2 = str1[13:]
    item_sku.append(str2)


def extract_data(k, j):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    print("extract")
   
    for i in range(k, j):
        box_main_title = soup.find("div", attrs={"data-csa-c-pos": i})
        title_all(box_main_title, item_title)

    for i in range(k, j):
        box_main_price = soup.find("div", attrs={"data-csa-c-pos": i})
        price_all(box_main_price, item_price)

    for i in range(k, j):
        box_main_image = soup.find("div", attrs={"data-csa-c-pos": i})
        image_url_all(box_main_image, item_image_url)

    for i in range(k, j):
        box_main_sku = soup.find("div", attrs={"data-csa-c-pos": i})
        sku_all(box_main_sku, item_sku)

    print("Scraping data from page")


def next_page(start_pos, end_pos,page_num):
    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-button.s-pagination-next')))
        next_button.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
        page_num += 1
        driver.get(f"https://www.amazon.in/s?k={keyword}&page={page_num}")
        start_pos += 16 
        end_pos += 16   
        print(start_pos)
        print(end_pos) 
        extract_data(start_pos, end_pos)
        return start_pos, end_pos,page_num
    except Exception as e:
        print("No more pages to navigate")
        return start_pos, end_pos

# Extract data from the first page
driver.get(f"https://www.amazon.in/s?k={keyword}")
extract_data(1, 22)


start_position, end_position = 1, 22
page_num = 1
for _ in range(2): 
    start_position, end_position,page_num = next_page(start_position,end_position,page_num)

# for i in range(1,62):
#     print(item_sku[i])
# print(item_title)
# print(item_price)
# print(item_image_url)
print(item_sku)

for i in range(1,63):
    print(item_sku[i])

# for i in range(1,63):
#     db.data.insert_one({'Product_Title':item_title[i],'Product_price':item_price[i],'Product_image_url':item_image_url[i],'Product_sku':item_sku[i]})

driver.quit()
