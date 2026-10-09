# UI 自动化实践（Python + Playwright）

> 这是我实习结束后，**自己动手从零搭的一套 UI 自动化测试框架**。
> 仓库地址：[web-ui-automation](https://github.com/oliver2981/web-ui-automation)
>
> 实习时我用 **TypeScript + Playwright** 做过 UI 自动化，这次换成 **Python + Playwright** 又独立实现了一遍，
> 目的很简单：① 把实习里学到的分层思想真正吃透；② 验证自己不是只会某一套脚本，而是**理解了原理、换门语言照样能搭**。

---

## 1. 这个项目做了什么

对练习网站 [saucedemo.com](https://www.saucedemo.com/) 的**完整下单主流程**做端到端自动化测试：

> 登录 → 浏览商品 → 加入购物车 → 进入购物车 → 结算填信息 → 下单成功

技术栈：**Python + Playwright + pytest**，做到了 4 个页面对象、8 条用例全部通过。

### 目录分层（这是重点）

```
web-ui-automation/
├── config/settings.py     # 全局配置：站点地址、测试账号、超时（改一处，到处生效）
├── data/users.json        # 测试数据：各种账号（数据和逻辑分离）
├── pages/                 # Page Object：页面元素与业务动作
│   ├── base_page.py       #   基类：open / click / fill / text_of / is_visible
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                 # 用例层：只写业务和断言
├── conftest.py            # logged_in fixture + 失败自动截图钩子
├── pytest.ini             # 去哪找用例、结果写到哪
└── utils/logger.py        # 统一日志封装
```

**一句话概括这个分层：**
`用例层`只表达"要测什么"，`页面层`负责"怎么操作页面"，`配置/数据层`提供"变量从哪来"。
网站页面一改，只需要动 `pages/` 里对应的那个类，用例层不用动。

---

## 2. 用到的关键技术点

| 技术点 | 怎么用的 |
|---|---|
| **Page Object 分层** | 抽 `BasePage` 放公共操作，各页面类继承它，只写本页元素和动作 |
| **fixture 去重** | `conftest.py` 的 `logged_in` 把"打开站点 + 登录"抽出，商品/购物车/结算用例直接复用 |
| **参数化** | `@pytest.mark.parametrize` 让一个登录失败用例跑两组数据（锁定用户、密码错误） |
| **数据分离** | 账号放在 `data/users.json`，用 key 读取，扩展只加数据不改代码 |
| **报告 + 排错** | `--alluredir` 产出 Allure 报告；用 `pytest_runtest_makereport` 钩子实现**失败自动截图**并附到报告 |

常用命令：

```bash
pytest                       # 跑全部用例（无头）
pytest --headed              # 打开浏览器窗口跑
allure serve allure-results  # 查看 Allure 报告
```

---

## 3. 我学到了什么

1. **分层不是为了好看，是为了"改一处、到处生效"。**
   一开始我把元素定位直接写在用例里，页面一变就得满项目找；改成 Page Object 后，定位只在 `pages/` 里出现一次。

2. **自动化的稳定性，一大半靠"等待"，不是靠"重跑"。**
   我遇到过用例偶发失败——十次挂一两次。根因是页面还没渲染完脚本就去点按钮了（异步加载）。解决办法：定位统一用页面自带的 `data-test` 属性，并在 `CartPage` 里加显式等待 `_wait_until_loaded()`（等结算按钮出现才算加载完）。改完偶发失败就消失了。

3. **失败时要能"看到现场"。**
   光看一句 `AssertionError` 很难定位。加了钩子后，用例一失败就自动截图附进 Allure 报告，一眼能看到失败时页面停在哪、有没有报错弹窗。

4. **数据和逻辑要分开。**
   账号数据抽到 JSON 后，加一个失败场景只要加一行数据，不用碰函数体。

5. **fixture 是 pytest 里"可复用的测试前准备"。**
   定义在 `conftest.py`，测试函数把名字写成参数就能用——登录态不用每条用例重复写。

---

## 4. 和实习的 Playwright 用法：有什么异同

实习时在 AutoLib 项目里，我用的是 **TypeScript + Playwright**；这个项目是 **Python + Playwright**。两者**同一个 Playwright 内核**，但用法上有同有异：

### 相同的地方（说明原理是通用的）

- **都是 Playwright 内核**：自动等待、`data-test` 定位、浏览器驱动这些机制**完全一样**。
- **都用 Page Object 分层**：页面元素和业务动作封装成类，用例只写业务和断言——**这个思想跟语言无关**。
- **都靠"自动等待"解决稳定性**，而不是手写一堆 `sleep`。

### 不同的地方

| | 实习（AutoLib） | 本项目 |
|---|---|---|
| 语言 | TypeScript | Python |
| 用例运行器 | TS 的测试运行器 | pytest |
| 测试对象 | 公司真实产品（AutoLib） | 公开练习站 saucedemo |
| 定位 | 真实业务页面，元素更复杂 | 页面自带 `data-test`，更规范 |
| 数据/报告 | 跟着团队既有流程 | 自己搭：JSON 数据 + Allure 报告 + 失败截图 |

### 最大的体会

> **换个语言绑定，我照样能搭起来**——因为实习让我理解了 Playwright 和 Page Object 的**原理**，而不是只背下某一套代码。
> 实习项目让我见过**真实业务**的复杂度和 Bug；这个个人项目让我把"分层 + 参数化 + 报告"这套框架**独立地从零实现**了一遍。

---

## 5. 相关笔记

- 项目源码 / 说明：[github.com/oliver2981/web-ui-automation](https://github.com/oliver2981/web-ui-automation)
- 项目里的七篇学习笔记（在仓库 `docs/` 目录）：从环境搭建、Playwright 上手、Page Object、pytest 参数化、元素定位与断言，到失败截图与 Allure、项目复盘与面试话术。
- 实习期整理的 Playwright 基础笔记，见本仓库：`Internship/Tools/Playwright/`。
