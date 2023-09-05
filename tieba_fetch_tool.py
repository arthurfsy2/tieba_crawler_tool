# reference link: 
# https://blog.csdn.net/qq_38887171/article/details/109197736
# https://docs.python.org/3/library/re.html
# https://www.w3schools.com/python/python_user_input.asp
# https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
# https://docs.python.org/3/tutorial/classes.html
# https://stackoverflow.com/questions/2792650/import-error-no-module-name-urllib2
import urllib
import requests
import argparse
from urllib.request import urlopen
import re


# deal with html tags
class Tool:
    # remove <img>
    #removeImg = re.compile('<img.*?>| {7}|')
    replaceImg = re.compile('<img.*?src="(.*?)".*?>')
    # remove hyperlink tag
    #removeAddr = re.compile('<a.*?>|</a>')
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
    def __init__(self, thread_url, only_lz, floor_tag):
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
            url = self.thread_url + self.only_lz + '&pn=' + str(page_number)
            response = requests.get(url)
            return response.text
        
        except requests.exceptions.RequestException as e:
            
            if hasattr(e, "reason"):
                print("failed to build connection with tieba: ", e.reason)
            return None

    # get thread title
    def get_title(self):
        page = self.get_page(1)
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
            result = re.search(pattern, page)
            if result:
                return result.group(1).strip()
            else:
                print("Doesn't get the thread title")
                return None
        
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
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents



    def set_file_title(self, title):
        download_path ="./Download/"
        if title is not None:
            print(title)
            # 将不符合文件名命名规则的符号替换为空格
            title = re.sub(r'[<>:"/\\|?*]', ' ', title)
            self.file = open(download_path+title + ".md", "w+",encoding="utf-8")
            self.file.write("["+title+"](" + base_url + ")\n\n")
        else:
            self.file = open(self.defaultTitle + ".md", "w+",encoding="utf-8")
    
    def write_data(self, contents):
        # write content each floor to file
        for item in contents:
            if self.floor_tag == '1':
                # Will add floor tag
                # split mark between each floor
                
                floor_line = "\n>" + str(self.floor) + u"楼-----------------------------------------------------------------------------------------\n"
                self.file.write(floor_line)
            self.file.write(item.decode("utf-8")) # convert byte to string
            self.floor += 1

    def start(self):
        page_num = self.get_total_page_num()
        title = self.get_title()
        self.set_file_title(title)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="输入帖子地址")
    
    options = parser.parse_args()
    
base_url = options.base_url

# create instance for class Baidu_Tieba
# return the html content of specified page
print("*** 百度贴吧帖子读取工具 ***")
#base_url = input('输入帖子地址: \n')
#only_lz = input('只看楼主发言，是 - 1， 否 - 0：\n')
only_lz = '0'
#floor_tag = input('只用楼层分割符号, 是 - 1， 否 - 0: \n')
floor_tag = '1'
tieba = Baidu_Tieba(base_url, only_lz, floor_tag) # url, only_lz, floor tag
tieba.start()


