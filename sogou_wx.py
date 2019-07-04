# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import csv
import time


# 声明一个Chrome浏览器
browser = webdriver.Chrome()
# url网址
url = 'https://weixin.sogou.com/'
# 请求该网址
browser.get(url)

# 声明一个列表存储字典
data_list = []

KeyWord = '粤港澳 大湾区'
def start_spiders():
    # 找到输入框id
    query = browser.find_element_by_id('query')
    query.send_keys(KeyWord)
    # 找到搜索按钮
    time.sleep(1)
    swz = browser.find_element_by_class_name('swz')
    swz.click()
    # 找到登陆按钮并点击
    time.sleep(1)  #如果要输入验证码，要给出充分的时间（15s）输入验证码
    top_login = browser.find_element_by_id('top_login')
    top_login.click()
    # 显示等待是否登陆成功
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'yh')
        )
    )
    print('登录成功')

    while True:
        # 找到所有的li标签
        lis = browser.find_elements_by_xpath('//ul[@class="news-list"]/li')
        # 找到下一页的按钮
        # 遍历列表
        for li in lis:
            # 题目
            title = li.find_element_by_xpath('.//h3').text
            # 作者
            author = li.find_element_by_class_name('account').text
            # 时间
            datetime = li.find_element_by_class_name('s2').text
            # 文章摘要，这个项目没要求
            #content = li.find_element_by_class_name('txt-info').text
            # 文章链接
            href = li.find_element_by_xpath('.//h3/a').get_attribute('data-share')

            # 声明一个字典存储数据
            data_dict = {}
            data_dict['title'] = title
            data_dict['author'] = author
            data_dict['datetime'] = datetime
            #data_dict['content'] = content
            data_dict['href'] = href
            
            print(data_dict)

            data_list.append(data_dict)

        # 如果找不到下一页按钮就抛出异常并退出循环
        try:
            sogou_next = browser.find_element_by_id('sogou_next')
            # 如果下一页按钮存在就继续
            time.sleep(3)
            sogou_next.click()
        except Exception as e:
            break


def main():

    start_spiders()


if __name__ == '__main__':

    main()
    # 退出浏览器
    browser.quit()
    print(data_list)
    # 将数据存储到json文件中
    with open('data_json.json', 'a+', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    print('json文件写入完成')
    # 将数据存入csv文件中
    # 表头
    csv_title = data_list[0].keys()
    with open('data_csv.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(csv_title)
        # 批量写入表头
        for row in data_list:
            writer.writerow(row.values())
    print('csv文件写入完成')
