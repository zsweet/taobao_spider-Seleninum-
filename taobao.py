import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

#browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KEYWORD = 'iPad'


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located(\
                        (By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable(\
                        (By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        #它会等待要加载的页数出现在下面界面里面即返回成功 这里是淘宝下面的页码高光那部分
        wait.until(EC.text_to_be_present_in_element(\
                        (By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))   )

        #判断商品信息框是否加载完毕
        wait.until(EC.presence_of_element_located(\
                        (By.CSS_SELECTOR, '.m-itemlist .items .item')))

        #开始获取商品信息
        get_products()
    except TimeoutException:
        index_page(page)




def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = PyQuery(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'image': item.find('.pic .img').attr('data-src'),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text()
            }
        print(product)
        #save_to_mongo(product)


MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if collection.insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

MAX_PAGE = 100
def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        print('正在获取：{0}'.format(i))
        index_page(i)

if __name__ == '__main__':
    print('=>>>>>>>>>>>>>>>>>>>>>....')
    main()
