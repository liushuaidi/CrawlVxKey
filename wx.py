# -*- coding: utf-8 -*-
import requests
from lxml import etree
from pyquery import PyQuery as pq
import json
import csv


data_list = []

f = open('./粤港澳 大湾区.json','r',encoding='utf-8').read()
data = json.loads(f)

for i in range(1000):
    url = data[i]['href']
    # url = "http://weixin.sogou.com/api/share?timestamp=1559181706&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAOmhpM1o93vuqrpDO8FtinhMoI8CkF6FTsCDtE0u5QLzZJBBRf8CqZYts3tTsFXhRs1K7H1m04e1FcBMU6YAkxNQI8K2NHvb0tfgHCVrLJXO7Ypwg3asqokRbUMd5xYPXJHJX-ephoKQdAHziZEb2PVwCg1sPYaGvOPNIT70wF0ec="
    response = requests.get(url)
    # print(response.status_code)
    #原本用的xpath，正文内容无法提取，遂转换思路，用pyquery
    html = response.text
    doc = pq(html)
    title = doc('.rich_media_title').text()
    # print(title)
    nickname = doc('#js_profile_qrcode > div > strong').text()
    # print(nickname)
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    # print(wechat)
    content = doc('.rich_media_content').text()
    # print(content)

    # 声明一个字典存储数据
    data_dict = {}
    data_dict['title'] = title
    data_dict['nickname'] = nickname
    data_dict['wechat'] = wechat
    data_dict['content'] = content
    data_list.append(data_dict)


    # 将数据存入csv文件中
    # 表头
    csv_title = data_list[0].keys()
    with open('粤港澳 跨境2.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(csv_title)
        # 批量写入表头
        for row in data_list:
            writer.writerow(row.values())
    print('csv文件写入完成',i)














# 原本打算用xpath
# data = response.content.decode()
# html = etree.HTML(data)
# print(type(html))  #element类型
# #文章标题
# title = html.xpath("//h2[@class='rich_media_title']")[0].xpath('string(.)').strip()
# print(title)
# #公众号名称
# nickname = html.xpath("//div[@id='meta_content']/span/a")[0].xpath('string(.)').strip()
# print(nickname)
# #微信号
# wechat_num = html.xpath("//p[@class='profile_meta']/span")[0].xpath('string(.)').strip()
# print(wechat_num)
# #功能介绍
# introduction = html.xpath("//p[@class='profile_meta']/span")[1].xpath('string(.)').strip()
# print(introduction)
# #正文-----暂时不会提取内容   好尴尬~~   前面几个都OK
# content = html.xpath("//div[@class='rich_media_content/text()']").xpath('string(.)').strip()