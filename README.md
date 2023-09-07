一个可以批量爬取指定百度贴吧贴子，下载并转换为.md格式的python脚本。

注：
1、本项目是基于此项目的魔改，默认选取所有评论以及添加楼层的分割线。[yuzequn095/tieba_crawler_tool: Use Python3 to backup Baidu tieba content](https://github.com/yuzequn095/tieba_crawler_tool/)
2、本项目仅用于个人贴子的备份

使用：

1. 在`base_url.txt`文件内填入需要备份的贴吧贴子，`https://tieba.baidu.com/p/XX`格式，且一行只能有一个地址。以下仅为示意参考：
```
https://tieba.baidu.com/p/8585923792
https://tieba.baidu.com/p/8585862755
```

2. 在项目当前目录运行`py multi_tieba_spy.py`即可将贴子下载并处理为.md格式，并保存到`Download`文件夹
注意：本脚本设置了间隔10秒钟再备份下一个地址（防止封IP）
可以修改以下代码的time.sleep(10)的数字
```
for url in base_url:
    print(f'命令：py "tieba_fetch_tool.py" {url}')
    command = f'py {tool_path} "{url}"'
    subprocess.run(command)
    time.sleep(10)  # 在每次循环后等待N秒，防止封IP
```


可选功能：
1. 批量添加frontmatter（配合vuepress使用，可将处理后的.md作为vuepress的页面展示）
运行`py ADDfrontmatter.py`，即可将添加好frontmatter内容的文件添加到`Download2`文件夹

2. 批量将多个.md文件合并为一个.md文件
运行`PY mergeMD.py`，即可将多个.md文件合并为merge.md，并添加到`Download2`文件夹

3. 下载markdown文件内所有`![](xxx.jpg)`的图片
运行`PY mdPicDownload.py`，即可批量下载图片到`PicDownload`文件夹。（需要在`mdPicDownload.py`内设置需要读取的markdown文件路径。