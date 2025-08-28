# Django

## 1. 创建项目

```bash
pip install django
django-admin startproject oliver（yourprojectname）
```

- 最外层 `oliver/` 就是项目根目录 `d:\projects\oliver\` ， 项目文件都放在里面。

- `manage.py` 是一个工具脚本，用作项目管理的。以后我们会使用它执行管理操作。

- 里面的 `oliver/` 目录是python包。 里面包含项目的重要配置文件。这个目录名字不能随便改，因为manage.py 要用到它。

- `bysms/settings.py` 是 Django 项目的配置文件. 包含了非常重要的配置项，以后我们可能需要修改里面的配置。

- `bysms/urls.py` 里面存放了 一张表， 声明了前端发过来的各种http请求，分别由哪些函数处理. 这个我们后面会重点的讲。

- `bysms/wsgi.py`

  python 组织制定了 web 服务网关接口（Web Server Gateway Interface） 规范 ，简称wsgi。参考文档 https://www.python.org/dev/peps/pep-3333/

  遵循wsgi规范的 web后端系统， 可以理解为 由两个部分组成

  `wsgi web server` 和 `wsgi web application`

  它们通常是运行在一个python进程中的两个模块，或者说两个子系统。

  `wsgi web server` 接受到前端的http请求后，会调用 `wsgi web application` 的接口（ 比如函数或者类方法）方法，由`wsgi web application` 具体处理该请求。然后再把处理结果返回给 `wsgi web server`， `wsgi web server`再返回给前端。

## 2. 启动项目

```bash
python manage.py runserver 0.0.0.0:80
```

其中 `0.0.0.0:80` 是指定 web服务绑定的 IP 地址和端口。

`0.0.0.0` 表示绑定本机所有的IP地址， 就是可以通过任何一个本机的IP (包括 环回地址 `127.0.0.1` ) 都可以访问我们的服务。

`80` 表示是服务启动在80端口上。

请打开浏览器，地址栏输入 '127.0.0.1'

## 3. 创建项目app与url请求

进入项目根目录，执行下面的命令。

```bash
python manage.py startapp sales 
```

这样就会创建一个目录名为 sales， 对应 一个名为 sales 的app，里面包含了如下自动生成的文件。

```
sales/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

这个目录其实就是一个python package，开始进行如下设计，凡是浏览器访问的http 请求的 url 地址 是 `/sales/orders/` , 就由 views.py 里面的函数 `listorders` 来处理， 返回一段字符串给浏览器。

打开 views.py , 在里面加入如下内容

```python
from django.http import HttpResponse

def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息。。。")
```

打开项目设置目录下的 urls.py，在 `urlpatterns` 列表变量中添加一条路由信息，结果如下

```python
from django.contrib import admin
from django.urls import path

# 别忘了导入 listorders 函数
from sales.views import listorders

urlpatterns = [
    path('admin/', admin.site.urls),

    # 添加如下的路由记录
    path('sales/orders/', listorders),
]
```

`urlpatterns` 列表 就是 Django 的 url 路由的入口。

里面是一条条的路由记录，我们添加的

```python
path('sales/orders/', listorders)
```

就是告诉 当前端过来的请求 url地址 是 `/sales/orders/` (注意：最后的一个斜杠不能省略) , 就由 views.py 里面的函数 `listorders` 来处理。

复杂的系统url条目多达几百甚至上千个， 放在一个表中，查看时，要找一条路由记录就非常麻烦。

这时，我们通常可以将不同的路由记录 按照功能 分拆到不同的 **url路由子表** 文件中。

比如，这里我们可以把 访问 的 url 凡是 以 `sales` 开头的全部都 由 sales app目录下面的 子路由文件 urls.py 处理。

首先我们需要在 sales 目录下面创建一个新的文件 `sales\urls.py` 。

然后在这个 `sales\urls.py` 文件中输入如下内容

```python
from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.listorders),
]
```

然后，我们再修改主url路由文件 `oliver/urls.py` , 如下

```python
from django.contrib import admin

# 导入一个include函数
from django.urls import path, include

from sales.views import listorders
urlpatterns = [
    path('admin/', admin.site.urls),

    # 凡是 url 以 sales/  开头的，
    # 都根据 sales.urls 里面的 子路由表进行路由
    path('sales/', include('sales.urls')),

]
```

## 4. 数据库

项目中数据库的配置在 `oliver/settings.py` 中，这里

```python
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

开发系统，需要定义我们需要的数据库表。

首先，我们再创建一个名为common的应用目录， 里面存放我们项目需要的一些公共的表的定义。

 进入项目根目录，执行下面的命令。

```bash
python manage.py startapp common 
```

就会创建一个目录名为 common， 对应 一个名为 common 的app。

打开 common/models.py，发现里面是空的，因为我们还没有定义我们的业务所需要的表。

我们修改它，加入如下内容

```python
from django.db import models

class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)
```

这个 Customer 类继承自 django.db.models.Model， 就是用来定义数据库表的。

里面的 name、phonenumber、address 是该表的3个字段。

定义表中的字段 就是定义一些静态属性，这些属性是 django.db.models 里面的各种 Field 对象，对应不同类型的字段。

比如这里的3个字段 都是 CharField 对象，对应 varchar类型的数据库字段。

后面的参数 `max_length` 指明了该 varchar字段的 最大长度。

在项目的配置文件 `settings.py` 中， INSTALLED_APPS 配置项 加入如下内容

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 加入下面这行
    'common.apps.CommonConfig',
]
```

'common.apps.CommonConfig' 告诉 Django ， CommonConfig 是 common/apps.py 文件中定义的一个应用配置的类。

现在Django知道了我们的 common 应用， 我们可以在项目根目录下执行命令

```bash
d:\projects\bysms>python manage.py makemigrations common
```

得到如下结果

```bash
Migrations for 'common':
  common\migrations\0001_initial.py
    - Create model Customer
```

这个命令，告诉Django ， 去看看common这个app里面的models.py ，我们已经修改了数据定义， 你现在去产生相应的更新脚本。

执行一下，会发现在 common\migrations 目录下面出现了0001_initial.py, 这个脚本就是相应要进行的数据库操作代码。

随即，执行如下命令

```bash
d:\projects\bysms>python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, common, contenttypes, sessions
Running migrations:
  Applying common.0001_initial... OK
```

就真正去数据库创建表了。

Django提供了一个管理员操作界面可以方便的 添加、修改、删除你定义的 model 表数据。

首先，我们需要创建 一个超级管理员账号。

进入到项目的根目录，执行如下命令，依次输入你要创建的管理员的 登录名、email、密码。

```bash
d:\projects\bysms>python manage.py createsuperuser
```

然后我们需要修改应用里面的 管理员 配置文件 common/admin.py，注册我们定义的model类。这样Django才会知道



```python
from django.contrib import admin

from .models import Customer

admin.site.register(Customer)
```

好了，现在就可以访问 `http://127.0.0.1/admin/` ，输入刚才注册的用户密码登录。

我们已经创建了数据库和 Customer表。

现在我们来实现一个功能：浏览器访问 `sales/customers/` ，我们的服务端就返回系统中所有的客户记录给浏览器。



我们先实现一个函数，来处理浏览器发出的URL为 `sales/customers/` 的访问请求， 我们需要返回 数据库中 customer 表 所有记录。

Django 中 对数据库表的操作， 应该都通过 Model对象 实现对数据的读写，而不是通过SQL语句。

比如，这里我们要获取 customer 表 所有记录， 该表是和我们前面定义的 Customer 类管理的。

我们可以这样获取所有的表记录:

在文件sales/views.py 中，定义一个listcustomers 函数，内容如下：

```python
# 导入 Customer 对象定义
from  common.models import  Customer

def listcustomers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = Customer.objects.values()

    # 定义返回字符串
    retStr = ''
    for customer in  qs:
        for name,value in customer.items():
            retStr += f'{name} : {value} | '

        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)
```

我们还需要修改路由表， 加上对 `sales/customers/` url请求的 路由。

前面，我们在oliver\urls.py 主路由文件中，已经有如下的记录了

```python
    # 凡是 url 以 sales/  开头的，
    # 都根据 sales.urls 里面的 子路由表进行路由
    path('sales/', include('sales.urls')),
```

这条URL记录，指明 凡是 url 以 sales/ 开头的，都根据 sales.urls 里面的 子路由表进行路由。

我们只需修改 `sales/urls.py` 即可，添加如下记录

```python
    path('customers/', views.listcustomers),
```

## 5. 增删改查

