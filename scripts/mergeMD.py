import os
from jinja2 import Template
import re
import json
from datetime import datetime

def extract_info_from_filename(filename):
    # 定义正则表达式来匹配文件名格式
    pattern = r'(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<hour>\d{2})\s+(?P<minute>\d{2})_(?P<tiezi_id>\d+)_(?P<tieba_name>[^_]+)_(?P<reply_num>回复\(\d+\))_(?P<title>.+?)\.md'
    
    match = re.match(pattern, filename)
    if match:
        date_str = match.group('date')
        hour = match.group('hour')
        minute = match.group('minute')
        
        # 组合日期和时间
        full_datetime_str = f"{date_str} {hour}:{minute}"
        tiezi_id = match.group('tiezi_id')
        tieba_name = match.group('tieba_name')
        reply_num = match.group('reply_num')
        title = match.group('title')
        
        # # 转换日期字符串为日期对象
        # date = datetime.strptime(full_datetime_str, '%Y-%m-%d').date()
        
        return {
            'date': full_datetime_str,
            'tiezi_id': tiezi_id,
            'tieba_name': tieba_name,
            'reply_num': reply_num,
            'title': title,
        }
    else:
        raise ValueError("Filename does not match the expected format.")




def merge_md_list(info_total, list_output_file):
    import urllib.parse
    
    # 创建表格头部
    content_list = "| 序号 | 发贴日期 | 贴吧名称 | 贴子标题 |回复数 |\n"
    content_list += "|----------|----------|----------|----------|----------|\n"
    
    for i, info in enumerate(info_total,start=1):
        content_list += f'|{i}| {info["date"]} | [ {info["tieba_name"]} ](https://tieba.baidu.com/f?kw={urllib.parse.quote(info["tieba_name"])} "{info["tieba_name"]}吧") | [ {info["title"]} ](https://tieba.baidu.com/p/{info["tiezi_id"]}) | {info["reply_num"]} |\n'
        
    output = list_template.render(
        author = author,
        oldest_date=info_total[-1]["date"].split(" ")[0],
        content_list=content_list,
    )

    # 写入输出文件
    with open(list_output_file, 'w', encoding='utf-8') as f:
        f.write(output)



def merge_md_files(directory, merge_output_file, list_output_file):
    info_total =[]
    content_merge = ''

    # 收集所有 .md 文件及其日期
    md_files_with_dates = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # print("file:",file)
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                info = extract_info_from_filename(file)
                info_total.append(info)
                
                date = info["date"]
                
                if date:
                    md_files_with_dates.append((date, file_path))
    info_total.sort(key=lambda x: x['date'], reverse=True)
    merge_md_list(info_total, list_output_file)
    

    # 按日期从最新到最远排序
    md_files_with_dates.sort(key=lambda x: x[0], reverse=True)

    # 读取并合并文件内容
    for _, file_path in md_files_with_dates:
        with open(file_path, 'r', encoding='utf-8') as input_file:
            content_merge += input_file.read() + '\n'

    # 渲染输出
    output = merge_template.render(
        author = author,
        oldest_date = md_files_with_dates[-1][0].split(" ")[0],
        content_merge=content_merge,
    )
    
    # 写入输出文件
    with open(merge_output_file, 'w', encoding='utf-8') as f:
        f.write(output)


if __name__ == "__main__":
    with open("scripts/config.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    author = data["author"]
    directory = data["directory"]
    save_dir = data["save_dir"]
    pic_base_url = data["pic_base_url"]
    merge_output_file = data["merge_output_file"]
    list_output_file = data["list_output_file"]
    merge_template_path = data["merge_template_path"]
    list_template_path = data["list_template_path"]
    Cookie = data["Cookie"]

    with open(merge_template_path, 'r', encoding='utf-8') as f:
        merge_template = Template(f.read())

    with open(list_template_path, 'r', encoding='utf-8') as f:
        list_template = Template(f.read())
    merge_md_files(directory, merge_output_file, list_output_file)

