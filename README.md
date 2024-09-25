一个可以批量爬取指定百度贴吧贴子，下载并转换为.md格式的python脚本。

注：
1、本项目是基于此项目的魔改，默认选取所有评论以及添加楼层的分割线。[yuzequn095/tieba_crawler_tool: Use Python3 to backup Baidu tieba content](https://github.com/yuzequn095/tieba_crawler_tool/)
2、本项目仅用于个人贴子的备份

相对于原repo新增的功能：
1、可批量处理贴子链接，并生成单独的markdown文件
2、可批量下载图片
3、可批量汇总为列表、内容的markdown文件

## 使用：

1. 将 `configBAK.json`修改为 `script/config.json`，以下为配置说明：

```json
{
    "directory": "./Download", //单贴默认下载的路径，可改为你本地vuepress的文章路径
    "author":"author", //用来控制merge.list.md当中的作者信息（默认为author）
    "save_dir": "./PicDownload", //图片默认下载路径，可在下载后手动复制/上传到你的图床目录
    "base_url_path": "./scripts/base_url.txt", //多个贴子的链接保存路径
    "pic_base_url": "", //如果你有图床，可以在 `pic_base_url`当中填入你的图床根目录(，末尾需要带"/")，这样即可在线查看图片
    "merge_output_file" : "./output/merge.md", //mergeMD.py 生成merge.md文件的路径
    "list_output_file": "./output/list.md", //mergeM.py 生成list.md文件的路径
    "merge_template_path": "./template/tieba_merge_template.md",
    "list_template_path" : "./template/tieba_list_template.md",
    "Cookie":"" //手动获取你自己账号的Cookie，默认为无Cookie
}
```

2. 在 `base_url.txt`文件内填入需要备份的贴吧贴子，`https://tieba.baidu.com/p/XX`格式，且一行只能有一个地址。以下仅为示意参考：

```text
https://tieba.baidu.com/p/8585923792
https://tieba.baidu.com/p/8585862755
```

> 或者，你可以通过typora打开 `我的帖子-list.md`该文件，复制“[我的帖子](https://tieba.baidu.com/i/i/my_tie)”下的内容，直接粘贴到此文件当中。
> 如果有多页，需要手动翻页将所有内容复制到该文件
> 全部复制完后，运行 `py scripts/extract_tieba_link.py`进行提取链接，提取后的链接会自动保存到 `base_url.txt`当中

3. 在项目当前目录运行 `py scripts/tieba_fetch_tool.py`即可将贴子下载并处理为.md格式，并保存到 `Download`文件夹
   注意：本脚本设置了间隔10秒钟再备份下一个地址（防止封IP）
   可以修改以下代码的 `time.sleep(10)`的数字

> 此外，你也可以通过本地代理，实现更换IP获取。本程序默认本地代理链接是：`127.0.0.1::7890`，建议开启全局代理

```Python3
# 以下内容可见./scripts/tieba_fetch_tool.py
def get_page(self, page_number):
    try:
        # 代理设置
        proxies = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
        headers = {
            "cookie":'' # 这里也可以指定你的Cookie，用于获取被封的贴子（该贴只能本人账号进行查看）
        }
        url = self.thread_url + self.only_lz + '&pn=' + str(page_number)
        response = requests.get(url, headers=headers, proxies=proxies)
        return response.text
```

> 如果开启了全局代理，可以将time.sleep(10)的数值调小，等到无法获取数据时，更换另外的GLOBAL的IP即可

```Python3
# 以下内容可见./scripts/tieba_fetch_tool.py
if "# " not in base_url:
    print(base_url)
    tieba = Baidu_Tieba(base_url, only_lz, floor_tag, i) # url, only_lz, floor tag
    tieba.start()
    time.sleep(10)  # 在每次循环后等待N秒，防止封IP
```

PS:

1. 本程序会自动批量下载原有贴子的图片，并保存到 `PicDownload`文件夹当中。
2. 在output目录生成的merge.md、list.md的图片链接默认为本地的链接，如："../PicDownload"。

## 可选功能

1. 修改tieba_list_template.md/tieba_merge_template.md

> 配合vuepress使用，可将处理后的.md作为vuepress的页面展示。可修改模板当中的 `category`、`tag`

运行 `py scripts/mergeMD.py`，即可将添加好frontmatter内容的列表汇总、内容汇总的markdown文件生成到 `Download2`文件夹
