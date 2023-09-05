import subprocess
import time
base_url = []
tool_path="./tieba_fetch_tool.py"

base_url_path = "./base_url.txt"
with open(base_url_path, "r") as file:
    for line in file:
        url = line.strip()  # 去除行首行尾的空白字符
        base_url.append(url)




for url in base_url:
    print(f'命令：py "tieba_fetch_tool.py" {url}')
    command = f'py {tool_path} "{url}"'
    subprocess.run(command)
    time.sleep(10)  # 在每次循环后等待N秒，防止封IP


    