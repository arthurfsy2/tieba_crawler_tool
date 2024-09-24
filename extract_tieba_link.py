import re
from collections import OrderedDict

# 1. 读取文件内容
with open('我的帖子-list.md', 'r', encoding='utf-8') as file:
    content = file.read()

# 2. 使用正则表达式提取链接
pattern = r'https://tieba\.baidu\.com/p/[^?]+'
urls = re.findall(pattern, content)

# 3. 使用 set 去重
urls.sort(key=lambda x: int(x.split('/p/')[1]), reverse=True)
unique_urls = list(OrderedDict.fromkeys(urls))

# 4. 将链接写入新文件
with open('base_url_list.txt', 'w', encoding='utf-8') as output_file:
    for url in unique_urls:
        output_file.write(url + '\n')

print("链接已成功提取、去重并保存到 base_url_list.txt")
