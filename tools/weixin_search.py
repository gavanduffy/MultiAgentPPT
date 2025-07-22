#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/6/25 09:09
# @File  : weixin_search.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : Uses search to find WeChat official account articles, first searches Sogou with keywords to get links, then uses get_real_url to get the real link, and finally uses the real link to get the official account content.
import json
import asyncio
from typing import Any, Dict, List, Optional
import requests
from lxml import html
from urllib.parse import quote
import time

def sogou_weixin_search(query: str) -> List[Dict[str, str]]:
    """Search for specified keywords in Sogou WeChat search and return a list of results"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': f'https://weixin.sogou.com/weixin?query={quote(query)}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }

    params = {
        'type': '2',
        's_from': 'input',
        'query': query,
        'ie': 'utf8',
        '_sug_': 'n',
        '_sug_type_': '',
    }

    try:
        response = requests.get('https://weixin.sogou.com/weixin', params=params, headers=headers)

        if response.status_code == 200:
            tree = html.fromstring(response.text)
            results = []

            elements = tree.xpath("//a[contains(@id, 'sogou_vr_11002601_title_')]")
            publish_time = tree.xpath(
                "//li[contains(@id, 'sogou_vr_11002601_box_')]/div[@class='txt-box']/div[@class='s-p']/span[@class='s2']")

            for element, time_elem in zip(elements, publish_time):
                title = element.text_content().strip()
                link = element.get('href')
                if link and not link.startswith('http'):
                    link = 'https://weixin.sogou.com' + link
                results.append({
                    'title': title,
                    'link': link,
                    'publish_time': time_elem.text_content().strip()
                })

            return results
        else:
            return []
    except Exception as e:
        return []


def get_real_url(sogou_url: str) -> str:
    """Get the real WeChat official account article link from a Sogou WeChat link"""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'Cookie': 'ABTEST=7|1750756616|v1; SUID=0A5BF4788E52A20B00000000685A6D08; IPLOC=CN1100; SUID=605BF4783954A20B00000000685A6D08; SUV=006817F578F45BFE685A6D0B913DA642; SNUID=B3E34CC0B8BF80F5737E3561B9B78454; ariaDefaultTheme=undefined',
    }

    try:
        response = requests.get(sogou_url, headers=headers)

        script_content = response.text
        start_index = script_content.find("url += '") + len("url += '")
        url_parts = []
        while True:
            part_start = script_content.find("url += '", start_index)
            if part_start == -1:
                break
            part_end = script_content.find("'", part_start + len("url += '"))
            part = script_content[part_start + len("url += '"):part_end]
            url_parts.append(part)
            start_index = part_end + 1

        full_url = ''.join(url_parts).replace("@", "")
        return "https://mp." + full_url
    except Exception as e:
        return ""


def get_article_content(real_url: str, referer: str) -> str:
    """Get the main content of a WeChat official account article"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': referer,
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    }

    try:
        response = requests.get(real_url, headers=headers)
        tree = html.fromstring(response.text)
        content_elements = tree.xpath("//div[@id='js_content']//text()")
        cleaned_content = [text.strip() for text in content_elements if text.strip()]
        main_content = '\n'.join(cleaned_content)
        return main_content
    except Exception as e:
        return f"Failed to get article content: {str(e)}"

def get_wechat_article(query: str, number=10):
    """
    Get the top 10 articles
    """
    start_time = time.time()
    results = sogou_weixin_search(query)
    if not results:
        return f"No articles related to {query} found."
    articles = []
    results = results[:number]
    for every_result in results:
        sogou_link = every_result["link"]
        real_url = get_real_url(sogou_link)
        # referer: request source
        content = get_article_content(real_url, referer=sogou_link)
        article = {
            "title": every_result["title"],
            "publish_time": every_result["publish_time"],
            "real_url": real_url,
            "content": content
        }
        articles.append(article)
    end_time = time.time()
    print(f"Articles related to keyword '{query}' have been retrieved. {len(articles)} articles found, taking {end_time - start_time:.2f} seconds.")
    return articles

if __name__ == '__main__':
    get_wechat_article(query="吉利汽车",number=2)
