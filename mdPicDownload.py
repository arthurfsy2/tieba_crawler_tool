import os
import re
import requests

def download_images_from_md(md_file, save_dir):
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()
        image_urls = re.findall(r'!\[\]\((.*?)\)', content)
        for url in image_urls:
            response = requests.get(url)
            if response.status_code == 200:
                image_name = url.split('/')[-1]
                save_path = os.path.join(save_dir, image_name)
                with open(save_path, 'wb') as image_file:
                    image_file.write(response.content)
                    print(f'Downloaded image: {save_path}')

# 示例用法
md_file = r'XXX'  # 替换为实际的.md文件路径
save_dir = r'./PicDownload'  # 替换为实际的保存目录路径
download_images_from_md(md_file, save_dir)
