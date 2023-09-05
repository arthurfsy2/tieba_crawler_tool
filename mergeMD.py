import os

def merge_md_files(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        output.write(input_file.read())
                        output.write('\n')

# 示例用法
directory = "./Download"  # 替换为实际的目录路径
output_file = "./Download2/merge.md"  # 替换为实际的输出文件路径
merge_md_files(directory, output_file)