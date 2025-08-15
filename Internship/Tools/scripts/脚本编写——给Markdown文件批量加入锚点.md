# 脚本编写——给 Markdown 文件批量加入锚点

> **背景：**我现在有几百个 Markdown 格式的文件在 D 盘里的一个文件夹里许多不同的文件夹里，我制作了一个脚本给这些文件分章节加入锚点，方便以后进行链接的跳转。

## 1. 脚本代码

以下是我根据需求编写的代码：

```python
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

```

## 2. 代码解读

这段代码主要用于处理Markdown文件中的标题，为各级标题添加编号和锚点。下面我将详细解释代码中用到的每个方法和相关用法：

### 2.1 导入模块
```python
import os
import re
from pathlib import Path
```
- `os`：提供操作系统相关功能，如文件路径操作
- `re`：正则表达式模块，用于字符串匹配
- `pathlib.Path`：面向对象的文件系统路径操作，比传统os.path更现代

### 2.2 process_markdown_file函数

这是核心函数，处理单个Markdown文件。

#### 2.2.1 文件读取
```python
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
```
- `open()`：以只读模式('r')打开文件，指定UTF-8编码
- `f.read()`：一次性读取整个文件内容

#### 2.2.2 分割行
```python
lines = content.split('\n')
```
- `split('\n')`：按换行符分割文本为行列表

#### 2.2.3 处理各级标题
使用字典`current_levels`记录各级标题的当前编号：
```python
current_levels = {2: 0, 3: 0, 4: 0}
```

##### 二级标题处理
```python
if line.startswith('## ') and not line.startswith('###'):
    current_levels[2] += 1
    current_levels[3] = 0  # 重置下级计数器
    current_levels[4] = 0
    title = line[3:].strip()
    new_line = f"## {title} {{#{current_levels[2]}}}"
```
- `startswith()`：检查字符串是否以指定前缀开头
- `strip()`：去除字符串两端空白
- f-string：格式化字符串，插入变量值

##### 三级标题处理
```python
elif line.startswith('### ') and not line.startswith('####'):
    current_levels[3] += 1
    current_levels[4] = 0
    title = line[4:].strip()
    new_line = f"### {title} {{#{current_levels[2]}-{current_levels[3]}}}"
```

##### 四级标题处理
```python
elif line.startswith('#### '):
    current_levels[4] += 1
    title = line[5:].strip()
    new_line = f"#### {title} {{#{current_levels[2]}-{current_levels[3]}-{current_levels[4]}}}"
```

#### 2.2.4 文件写入
```python
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
```
- `'\n'.join()`：用换行符连接列表中的行
- `f.write()`：将内容写入文件

### 2.3 main函数
程序的主入口点。

#### 2.3.1 检查目录
```python
docs_dir = Path('D:\\sailwind_docs\\docs')
if not docs_dir.exists():
    print(f"目录 {docs_dir} 不存在")
    return
```
- `Path()`：创建Path对象表示路径
- `exists()`：检查路径是否存在

#### 2.3.2 遍历文件
```python
for root, _, files in os.walk(docs_dir):
    for file in files:
        if file.endswith('.md'):
            file_path = Path(root) / file
            print(f"正在处理: {file_path}")
            process_markdown_file(file_path)
```
- `os.walk()`：递归遍历目录树
- `endswith('.md')`：检查文件扩展名是否为.md
- `Path /`操作符：路径拼接

### 2.4 程序入口
```python
if __name__ == '__main__':
    main()
```
- `__name__ == '__main__'`：判断是否直接运行该脚本

### 关键知识点总结

1. **文件操作**：使用`with`语句确保文件正确关闭
2. **字符串处理**：`startswith()`, `strip()`, `split()`, `join()`
3. **路径操作**：推荐使用`pathlib`替代传统`os.path`
4. **递归遍历**：`os.walk()`是处理目录树的强大工具
5. **格式化字符串**：f-string提供简洁的字符串插值语法