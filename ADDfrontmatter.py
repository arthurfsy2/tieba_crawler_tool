import os

pathA = "./Download"  # 替换为实际的源目录路径
pathB = "./Download2"  # 替换为实际的目标目录路径

for filename in os.listdir(pathA):
    if filename.endswith(".md"):
        file_pathA = os.path.join(pathA, filename)
        file_pathB = os.path.join(pathB, filename)
        title = os.path.splitext(filename)[0]  # 获取文件名并去除扩展名
        with open(file_pathA, "r",encoding='utf-8') as fileA:
            content = fileA.read()
            new_content = f'---\ntitle: {title}\nicon: "pencil"\ncategory:\n  - Arthur\ntag:\n  - 贴吧\n---\n\n{content}'
        with open(file_pathB, "w",encoding='utf-8') as fileB:
            fileB.write(new_content)
