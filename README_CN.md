# SQL注入与反注入
[English](README.md) | 中文

![](https://skillicons.dev/icons?i=py,postgres)

在网络空间安全领域，SQL注入是发生在Web程序中数据库层的安全漏洞，是网站存在最多、最简单的漏洞。SQL攻防是空间信息安全的基础，可有效保护空间情报数据。为了学习、研究SQL注入，本项目仿真了一个基于PostgreSQL注入攻击的基本框架。后续，在Web程序代码中嵌入简单的参数化查询来防御注入行为。

## 注入原理
当访问动态网页时，Web服务器会向数据访问层发起SQL查询请求。如果权限验证通过就会执行SQL语句。在实际情况中，如果用户输入的数据被构造成恶意SQL代码，Web程序又未对动态构造的语句参数进行审查，就会留下安全漏洞。

当前，SQL注入的威胁主要有如下情况：

- 猜解后台数据库以盗取网站的敏感信息。

- 绕过认证，如绕过验证登录网站后台。

- 注入可借助数据库的存储过程进行提升权限等操作的恶意代码。

## 实验框架
**1、创建数据表**

基于PostgreSQL，使用[`sim_data.sql`](https://github.com/Rc-W024/SQL-injection/blob/main/sim_data.sql)示例代码创建一个空间情报信息表，包含`id`、`username`、`password`和`geom`字段，用于存储情报信息。并随机生成30组情报数据进行仿真。

![info](https://github.com/Rc-W024/SQL-injection/assets/97808991/4bf4972f-6508-40ad-b6a1-17ba2ece25c0)

**2、创建逻辑脚本**

创建一个简单的基于Python *Flask*框架的Web应用程序，以实现用户输入、查询逻辑，其中包含了一个用于可视化的HTML页面。需要注意的是，当使用*Flask*的`render_template`函数时，程序会在`templates`文件夹中查找与指定模板名称匹配的HTML文件。这种约定是为了组织和管理Web的模板文件，使其与其他代码分离，以提供更好的可维护性和扩展性。同时，这样还可以避免模板文件被公开访问。

**3、监控并记录**

此外，需要为用户的每次查询流程生成相应的日志并记录在指定文件中，包括接收到的恶意输入和执行的查询语句，以便在后期分析日志并识别、检查相应的注入攻击行为。在本例中，利用*logging*包来设置并生成日志。如下图日志文件所示，红框表示采集到的用户查询信息，蓝框表示系统所执行的SQL语句。

![log](https://github.com/Rc-W024/SQL-injection/assets/97808991/4011b517-62a8-4719-aa62-c49cda22bbad)

**4、修复及防御**
在反SQL注入中，通常使用参数化查询、预编译语句或ORM框架来防御攻击行为。对于参数化查询，将输入语句的单引号替换为双引号是常见的做法之一：

```python
# replace a single quote with two single quotes
input_str.replace("'","''")
```

这种替换是为了防止用户输入字符串中的单引号干扰SQL查询语句的结构。SQL查询语句通常使用单引号来表示字符串值，如果用户输入的字符串包含单引号且没有进行适当处理，就可能导致查询语句的语法错误或意外行为。攻击者通常会尝试通过在输入中插入单引号来绕过字符串的结束并注入恶意代码，通过替换，可有效防止SQL注入攻击。在本例中，使用了输入验证和过滤的方式实现参数化查询。

![log_defense](https://github.com/Rc-W024/SQL-injection/assets/97808991/05ae59a7-30e9-4a72-bf9d-b8b0fc3e4aa1)

## 注入防御
### 对象关系映射（ORM）
ORM通过将SQL语句中的变量部分（例如查询条件中的参数）与代码分离，来防止SQL注入攻击。ORM工具会将变量部分转换成预编译语句，然后将预编译语句和参数分别发送到数据库中执行。这样可以避免恶意用户通过构造SQL语句来攻击数据库。

本例中，可使用*SQLAlchemy*，是一个流行的Python ORM库，提供了一种安全和方便的方式来与数据库交互。可将`scripts`文件夹中[`ORM.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/ORM.py)提供的模块嵌入到主程序代码中，并只需要在`def query()`部分添加如下语句即可：

```python
# create session object
session=Session()
# execute query
results=session.query(SimData).filter_by(username=filtered_username).first()
```

### SQL Server用户权限最小化
使用[`MinPermissions.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/MinPermissions.py)创建一个只具有执行查看权限的数据库用户，并在连接数据库时使用该用户的凭据，这样可以防止恶意用户在查询中注入恶意代码。另外，可结合使用参数化查询，确保用户输入在查询过程中被视为参数而不是代码的一部分，助于SQL注入攻击的防御。

### 避免动态SQL查询
当系统直接将用户提供的输入内容拼接到查询语句中时，攻击者可利用输入的特殊字符来修改查询逻辑来执行恶意SQL代码，这会导致数据库数据泄露或篡改、非法获取完全访问权限等问题。通过动态构建SQL查询，系统可更容易地过滤和验证用户输入，从而降低SQL注入的风险。

在本例中，使用参数化查询而不是通过字符串拼接动态构建查询语句。在*psycopg2*中，使用`%s`占位符来表示查询参数，并将其作为元组传递给`execute()`。
