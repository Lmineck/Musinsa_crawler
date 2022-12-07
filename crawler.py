import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# 크롤링 할 경로
def PageUrl(itemName, pageNum):
    url = 'https://www.musinsa.com/search/musinsa/goods?q='+itemName+'&list_kind=small&sortCode=pop&sub_sort=&page='+str(pageNum)+'&display_cnt=0&saleGoods=false&includeSoldOut=false&setupGoods=false&popular=false&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&campaignId=&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&shoeSizeOption=&groupSale=false&d_cat_cd=&attribute='
    return url

# 크롤링 할 데이터 수집
_itemName = input("검색할 의류명을 입력하세요: ")
pageUrl = PageUrl(_itemName, 1)

# 크롤링
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(pageUrl)

totalPageNum = driver.find_element(By.CSS_SELECTOR, ".totalPagingNum").text
print("Total page of watch : ", str(totalPageNum))
print()

result = []
cnt = 1
start = time.time()
for i in range(int(totalPageNum)):
    pageUrl = PageUrl(_itemName, i)
    driver.get(pageUrl)
    time.sleep(1)
    item_infos = driver.find_elements(By.CSS_SELECTOR, ".img-block")
    item_images = driver.find_elements(By.CSS_SELECTOR, ".lazyload.lazy")

    print(_itemName, " : ", len(item_infos), "items exist, ", i + 1, "/", totalPageNum, " page")

    for j in range(len(item_infos)):
        try:
            title = item_infos[j].get_attribute("title")
            brand = item_infos[j].get_attribute("data-bh-content-meta4")
            price = item_infos[j].get_attribute("data-bh-content-meta3")
            url = item_infos[j].get_attribute("href")
            img_url = item_images[j].get_attribute("data-original")
            shop = "musinsa"

            result.append([title, brand, price, url, img_url])

        except Exception as e:
            print(e)
            pass

end = time.time()
print('crawling time : ', f'{end-start:.1f} sec')

# pandas 데이터 변환
data = pd.DataFrame(result)
data.columns = ['title', 'brand', 'price', 'url', 'img_url']
data.to_csv(_itemName+'(musinsa).csv', encoding='cp949', index=False)

#exit
driver.close()