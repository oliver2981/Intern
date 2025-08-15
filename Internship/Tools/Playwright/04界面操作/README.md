# 界面操作

## 1. 元素通用操作 

### 1.1 获取文本内容

通过 Locator对象的 [inner_text()](https://playwright.dev/python/docs/api/class-locator#locator-inner-text) 方法 可以获取元素的内部文本，

如果Locator选择到的元素是多个，可以使用 [all_inner_texts](https://playwright.dev/python/docs/api/class-locator#locator-all-inner-texts) 获取所有匹配的文本，放到列表中返回。



上面者两个方法返回的都是元素内部的 `可见` 文本。

html 元素内部还可以包括不可见的文本，比如

```
<p id="source">
  <span id='text'>看一下<br>这个内容<br>如何变化</span>
  <span style="display:none">隐藏内容</span>
</p>
```

要获取p元素内部所有内容，包括隐藏内容，可以用 Locator对象的 [text_content()](https://playwright.dev/python/docs/api/class-locator#locator-text-content) 或者 [all_text_contents()](https://playwright.dev/python/docs/api/class-locator#locator-all-text-contents) 方法 获取 `单个` 或者 `多个` 匹配对象文本

如下所示

```
lc = page.locator("#source")
print('innerText:',   lc.inner_text())
print('--------------')
print('textContent:', lc.text_contentS())
```

### 1.2 获取元素属性

获取元素的属性值，可以使用 Locator对象的 [get_attribute](https://playwright.dev/python/docs/api/class-locator#locator-get-attribute) 方法

### 1.3 获取元素内部Html

获取元素内部的整个html文本， 可以使用 Locator对象的 [inner_html](https://playwright.dev/python/docs/api/class-locator#locator-inner-html) 方法

### 1.4 点击

前面讲过的Locator对象的 [click](https://playwright.dev/python/docs/api/class-locator#locator-click) 方法，是 `单击` 元素



如果要 `双击` ，可以使用 [dblclick](https://playwright.dev/python/docs/api/class-locator#locator-dblclick) 方法

### 1.5 悬停

让光标悬停在某个元素上方，可以使用 Locator对象的 [hover](https://playwright.dev/python/docs/api/class-locator#locator-hover) 方法

### 1.6 等待元素可见

Playwright通过Locator对元素进行操作时，如果元素当前还没有出现，缺省就会等待30秒。

但是，有时我们的代码并不是要操作这个元素，而是要等待这个元素出现后，进行别的操作。

这时，可以使用 Locator对象的 [wait_for](https://playwright.dev/python/docs/api/class-locator#locator-wait-for) 方法

比如

```
page.locator("#source").wait_for()
```

该方法有个参数 `state` ，缺省值为 `'visible'` ， 就是等待元素可见。

如果值为 `'hidden'` 就是等待该元素消失。



等待时长为全局设定的时长， 缺省为 30秒，如果要修改，可以使用参数 `timeout`。

超出时长，元素还没有出现在界面上，会抛出错误。

### 1.7 判断元素是否可见

有时，我们的自动化代码需要根据当前界面中，`是否存在某些内容` ，来决定下一步操作。

这时，可以使用 Locator对象的 [is_visible](https://playwright.dev/python/docs/api/class-locator#locator-is-visible) 方法

比如

```
page.locator("#source").is_visible()
```



该方法不会等待元素出现，而是立即返回 True 或 False 。

## 2. 输入框操作 

### 2.1 文本框输入

单行文本框 `input` 或者 多行文本框 `textarea` 都可以使用 Locator对象的 [fill](https://playwright.dev/python/docs/api/class-locator#locator-fill) 方法进行输入

### 2.2 文本框清空

要清空 单行文本框 `input` 或者 多行文本框 `textarea` 的内容，都可以使用 Locator对象的 [clear](https://playwright.dev/python/docs/api/class-locator#locator-clear) 方法

### 2.3 获取输入框里面的文字

如果要获取输入框 `<input>` ， `<textarea>` 对应的用户输入文本内容，不能用 `inner_text()` 方法。

而是应该用 [input_value](https://playwright.dev/python/docs/api/class-locator#locator-input-value) 方法

### 2.4 文件输入框

html中 有文件类型的输入框，用于指定本地文件， 通常用于上传文件

```
<input type="file" multiple="multiple">
```

要设置选中的文件，可以使用 Locator 对象的 [set_input_files](https://playwright.dev/python/docs/api/class-locator#locator-set-input-files) 方法。

比如

```
# 先定位
lc = page.locator('input[type=file]')

# 单选一个文件
lc.set_input_files('d:/1.png')

# 或者 多选 文件
lc.set_input_files(['d:/1.png', 'd:/2.jpg'])
```

### 2.5 radio单选/checkbox多选

[请点击打开这个网址](https://www.byhy.net/cdn2/files/selenium/test2.html)

并且按F12，观察HTML的内容



常见的选择框包括： radio框、checkbox框、select框

`radio` 是常见的 点选 元素

比如, 下面的 html：

```
<div id="s_radio">
  <input type="radio" name="teacher" value="小江老师">小江老师<br>
  <input type="radio" name="teacher" value="小雷老师">小雷老师<br>
  <input type="radio" name="teacher" value="小凯老师" checked="checked">小凯老师
</div>
```

如果要点选 radio框， 可以使用 Locator对象的 [check](https://playwright.dev/python/docs/api/class-locator#locator-check) 方法

如果要取消选择 radio框， 可以使用 Locator对象的 [uncheck](https://playwright.dev/python/docs/api/class-locator#locator-uncheck) 方法

如果我们要判断 radio框 是否选中，可以使用 Locator对象的 [is_checked](https://playwright.dev/python/docs/api/class-locator#locator-is-checked) 方法



假设，我们对上面html中的 radio 输入框

- 先打印当前选中的老师名字
- 再选择 小雷老师

对应的代码如下

```python
# 获取当前选中的元素
lcs = page.locator('#s_radio input[name="teacher"]:checked').all()
teachers = [lc.get_attribute('value')  for lc in lcs ]
print('当前选中的是:', ' '.join(teachers))

# 确保点选 小雷老师
page.locator("#s_radio input[value='小雷老师']").check()
```



`checkbox` 是常见的 勾选 元素

比如, 下面的html：

```
<div id="s_checkbox">
  <input type="checkbox" name="teacher" value="小江老师" checked="checked">小江老师<br>
  <input type="checkbox" name="teacher" value="小雷老师">小雷老师<br>
  <input type="checkbox" name="teacher" value="小凯老师" checked="checked">小凯老师
</div>
```

和 radio input 一样，

如果要点选 checkbox框， 可以使用 Locator对象的 [check](https://playwright.dev/python/docs/api/class-locator#locator-check) 方法

如果要取消选择 checkbox框， 可以使用 Locator对象的 [uncheck](https://playwright.dev/python/docs/api/class-locator#locator-uncheck) 方法

如果我们要判断 checkbox 框 是否选中，可以使用 Locator对象的 [is_checked](https://playwright.dev/python/docs/api/class-locator#locator-is-checked) 方法

比如, 我们要在前面面的html中

- 先打印当前选中的老师名字
- 再选择 小雷老师

对应的代码如下

```
# 获取当前选中的元素
lcs = page.locator('#s_checkbox input[name="teacher"]:checked').all()
teachers = [lc.get_attribute('value')  for lc in lcs ]
print('当前选中的是:', ' '.join(teachers))

# 点选 小雷老师
page.locator("#s_checkbox input[value='小雷老师']").click()
```

### 2.6 select元素操作

radio框及checkbox框都是input元素，只是里面的type不同而已。

select框 则是一个新的select标签，大家可以对照浏览器网页内容查看一下



要选择选项，可以使用 `select` 元素对应的 Locator对象的 [select_option](https://playwright.dev/python/docs/api/class-locator#locator-select-option) 方法

#### 2.6.1 select单选框

对于 select单选框：

不管原来选的是什么，直接用Select方法选择即可。

例如，选择示例里面的小江老师，示例代码如下

```
page.locator('#ss_single').select_option('小江老师')
```

这里 select_option 参数是 选项 `option` 元素 的 `value 或者 选项文本` ， 要完全匹配。



也可以使用关键字参数 `index` , `value` , `label` 指定分别根据 索引，value属性， 选项文本 进行匹配

比如

```
# 根据 索引 选择， 从0 开始， 但是为0的时候，好像有bug
page.locator('#ss_single').select_option(index=1)

# 根据 value属性 选择
page.locator('#ss_single').select_option(value='小江老师')

# 根据 选项文本 选择
page.locator('#ss_single').select_option(label='小江老师')

# 清空所有选择
page.locator('#ss_single').select_option([])
```

#### 2.6.2 select多选框

对于select多选框，要选中某几个选项，同样可以使用上面的方法，参数为包含多个值的列表即可

比如

```
# 根据 value属性 或者 选项文本 多选
page.locator('#ss_multi').select_option(['小江老师', '小雷老师'])

# 根据 value属性 多选
page.locator('#ss_multi').select_option(value=['小江老师', '小雷老师'])

# 根据 选项文本 多选
page.locator('#ss_multi').select_option(label=['小江老师', '小雷老师'])

# 清空所有选择
page.locator('#ss_multi').select_option([])
```

注意，原来已经选中的选项，没有出现在 参数里面的，自动被清除选择。

#### 2.6.3 获取select选中选项

同样可以通过css selector 表达式 `:checked` 伪选择 获取所有选中的 select选项

比如：

```
page.locator('#ss_multi').select_option(['小江老师','小雷老师'])

lcs = page.locator('#ss_multi option:checked').all_inner_texts()
print(lcs)
```

## 3. 网页操作 

### 3.1 打开网址/刷新/前进/后退

要 `打开网址/刷新/前进/后退` ， 可以分别调用 Page 对象的 `goto/reload/go_back/go_forward` 方法

### 3.2 获取网页Html

要 `获取整个网页对应的HTML` ， 可以调用 Page 对象的 `content` 方法

### 3.3 title

要 `获取整个网页的标题栏文本` ， 可以调用 Page 对象的 `title` 方法

### 3.4 set-viewport-size

要 `设置页面大小` ， 可以调用 Page 对象的 `set_viewport_size` 方法

比如

```
page.set_viewport_size({"width": 640, "height": 480})
```

设置宽度/高度的单位是 像素 。