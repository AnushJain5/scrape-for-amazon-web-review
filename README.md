# scrape-for-amazon-web-review
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pymongo import MongoClient
import threading
from datetime import datetime
import time

client = MongoClient('localhost') 
db = client["Dragon"]
collection = db['data']

# sku = input("Enter the sku")

title_list = []
def get_url_all(sku):
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

    val = f"https://www.amazon.in/dp/{sku}"
    driver.get(val)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "a-size-large")))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,features="html.parser")
    #title
    title1 = soup.find("span",attrs={"class":"a-size-large product-title-word-break"})
    title = title1.string.strip()
    print(title)

    #price
    price1 = soup.find("span",attrs={"class":"a-price aok-align-center reinventPricePriceToPayMargin priceToPay"})
    price2 = price1.find("span",attrs={"class":"a-price-whole"})
    price = price2.text.strip()
    price = float(price.replace(",",""))
    print(price)

    #sku
    print(sku)

    #images
    images = []

    image_tags = soup.find_all("li", attrs={"class": "a-spacing-small item imageThumbnail a-declarative"})
    for image_tag in image_tags:

        image_url = image_tag.find("img")
        image_url2 = image_url.get("src")
        images.append(image_url2)

    print(images)

    #brands
    brand = title.split()[0]
    print(brand)

    #stock in/out
    avail = soup.find("div",attrs={"id":"availability"})
    # stock3 = soup.find("span",attrs={"class":"a-size-medium a-color-success"or{"class":"a-size-base a-color-price a-text-bold"}})
    stock3 = avail.find("span",attrs={"class":"a-size-base a-color-price a-text-bold"})
    stock4 = avail.find("span",attrs={"class":"a-size-medium a-color-success"})
    stock = "out"
    if stock3:
        stock = stock3.text.strip()
    elif stock4:
        stock = stock4.text.strip()
    # print(stock3.text.strip())
    print(stock)

    #updateDetail

    update_detail = 1
    print(update_detail)

    #updated_time
    now = datetime.now()
    print(now)
    updated_time = time.mktime(now.timetuple())
    print(updated_time)

    # db.data.insert_one({'Product_Title':title,'Product_price':price,'Product_image_url':images,'Product_sku':sku,'Product_stock':stock,'Product_brand':brand,'Update_detail':update_detail,'Update_dat':updated_time})



x = collection.find()
db_list = list(x)

n = len(db_list)

# for i in range(0,6):
#     for x,y in db_list[i].items():
#         print(x,y)

for i in range(0,10,5):
    a = db_list[i+0]["Product_sku"]
    b = db_list[i+1]["Product_sku"]
    c = db_list[i+2]["Product_sku"]
    d = db_list[i+3]["Product_sku"]
    e = db_list[i+4]["Product_sku"]
    

    t1 = threading.Thread(target=get_url_all, args=(a,))
    t2 = threading.Thread(target=get_url_all, args=(b,))
    t3 = threading.Thread(target=get_url_all, args=(c,))
    t4 = threading.Thread(target=get_url_all, args=(d,))
    t5 = threading.Thread(target=get_url_all, args=(e,))
    

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    # threads = []
    # for j in range(0,5):
    #     thread = threading.Thread(target=get_url_all, args=(db_list[i+0]["Product_sku"],))
    #     threads.append(thread)
    
    # for thread in threads:
    #     thread.start()

    # for thread in threads:
    #     thread.join()
    



# print("Done")
