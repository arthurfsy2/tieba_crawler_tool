# reference link: 
# https://blog.csdn.net/qq_38887171/article/details/109197736
# https://docs.python.org/3/library/re.html
# https://www.w3schools.com/python/python_user_input.asp
# https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
# https://docs.python.org/3/tutorial/classes.html
# https://stackoverflow.com/questions/2792650/import-error-no-module-name-urllib2
import urllib
import requests
from collections import OrderedDict
from urllib.request import urlopen
import re
import os
from urllib.parse import urljoin
import sys
import time
import json

def download_and_replace_pic_url(content):
    global save_dir, pic_base_url
    image_urls = re.findall(r'!\[\]\((.*?)\)', content)
    
    for url in image_urls:
        image_name = url.split('/')[-1].split('?')[0]  # 去掉查询参数
        save_path = os.path.join(save_dir, image_name)
        
        # 检查文件是否已存在
        if os.path.exists(save_path):
            print(f'跳过已下载图片: {save_path}')
            continue  # 跳过下载
        
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as image_file:
                image_file.write(response.content)
                print(f'已下载图片: {save_path}')

    # 替换原来的内容
    for url in image_urls:
        image_name = url.split('/')[-1].split('?')[0]
        if pic_base_url:
            new_image_url = urljoin(pic_base_url, image_name)
        else:
            new_image_url = f"../PicDownload/{image_name}"
        content = content.replace(url, new_image_url)
    
    return content  # 返回替换后的内容

# deal with html tags
class Tool:
    # remove <img>
    #removeImg = re.compile('<img.*?>| {7}|')
    replaceImg = re.compile('<img.*?src="(.*?)".*?>')
    # remove hyperlink tag
    #removeAddr = re.compile('<a.*?>|</a>')
    replaceAddr = re.compile('<a href=".*?>(.*?)</a>')
    # replace new line with \n
    #replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # replace table with \t
    #replaceTD = re.compile('<td>')
    # replace paragraph heading with \n
    #replacePara = re.compile('<p.*?>')
    # replace new line with \n
    replaceBR = re.compile('<br><br>|<br>')
    # remove tags
    #removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        #x = re.sub(self.removeImg, "", x)
        #x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceAddr, r'[\1](\1)', x)
        #x = re.sub(self.replaceLine, "\n", x)
       # x = re.sub(self.replaceTD, "\t", x)
        #x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceImg, r'![](\1)', x)
        x = re.sub(self.replaceBR, "\n", x)
       # x = re.sub(self.removeExtraTag, "", x)
        # strip() remove other contents
        return x.strip()

# fetch url format
# http://tieba.baidu.com/p/thread_id?see_lz=1&pn=1
# http:// - http protocol
# tieba.baidu.com - website address
# p/thread_id - thread id
# lz=1&pn=1 - only post holder & page number
class Baidu_Tieba:

    # initialize and pass address and requirement parameters
    def __init__(self, thread_url, only_lz, floor_tag, i):
        self.thread_url = thread_url
        self.only_lz = '?see_lz=' + str(only_lz)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floor_tag = floor_tag


    # pass in the page number and fetch the page content
    def get_page(self, page_number):
        try:
            # 代理设置
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890',
            }
            headers = {
                "cookie":Cookie
            }

            url = self.thread_url + self.only_lz + '&pn=' + str(page_number)
            response = requests.get(url, headers=headers, proxies=proxies)
            return response.text
        
        except requests.exceptions.RequestException as e:
            
            if hasattr(e, "reason"):
                print("failed to build connection with tieba: ", e.reason)
            return None

    # get thread title
    def get_title(self):
        url  = self.thread_url.split("/p/")[1]
        def get_content_by_pattern(key_content, page):
            pattern = re.compile(key_content, re.S)
            result = re.search(pattern, page)
            content = result.group(1).strip() if result else None
            return content
        
        page = self.get_page(1)

        raw_title_key_pattern1 = '<h1 class="core_title_txt.*?>(.*?)</h1>'
        raw_title_key_pattern2 = '<h3 class="core_title_txt.*?>(.*?)</h3>'

        raw_title = get_content_by_pattern(raw_title_key_pattern1, page) 
        raw_title_final = raw_title if raw_title else get_content_by_pattern(raw_title_key_pattern2, page) 
        if not  raw_title_final:
            print("无法获取贴子标题，可能原因：\n1. 操作过快导致IP被封，请更换IP后再次尝试\n2. 请检查该贴能否通过浏览器正常访问")
            sys.exit()

        create_date_pattern1 = '<span class="tail-info">1楼</span><span class="tail-info">(.*?)</span>'
        create_date_pattern2 = '&quot;date&quot;:&quot;(.*?)&quot;,&quot'
        create_date = get_content_by_pattern(create_date_pattern1, page)
        create_date_final = create_date if create_date else get_content_by_pattern(create_date_pattern2, page) 
        tieba_name_pattern =  'fname="(.*?)">' 
        tieba_name = get_content_by_pattern(tieba_name_pattern, page)
        
        reply_num_pattern = '<li class="l_reply_num" style="margin-left:.*?" ><span class=".*?" style="margin-right:.*?">(.*?)</span>'
        reply_num = get_content_by_pattern(reply_num_pattern, page)
        final_title = f"{create_date_final}_{url}_{tieba_name}_回复({reply_num})_{raw_title_final}"  
        
        return raw_title_final, final_title
        
    # get total page number
    def get_total_page_num(self):
        page = self.get_page(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # get the content of each level
    def get_content(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "> " + self.tool.replace(item) + "\n"
            content = download_and_replace_pic_url(content)
            contents.append(content.encode('utf-8'))
        return contents



    def set_file_title(self, raw_title, final_title):
        download_path ="./Download/"
        # download_path =r"D:\web\blog\src\Arthur\Tieba\我的贴子"
        if raw_title is not None:
            print("raw_title: ",raw_title)
            print("final_title: ",final_title)
            # 将不符合文件名命名规则的符号替换为空格
            final_title = re.sub(r'[<>:"/\\|?*]', ' ', final_title)
            self.file = open(download_path + final_title + ".md", "w+",encoding="utf-8")
            self.file.write(f"## ["+raw_title+"](" + base_url + ")\n\n")
        else:
            self.file = open(base_url.split("/p/")[1] + ".md", "w+",encoding="utf-8")
    
    def write_data(self, contents):
        # write content each floor to file
        for item in contents:
            if self.floor_tag == '1':
                # Will add floor tag
                # split mark between each floor
                
                floor_line = "---\n> " + str(self.floor) + u"楼\n"
                self.file.write(floor_line)
            self.file.write(item.decode("utf-8")) # convert byte to string
            self.floor += 1

    def start(self):
        page_num = self.get_total_page_num()
        raw_title, final_title = self.get_title()
        self.set_file_title(raw_title, final_title)
        if page_num is None:
            print("Invalid URL")
            return
        try:
            print("该帖子共有" + str(page_num) + "页")
            for i in range(1, int(page_num) + 1):
                print("正在写入第" + str(i) + "页数据")
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
        # 出现写入异常
        except IOError as e:
            print("exception" + e.message)
        finally:
            print("done")



if __name__ == "__main__":
    with open("scripts/config.json", "r",encoding="utf-8") as file:
        data = json.load(file)

    save_dir = data["save_dir"]
    pic_base_url = data["pic_base_url"]
    merge_output_file = data["merge_output_file"]
    list_output_file = data["list_output_file"]
    merge_template_path = data["merge_template_path"]
    list_template_path = data["list_template_path"]
    Cookie = data["Cookie"]
    base_url_path = data["base_url_path"]

    print("*** 百度贴吧帖子读取工具 ***")
    #base_url = input('输入帖子地址: \n')
    #only_lz = input('只看楼主发言，是 - 1， 否 - 0：\n')
    only_lz = '0'
    #floor_tag = input('只用楼层分割符号, 是 - 1， 否 - 0: \n')
    floor_tag = '1'
    base_urls = []

    with open(base_url_path, "r") as file:
        for line in file:
            url = line.strip()  # 去除行首行尾的空白字符
            base_urls.append(url)

    base_urls.sort(key=lambda x: int(x.split('/p/')[1]), reverse=True)
    
    # 去重并保持顺序
    unique_urls = list(OrderedDict.fromkeys(base_urls))

    # 写回文件
    with open(base_url_path, "w") as file:
        for url in unique_urls:
            file.write(url + "\n")  # 每个 URL 一行

    for i, base_url in enumerate(unique_urls,start=1):
        
        if "# " not in base_url:
            print(base_url)
            tieba = Baidu_Tieba(base_url, only_lz, floor_tag, i) # url, only_lz, floor tag
            tieba.start()
            time.sleep(1)  # 在每次循环后等待N秒，防止封IP



