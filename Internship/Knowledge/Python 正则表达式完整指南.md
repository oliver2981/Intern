# Python 正则表达式完整指南



## 简介

正则表达式（Regular Expression，简称regex）是一种强大的文本处理工具，使用特定模式来匹配和操作字符串。Python通过`re`模块提供完整的正则表达式支持。

### 基本概念

- **模式（Pattern）**: 定义搜索规则的字符串
- **匹配（Match）**: 在目标字符串中找到符合模式的内容
- **搜索（Search）**: 在字符串中查找模式的过程
- **替换（Substitution）**: 将匹配的内容替换为指定文本

## re模块核心方法

### 1. re.match()

从字符串起始位置匹配模式

```python
import re

result = re.match(r'hello', 'hello world')
if result:
    print("匹配成功:", result.group())  # 输出: hello
```

### 2. re.search()

在整个字符串中搜索第一个匹配项

```python
result = re.search(r'world', 'hello world')
if result:
    print("找到:", result.group())  # 输出: world
```

### 3. re.findall()

返回所有匹配项的列表

```python
results = re.findall(r'\d+', '3 apples, 12 bananas, 8 oranges')
print(results)  # 输出: ['3', '12', '8']
```

### 4. re.finditer()

返回匹配项的迭代器

```python
for match in re.finditer(r'\d+', '3 apples, 12 bananas'):
    print(match.group(), "at position", match.start())
```

### 5. re.sub()

替换匹配项

```python
text = re.sub(r'\d+', 'NUM', '3 apples, 12 bananas')
print(text)  # 输出: NUM apples, NUM bananas
```

### 6. re.compile()

编译正则表达式模式（提高重复使用效率）

```python
pattern = re.compile(r'\d+')
results = pattern.findall('3 apples, 12 bananas')
```

## 正则表达式语法

### 基本元字符

| 字符    | 描述                     | 示例                              |
| ------- | ------------------------ | --------------------------------- |
| `.`     | 匹配任意字符（除换行符） | `a.c` 匹配 "abc", "a c"           |
| `^`     | 匹配字符串开头           | `^Hello` 匹配 "Hello world"       |
| `$`     | 匹配字符串结尾           | `world$` 匹配 "hello world"       |
| `*`     | 前一个字符0次或多次      | `ab*` 匹配 "a", "ab", "abb"       |
| `+`     | 前一个字符1次或多次      | `ab+` 匹配 "ab", "abb"            |
| `?`     | 前一个字符0次或1次       | `ab?` 匹配 "a", "ab"              |
| `{m,n}` | 前一个字符m到n次         | `a{2,4}` 匹配 "aa", "aaa", "aaaa" |

### 字符类

| 模式     | 描述                  | 等效表示         |
| -------- | --------------------- | ---------------- |
| `[abc]`  | 匹配a、b或c           |                  |
| `[a-z]`  | 匹配任何小写字母      |                  |
| `[^abc]` | 匹配除a、b、c外的字符 |                  |
| `\d`     | 匹配数字              | `[0-9]`          |
| `\D`     | 匹配非数字            | `[^0-9]`         |
| `\w`     | 匹配单词字符          | `[a-zA-Z0-9_]`   |
| `\W`     | 匹配非单词字符        | `[^a-zA-Z0-9_]`  |
| `\s`     | 匹配空白字符          | `[ \t\n\r\f\v]`  |
| `\S`     | 匹配非空白字符        | `[^ \t\n\r\f\v]` |

### 分组与捕获

| 模式                | 描述         |
| ------------------- | ------------ |
| `(pattern)`         | 捕获分组     |
| `(?:pattern)`       | 非捕获分组   |
| `(?P<name>pattern)` | 命名捕获分组 |
| `\1`, `\2`          | 引用捕获分组 |

### 断言

| 模式           | 描述         |
| -------------- | ------------ |
| `(?=pattern)`  | 正向先行断言 |
| `(?!pattern)`  | 负向先行断言 |
| `(?<=pattern)` | 正向后行断言 |
| `(?<!pattern)` | 负向后行断言 |

### 修饰符

| 标志                     | 描述            |
| ------------------------ | --------------- |
| `re.IGNORECASE` / `re.I` | 忽略大小写      |
| `re.MULTILINE` / `re.M`  | 多行模式        |
| `re.DOTALL` / `re.S`     | 使`.`匹配换行符 |
| `re.VERBOSE` / `re.X`    | 允许注释和空格  |

## 常用模式示例

### 邮箱验证

```python
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
emails = ['test@example.com', 'invalid.email']
for email in emails:
    if re.match(email_pattern, email):
        print(f"{email} 是有效的邮箱地址")
```

### URL提取

```python
text = "Visit https://www.example.com and http://sub.domain.org/path"
url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w.-]*'
urls = re.findall(url_pattern, text)
print("找到的URL:", urls)
```

### 电话号码匹配

```python
phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}'
phones = re.findall(phone_pattern, "Call 123-4567 or (055) 1234-5678")
print("电话号码:", phones)
```

### HTML标签处理

```python
html = "<div>Content <span>inside</span> tags</div>"
# 移除所有HTML标签
clean_text = re.sub(r'<[^>]+>', '', html)
print("清理后文本:", clean_text)

# 提取所有标签内容
tags_content = re.findall(r'<(\w+)>(.*?)</\1>', html)
print("标签内容:", tags_content)
```

### 日期提取

```python
text = "Dates: 2023-12-25, 01/15/2023, 23.04.2023"
date_pattern = r'\b\d{4}[-./]\d{2}[-./]\d{2}\b|\b\d{2}[-./]\d{2}[-./]\d{4}\b'
dates = re.findall(date_pattern, text)
print("找到的日期:", dates)
```

## 高级技巧与性能优化

### 1. 使用编译模式

```python
# 低效方式
for text in large_text_collection:
    re.findall(r'complex_pattern', text)

# 高效方式
pattern = re.compile(r'complex_pattern')
for text in large_text_collection:
    pattern.findall(text)
```

### 2. 避免回溯灾难

```python
# 有问题：过多回溯
re.match(r'(a+)+b', 'a' * 1000)

# 改进：使用原子分组或占有量词
re.match(r'(?>(a+))+b', 'a' * 1000)
```

### 3. 使用非捕获分组提高性能

```python
# 不需要捕获时使用非捕获分组
pattern = re.compile(r'(?:http|https)://(?:www\.)?example\.com')
```

### 4. 利用预编译字符类

```python
# 使用预定义字符类而非自定义范围
re.findall(r'\w+', text)  # 优于 [a-zA-Z0-9_]
```

### 5. 使用re.VERBOSE提高可读性

```python
complex_pattern = re.compile(r"""
    ^\s*                 # 开头可能有的空白
    (\(\d{3}\))?        # 可选的区号，括号形式
    \s*                  # 可能有的空白
    \d{3}                # 前缀三位数
    [-.]?                # 可选的分隔符
    \d{4}                # 后缀四位数
    \s*                  # 结尾可能有的空白
    $                    # 字符串结束
""", re.VERBOSE)
```

## 常见问题与解决方案

### 1. 贪婪 vs 非贪婪匹配

```python
text = "<div>Content</div><div>More</div>"

# 贪婪匹配（默认）
greedy = re.findall(r'<div>.*</div>', text)
print("贪婪:", greedy)  # 匹配整个字符串

# 非贪婪匹配
non_greedy = re.findall(r'<div>.*?</div>', text)
print("非贪婪:", non_greedy)  # 匹配单个div标签
```

### 2. 多行匹配

```python
text = "First line\nSecond line\nThird line"

# 默认不匹配换行符
result1 = re.findall(r'^.*$', text)
print("单行模式:", result1)  # 整个文本作为一行

# 多行模式
result2 = re.findall(r'^.*$', text, re.MULTILINE)
print("多行模式:", result2)  # 每行作为单独匹配
```

### 3. Unicode字符处理

```python
# 匹配中文字符
chinese_text = "中文测试 English 混合"
chinese_chars = re.findall(r'[\u4e00-\u9fff]+', chinese_text)
print("中文字符:", chinese_chars)

# Unicode属性（需要regex库）
# import regex
# words = regex.findall(r'\p{L}+', unicode_text)
```

### 4. 复杂替换 with 回调函数

```python
def replace_callback(match):
    word = match.group(0)
    return word.upper() if len(word) > 3 else word

text = "this is a sample text with various words"
result = re.sub(r'\w+', replace_callback, text)
print("替换结果:", result)
```

## 实用工具与资源

### 在线测试工具

- [Regex101](https://regex101.com/) - 实时测试和调试
- [RegExr](https://regexr.com/) - 学习和测试正则表达式
- [Debuggex](https://www.debuggex.com/) - 可视化正则表达式

### 推荐学习资源

1. **官方文档**: [Python re模块文档](https://docs.python.org/3/library/re.html)
2. **书籍**: 《精通正则表达式》（Jeffrey Friedl）
3. **教程**: [Regular-Expressions.info](https://www.regular-expressions.info/)

### 性能测试工具

```python
import timeit

def test_performance():
    pattern = re.compile(r'\d{3}-\d{2}-\d{4}')
    text = 'My SSN is 123-45-6789 and another is 987-65-4321'
    return pattern.findall(text)

time = timeit.timeit(test_performance, number=10000)
print(f"执行10000次耗时: {time:.4f}秒")
```

------

## 总结

Python的正则表达式提供了强大的文本处理能力，掌握其核心概念和技巧可以显著提高文本处理效率。关键要点：

1. **选择合适的匹配方法**：根据需求使用match、search、findall或finditer
2. **理解贪婪与非贪婪**：合理使用`?`控制匹配行为
3. **使用编译模式**：提高重复使用时的性能
4. **掌握分组技巧**：合理使用捕获和非捕获分组
5. **注意性能优化**：避免回溯灾难，使用高效模式

正则表达式需要实践才能熟练掌握，建议结合实际项目多练习使用。