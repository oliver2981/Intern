# 脚本编写——从JSON文件分类转换为Excel表格

> **背景**：在 D 盘 test 文件夹里有几百个测试用例相关的 json 文件，样式为：
>
> ```json
> [
>  {
>  "casetitle": "测试用例1",
>  "priority": "1",
>  "precondition": "无",
>  "steps": [
>      {"step": "步骤1", "expect": "预期1"},
>      {"step": "步骤2", "expect": "预期2"}
>  ],
>  "func_model": "模块A"
> },
> {
>  "casetitle": "测试用例2",
>  "priority": "2",
>  "precondition": "无",
>  "steps": [
>      {"step": "步骤1", "expect": "预期1"},
>      {"step": "步骤2", "expect": "预期2"}
>  ],
>  "func_model": "模块A"
> }
> ]
> ```
>
> 我现在需要一个 python 脚本，有以下几点需求：
>
> 1. 从 D 盘里面几百个 json 文件分类导入不同的 xlsx 文件里，还要再创造一个 xlsx 文件把这些 json 脚本全部导入同一个 excel表格，这些 json 文件靠文件名字里的数字分类（这些 json 文件名里都有如同第 1 章、第 2 章这样的开头）。
>
> 2. 每个 excel 文件里要有 8 列，分别为“所属模块”对应 json 文件名但不要文件扩展名、“用例标题”对应“casetitle”、“前置条件”对应“precondition”、“步骤”和“预期”对应“steps”、“优先级”对应“priority”。最右侧还有两行空列分别为“测试结果”和是否可用。
>
> 3. 每个步骤和预期结果加上 1. 2. 3. 这样的编号。
>
> 4. 汇总我希望是从第 1 章到最后一章按数字顺序汇总。
> 5. 适当美化一下生成的 xlsx 文件。

## 1. 代码示范

以下是按照需求制作的脚本代码

```python
import os
import json
import re
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill


def set_excel_style(ws):
    # 样式设置
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style="thin"),
                         right=Side(style="thin"),
                         top=Side(style="thin"),
                         bottom=Side(style="thin"))

    data_font = Font(name="微软雅黑", size=10)
    data_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # 应用标题样式
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = thin_border

    # 应用数据样式
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = data_font
            cell.alignment = data_alignment
            cell.border = thin_border

    # 智能列宽控制
    max_widths = {
        "步骤": 40,  # 限制最大40字符
        "预期": 40,
        "用例标题": 25,
        "所属模块": 20,
        "前置条件": 30
    }

    for col in ws.columns:
        col_letter = col[0].column_letter
        header = ws[f"{col_letter}1"].value

        if header in max_widths:
            # 计算列宽（不超过最大值）
            max_content_len = max(
                len(str(cell.value)) if cell.value else 0
                for cell in col
            )
            final_width = min(max_content_len, max_widths[header]) * 1.2
            ws.column_dimensions[col_letter].width = final_width
        else:
            # 常规列宽计算
            max_length = max(
                len(str(cell.value)) if cell.value else 0
                for cell in col
            )
            ws.column_dimensions[col_letter].width = (max_length + 2) * 1.2

    # 冻结标题行
    ws.freeze_panes = "A2"


def process_json_files():
    input_dir = r"D:\test"
    output_dir = r"D:\test_output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_data = []
    chapter_data = {}
    columns = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "优先级", "测试结果", "是否可用"]

    # 第一阶段：数据收集
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            module_name = os.path.splitext(filename)[0]
            match = re.search(r"(\d+)", filename)
            chapter_num = int(match.group(1)) if match else 999

            filepath = os.path.join(input_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    continue

                for case in data:
                    # 生成带编号的步骤和预期
                    steps_list = [f"{i + 1}. {step['step']}" for i, step in enumerate(case["steps"])]
                    expect_list = [f"{i + 1}. {step['expect']}" for i, step in enumerate(case["steps"])]

                    row = {
                        "所属模块": module_name,
                        "用例标题": case["casetitle"],
                        "前置条件": case["precondition"],
                        "步骤": "\n".join(steps_list),
                        "预期": "\n".join(expect_list),
                        "优先级": case["priority"],
                        "测试结果": "",
                        "是否可用": ""
                    }

                    # 存储到章节字典
                    if chapter_num not in chapter_data:
                        chapter_data[chapter_num] = []
                    chapter_data[chapter_num].append(row)
                    all_data.append(row)

    # 第二阶段：生成分章文件
    for ch_num, data in chapter_data.items():
        if ch_num == 999:
            output_filename = "未分类.xlsx"
        else:
            output_filename = f"第{ch_num}章.xlsx"

        chapter_filepath = os.path.join(output_dir, output_filename)
        df = pd.DataFrame(data)
        df.to_excel(chapter_filepath, index=False, columns=columns)

        # 应用样式
        wb = load_workbook(chapter_filepath)
        ws = wb.active
        set_excel_style(ws)
        wb.save(chapter_filepath)

    # 第三阶段：生成排序后的汇总文件
    if chapter_data:
        summary_path = os.path.join(output_dir, "汇总.xlsx")

        # 按章节数字排序（1→2→3...→未分类）
        sorted_chapters = sorted([k for k in chapter_data.keys() if k != 999])
        sorted_data = []

        for ch in sorted_chapters:
            sorted_data.extend(chapter_data[ch])
        if 999 in chapter_data:
            sorted_data.extend(chapter_data[999])

        # 生成并保存
        df_all = pd.DataFrame(sorted_data)
        df_all.to_excel(summary_path, index=False, columns=columns)

        # 应用样式
        wb = load_workbook(summary_path)
        ws = wb.active
        set_excel_style(ws)
        wb.save(summary_path)


if __name__ == "__main__":
    process_json_files()
```

## 2. 完整代码解析

### 2.1 导入模块部分
```python
import os
import json
import re
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
```
- `os`：用于操作系统文件路径和目录操作
- `json`：处理JSON格式的测试用例文件
- `re`：正则表达式模块，用于提取章节数字
- `pandas`：数据处理核心库，用于生成Excel
- `openpyxl`相关导入：用于Excel样式设置

### 2.2 样式设置函数
```python
def set_excel_style(ws):
    # 样式配置
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
```
- `PatternFill`：设置标题行蓝色背景填充
- `Font`：定义标题字体样式（微软雅黑/加粗/白色）

### 2.3 边框和对齐设置
```python
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style="thin"), 
                        right=Side(style="thin"), 
                        top=Side(style="thin"), 
                        bottom=Side(style="thin"))
```
- `Alignment`：设置单元格文字居中对齐并自动换行
- `Border`：定义统一的细边框样式

### 2.4 数据单元格样式
```python
    data_font = Font(name="微软雅黑", size=10)
    data_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
```
- 数据行使用稍小的字体
- 左对齐+顶部对齐，保证多行文本显示整齐

### 2.5 列宽智能控制
```python
    max_widths = {
        "步骤": 40,  # 限制最大40字符
        "预期": 40,
        "用例标题": 25,
        "所属模块": 20
    }
```
- 定义各列最大宽度限制（字符数）
- 特别控制"步骤"和"预期"列不超过40字符

### 2.6 主处理函数
```python
def process_json_files():
    input_dir = r"D:\test"
    output_dir = r"D:\test_output"
```
- `input_dir`：原始JSON文件存放路径
- `output_dir`：生成的Excel输出路径

### 2.7 数据收集阶段
```python
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            module_name = os.path.splitext(filename)[0]
```
- 遍历输入目录所有.json文件
- 去除扩展名获取模块名称

### 2.8 章节数字提取
```python
            match = re.search(r"(\d+)", filename)
            chapter_num = int(match.group(1)) if match else 999
```
- 使用正则提取文件名中的数字
- 无数字文件归到999（未分类章节）

### 2.9 测试用例处理
```python
            steps_list = [f"{i+1}. {step['step']}" for i, step in enumerate(case["steps"])]
            expect_list = [f"{i+1}. {step['expect']}" for i, step in enumerate(case["steps"])]
```
- 生成带编号的步骤列表（如"1. 打开浏览器"）
- 同步生成带编号的预期结果

### 2.10 数据排序逻辑
```python
    sorted_chapters = sorted([k for k in chapter_data.keys() if k != 999])
    for ch in sorted_chapters:
        sorted_data.extend(chapter_data[ch])
```
- 先排序数字章节（1,2,3...）
- 最后追加未分类章节（999）

### 2.11 Excel生成
```python
    df_all.to_excel(summary_path, index=False, columns=columns)
    wb = load_workbook(summary_path)
    ws = wb.active
    set_excel_style(ws)
```
- 用pandas生成原始Excel
- 用openpyxl加载后应用样式
- 最后保存美化后的文件

### 2.12 主程序入口
```python
if __name__ == "__main__":
    process_json_files()
```
- 标准Python主程序入口
- 直接调用处理函数开始执行

这个脚本实现了从JSON测试用例到美化Excel的完整转换流程，包含智能排序、样式控制和列宽优化等功能。
