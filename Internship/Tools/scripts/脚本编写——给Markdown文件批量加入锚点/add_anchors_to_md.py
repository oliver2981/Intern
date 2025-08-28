import os
import re
from pathlib import Path


def process_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n') # 将文本里的内容按照每一行进行分类，splitlines() 略慢（需检测多种换行符）
    new_lines = []
    current_levels = {2: 0, 3: 0, 4: 0}  # 记录各级标题当前编号

    for line in lines:
        # 匹配二级标题 (##)
        if line.startswith('## ') and not line.startswith('###'):
            current_levels[2] += 1
            current_levels[3] = 0  # 重置三级标题计数器
            current_levels[4] = 0  # 重置四级标题计数器
            title = line[3:].strip() #移除标题后的空格，格式统一
            new_line = f"## {title} {{#{current_levels[2]}}}" # Markdown 里为标题添加锚点的格式
            new_lines.append(new_line)

        # 匹配三级标题 (###)
        elif line.startswith('### ') and not line.startswith('####'):
            current_levels[3] += 1
            current_levels[4] = 0  # 重置四级标题计数器
            title = line[4:].strip()
            new_line = f"### {title} {{#{current_levels[2]}-{current_levels[3]}}}"
            new_lines.append(new_line)

        # 匹配四级标题 (####)
        elif line.startswith('#### '):
            current_levels[4] += 1
            title = line[5:].strip()
            new_line = f"#### {title} {{#{current_levels[2]}-{current_levels[3]}-{current_levels[4]}}}"
            new_lines.append(new_line)

        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines)) # 逐行写入


def main():
    docs_dir = Path('D:\sailwind_docs\docs')
    if not docs_dir.exists():
        print(f"目录 {docs_dir} 不存在")
        return

    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file # 等效于file_path = os.path.join(root, file)
                print(f"正在处理: {file_path}")
                process_markdown_file(file_path)

    print("所有Markdown文件处理完成")


if __name__ == '__main__':
    main()
