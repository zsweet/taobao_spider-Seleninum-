import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#节点交互
def get_baidu():
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.baidu.com')
        input = browser.find_element_by_id('kw')
        # input = browser.find_element(By.ID,'kw')  与上面相同
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    except BaseException as  e:
        print ( 'baidu function error:{1}'.format(e) )
    finally:
        browser.close()
    #     print('end')


#节点交互
def get_taobao():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.taobao.com')
        input = browser.find_element_by_id('q')
        input.send_keys('iPhone')
        time.sleep(1)
        input.clear()
        input.send_keys('iPad')
        button = browser.find_element_by_class_name('btn-search')
        button.click()
    except BaseException as  e:
        print ( 'taobao function error:{1}'.format(e) )
        #print('taobao function error:%s'% e)
    finally:
        browser.close()

#动作链
def node_chain():
    try:
        browser = webdriver.Chrome()
        url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
        browser.get(url)
        browser.switch_to.frame('iframeResult')
        source = browser.find_element_by_css_selector('#draggable')
        target = browser.find_element_by_css_selector('#droppable')
        actions = ActionChains(browser)
        actions.drag_and_drop(source, target)
        actions.perform()
    except BaseException as  e:
        print ( 'node_chain function error:{1}'.format(e) )
    finally:
        browser.close()

#execute Javascipt
def javascript():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.zhihu.com/explore')
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        browser.execute_script('alert("To Bottom")')
    except BaseException as  e:
        print ( 'javascript function error:{1}'.format(e) )
def get_attribution():
    try:
        browser = webdriver.Chrome()
        url = 'https://www.zhihu.com/explore'
        browser.get(url)
        logo = browser.find_element_by_id('zh-top-link-logo')
        print(logo)
        print(logo.get_attribute('class'))
    except BaseException as  e:
        print('javascript function error:{1}'.format(e))

#切换frame   iframe，也就是子Frame，相当于页面的子页面，它的结构和外部网页的结构是完全一致的
def change_frame():
    browser = webdriver.Chrome()
    url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    browser.get(url)
    browser.switch_to.frame('iframeResult')
    try:
        logo = browser.find_element_by_class_name('logo')
    except NoSuchElementException:
        print('NO LOGO')
    browser.switch_to.parent_frame()
    logo = browser.find_element_by_class_name('logo')
    #print( browser.find_element_by_xpath('//*[@name="logo"]'))
    print(logo)
    print(logo.text)

#选项卡设置
def choose_card():
    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com')
    browser.execute_script('window.open()')
    print(browser.window_handles)
    browser.switch_to_window(browser.window_handles[1])
    browser.get('https://www.taobao.com')
    time.sleep(1)
    browser.switch_to_window(browser.window_handles[0])
    browser.get('https://python.org')

if __name__ == '__main__':
    #get_taobao()
    #get_taobao()
    #node_chain()
    #javascript()
    #get_attribution()
    choose_card()
