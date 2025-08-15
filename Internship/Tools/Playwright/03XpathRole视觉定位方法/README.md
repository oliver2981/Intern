# Xpath/Role/视觉 定位方法

## 1. Xpath 定位 

XPath (XML Path Language) 是由国际标准化组织W3C指定的，用来在 XML 和 HTML 文档中选择节点的语言。



Playwright 的 Locator 参数也可以使用 Xpath语法，比如

原来这样根据CSS selector 选择的

```python
element = page.locator('[href="http://www.miitbeian.gov.cn"]')
```

改为 Xpath 可以这样写

```python
element = page.locator('//*[@href="http://www.miitbeian.gov.cn"]')
```



## 2. Playwright更推荐的定位 

CSS 选择器定位/xpath定位，都是根据 `HTML网页元素特征` 的定位，属于开发者角度的定位。

Playwright 优先不推荐这样，它推荐从用户角度视觉呈现的定位。

因为它觉得用户角度相对比较固定，不容易变， 而 html页面写法容易变化。



但有时，有的元素，没有通过用户视觉定位的特征。

开发者角度的这种HTML网页元素特征定位 还是有其优势的，必须要学习的。



## 3. 根据文本内容定位 

有时我们想获取页面包含某些文字的元素， 这用 css selector 不好选择，可以使用 Page/Locator 对象的 [get_by_text](https://playwright.dev/python/docs/api/class-locator#locator-get-by-text) 方法

比如，[点击打开这个网页](https://www.byhy.net/cdn2/files/selenium/stock1.html)，

如果要获取 所有 文本内容包含 `11` 的元素，就可以这样

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")

# 根据文本内容选择所有元素
elements = page.get_by_text('11').all()

# 打印出元素文本
for ele in elements:
    print(ele.inner_text())
```

运行发现，打印结果为

```
600111
600113
600115
```



如果，希望包含的内容是以 `11` 结尾的，就可以使用正则表达式对象 作为参数，如下

```python
import re
elements = page.get_by_text(re.compile("11$")).all()
```



正则表达式 `11$` 表示以 `11` 结尾，通过正则表达式，我们可以进行各种复杂的基于文本模式的定位。

## 4. 根据 元素 role 定位 

### 4.1 ARIA Role

Playwright 支持根据 元素 `角色 role）` 定位。

web应用现在有一种标准 称之为： `ARIA （Accessible Rich Internet Applications）`。

ARIA 根据web界面元素的用途，为这些元素定义了一套 [角色（ Role ）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles) 信息，添加到页面中，

从而 让 残疾人士，或者 普通人在 某种环境下（比如夜里，太空中），不方便使用常规方法操作应用，使用[辅助技术工具](https://www.w3.org/TR/wai-aria-1.2/#dfn-assistive-technology)，来操作 web 应用的。



ARIA 为 web 元素增加了一些 Role相关的属性定义，方便 `辅助技术工具` 识别和操作。

比如：当我们完成系统注册时，弹出提示信息，html通常会这样

```
<div class="alert-message">
  您已成功注册，很快您将收到一封确认电子邮件
</div>
```

但是，这样写的内容不方便辅助技术识别出这是一个重要的信息，需要读给用户听。

这时，可以加上 ARIA role 属性设置，如下

```
<div class="alert-message" role="alert">
  您已成功注册，很快您将收到一封确认电子邮件
</div>
```

因为 `role="alert"` 是 ARIA规范里面的属性， 辅助系统（比如读屏系统）会特别注意，就会侦测到，并且实时读出来。

所以，直接可以根据如下代码 定位该元素

```
# 根据 role 定位
lc = page.get_by_role('alert')

# 打印元素文本
print(lc.inner_text())
```



html元素中，有些 特定语义元素（semantic elements）被ARIA规范认定为自身就包含 ARIA role 信息，并不需要我们明显的加上 ARIA role 属性设置，

比如

```
<progress value="75" max="100">75 %</progress>
```

就等于隐含了如下信息

```
<progress value="75" max="100"
  role="progressbar"
  aria-valuenow="75"
  aria-valuemax="100">75 %</div>
```

所以，直接可以根据如下代码 定位该元素

```python
# 根据 role 定位
lc = page.get_by_role('progressbar')

# 打印元素属性 value 的值
print(lc.get_attribute('value'))
```



再比如 `search` 类型的输入框，默认就有 `searchbox` role，

```
<input type="search">
```

所以，直接可以根据如下代码 定位该元素

```python
lc = page.get_by_role('searchbox')
print(lc.fill('oliver'))
```

### 4.2 ARIA Attribute

ARIA规范除了可以给元素添加 `ARIA role` ，还可以添加其它 [ARIA属性（ARIA attributes）](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes) ，比如

```css
<div role="heading" aria-level="1">标题1</div>
<div role="heading" aria-level="2">标题2</div>
```

`aria-level` 就是一个 ARIA 属性，表示 role 为 `heading` 时的 `等级` 信息

上面的定义，其实和下面的 html 元素 h1/h2 等价

```
<h1>标题1</h1>
<h2>标题2</h2>
```

`h1` 隐含了 `role="heading" aria-level="1"` 属性

`h2` 隐含了 `role="heading" aria-level="2"` 属性



Playwright 对常见的 ARIA 属性 ，[有额外的参数](https://playwright.dev/python/docs/api/class-page#page-get-by-role)对应，

比如 `aria-checked/aria-disabled/aria-expanded/aria-level` 等等



上例中，h2 元素，隐含了 `role="heading" aria-level="2"`， 所以可以用下面代码定位

```python
lc = page.get_by_role('heading',level=2)
print(lc.inner_text())
```

### 4.3 Accessible Name

只根据 `ARIA role` 和 `ARIA属性` 往往并不能唯一定位元素。

role定位最常见的组合是 `ARIA role` 和 [Accessible Name](https://developer.mozilla.org/en-US/docs/Glossary/Accessible_name)

因为，`Accessible Name` 就像元素的 `名字` 一样，往往可以唯一定位。

html 元素标准属性 `name` 是浏览器内部的，用户看不到，比如



```
<a name='link2byhy' href="https://www.byhy.net">百月黑羽教程</a>
```



`Accessible Name` 不一样，它是元素界面可见的文本名，

比如上面的元素，暗含的 `Accessible Name` 值就是 `教程` ， 当然也暗含了 `ARIA role` 值为 `link`

所以，可以这样定位

```python
lc = page.get_by_role('link',name='白月黑羽教程')
print(lc.click())
```

上面的写法， 只要 Accessible Name 包含 参数name 的字符串内容即可，而且大小写不分， 并不需要完全一致。

所以，这样也可以定位到

```python
lc = page.get_by_role('link',name='白月黑羽')
```

如果需要 Accessible Name 和 参数name 的内容完全一致，可以指定 `exact=True` ，如下

```python
lc = page.get_by_role('link',name='白月黑羽', exact=True)
```



name值还可以通过[正则表达式](https://www.byhy.net/py/lang/extra/regex/)，进行较复杂的匹配规则，比如

```python
lc = page.get_by_role('link',name=re.compile("^白月.*羽"))
```



那么除了html 元素 a 以外， 哪些元素是自带 Accessible Name 属性的呢？

他们的 Accessible Name 值 又是怎么确定的呢？

[w3c计算规则文档](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/#name_calculation)



以下是一些常见的用法：

<a> <td> <button> Accessible Name 值 就是其内部的文本内容。



`<textarea> <input>` 这些输入框，它们的 Accessible Name 值 是和他们关联的 的文本。

比如：

```
<label>
  <input type="checkbox" /> Subscribe
</label>
```

这个 checkbox 的 Accessible Name 却是 `Subscribe` ，应该这样定位

```python
page.get_by_role("checkbox", name="Subscribe")
```



另外，一些元素 比如 `<img>` ，它的 Accessible Name 是其html 属性 `alt` 的值

比如

```
<img src="grape.jpg" alt="banana"/>
```

它的 Accessible Name 值为 `banana` ，role 为 `img`

### 4.4 使用 codegen 助手

Playwright 认为， 这种根据role定位是 用户 或者辅助技术 直观感知页面的方式， 应该是最优先使用的。

但是，哪些HTML元素有哪些隐含的 ARIA role 和 ARIA Attribute，对应的 Accessible Name又是什么？

我们可以使用 Playwright 的代码助手 `codegen` ，

代码助手产生代码时， 能使用 role定位的，会优先使用 role 定位。

输入如下命令：

```bash
playwright codegen
```

## 5. 其它用户视觉定位 

下面的这4种定位，也属于根据用户视觉上的内容定位。

可以通过代码助手产生，其实也完全可以用 css selector 定位替代。

### 5.1 根据 元素 placeholder 定位

`input` 元素，通常都有 `placeholder` 属性，

可以使用 Page/Locator 对象的 [get_by_placeholder](https://playwright.dev/python/docs/api/class-locator#locator-get-by-placeholder) 方法，根据 `placeholder` 属性值定位。



比如

```
<input type="text" placeholder="captcha" />
```

就可以这样定位

```python
page.get_by_placeholder('captcha',exact=True).fill('白月黑羽')
```

参数 `exact` 值为 `True` ，表示完全匹配，且区分大小写。如果值为False，就只需包含参数字符串即可，且不区分大小写。

作用类似 get_by_role 里面的 `exact` 参数

### 5.2 根据 元素关联的 label 定位

`input` 元素，通常都有关联的 label

可以使用 Page/Locator 对象的 [get_by_label](https://playwright.dev/python/docs/api/class-locator#locator-get-by-label) 方法，根据 元素关联的 label 定位。



比如

```
  <input aria-label="Username">
  <label for="password-input">Password:</label>
  <input id="password-input">
```

就可以这样定位

```python
page.get_by_label("Username").fill("john")
page.get_by_label("Password").fill("secret")
```



`get_by_label` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

### 5.3 根据 元素的 alt text 定位

有些元素，比如 `img` 元素，通常都有 `alt` 属性

可以使用 Page/Locator 对象的 [get_by_alt_text](https://playwright.dev/python/docs/api/class-locator#locator-get-by-alt-text) 方法，根据 元素的 `alt` 属性值 定位



比如

```
<img 
  src="https://doc.qt.io/qtforpython/_images/windows-pushbutton.png" 
  alt="qt-button">
```

就可以这样定位

```python
href = page.get_by_alt_text("qt-button").get_attribute('src')
print(href)
```



`get_by_alt_text` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

### 5.4 根据 元素 title 定位

有些元素，比如 `span`, `a` 等等，可能有 `title` 属性，当鼠标悬浮在该元素上时，可以显示title属性内在一个提示框里面

可以使用 Page/Locator 对象的 [get_by_title](https://playwright.dev/python/docs/api/class-locator#locator-get-by-title) 方法，根据 元素的 `title` 属性值 定位



比如

```
  <a href="https://www.byhy.net" title="byhy首页">白月黑羽教程</a>
```

就可以这样定位

```python
page.get_by_title("byhy首页").click()
```



`get_by_title` 也有 `exact` 参数，作用和 `get_by_placeholder` 里面的 `exact` 参数 一样。

## 6. 缺省等待时间 

Playwright 中，当我们定位元素（比如 通过locator/get_by_text 等方法）后，对元素进行操作（比如 click, fill），

如果当时根据定位条件，找不到这个元素， Playwright并不会立即抛出错误， 而是缺省等待元素时间为30秒，在30秒内如果元素出现了，就立即操作成功返回。

比如，[点击打开这个网页](https://www.byhy.net/cdn2/files/selenium/stock1.html)。

这个网页，我们输入股票名称关键字，点击搜索后， 搜索结果并不是立即返回的，而是有 一定的延时。

但是，如下代码并没有sleep之类的等待，也没有设置缺省等待时间，为什么在 打印 id为1的元素文本时，不会报错呢？

```python
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
page.locator('#kw').fill('通讯\n')
page.locator('#go').click()
element = page.locator("[id='1']")

print(element.inner_text())
```



因为Playwright不需要我们额外设置，本来元素操作时，如果根据定位规则找不到元素，就会等待最多 30秒。



如果修改下面的代码

```python
print(element.inner_text())
```

改为

```python
print(element.inner_text(timeout=10 ))
```

表示等待元素出现时长修改为10毫秒，再运行，就会有错误了。



如果，想修改 `缺省` 等待时间， 可以使用 `BrowserContext` 对象， 如下

```python
from playwright.sync_api import sync_playwright
p = sync_playwright().start()

browser = p.chromium.launch(headless=False, slow_mo=50)
context = browser.new_context()
context.set_default_timeout(10) #修改缺省等待时间为10毫秒
page = context.new_page() # 通过context 创建Page对象
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
page.locator('#kw').fill('通讯\n')
page.locator('#go').click()

element = page.locator("[id='1']")
print(element.inner_text())
```

可以发现缺省等待时间修改为10毫秒，后续操作等待时间无需单独指定，都是10毫秒了。