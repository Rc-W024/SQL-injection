# SQL Injection and Anti-Injection
In the field of cybersecurity, SQL injection is a security vulnerability that occurs in the database layer of a Web program, and it is the most common and simplest vulnerability in a website. This is the basis of spatial information security, which can effectively protect GEOINT data. In order to study SQL injection, a basic simulation framework based on PostgreSQL injection attack is experimented. Finally, embed simple parameterized queries in web application code to prevent SQL injection behavior.

在网络空间安全领域，SQL注入是发生在Web程序中数据库层的安全漏洞，是网站存在最多、也是最简单的漏洞。SQL攻防是空间信息安全的基础，可有效保护空间情报数据。为了学习、研究SQL注入，本项目仿真了一个基于PostgreSQL注入攻击的基本框架。最后，在Web程序代码中嵌入简单的参数化查询来防止SQL注入行为。

## Injection Principle
When accessing a dynamic web page, the web server will initiate a SQL query request to the data access layer. If the permission verification is passed, the SQL statement will be executed. In practice, if the data entered by the user is constructed into malicious SQL code, and the Web program does not review the dynamically constructed statement parameters, a security hole will be left.

当访问动态网页时，Web服务器会向数据访问层发起SQL查询请求。如果权限验证通过就会执行SQL语句。在实际中，如果用户输入的数据被构造成恶意SQL代码，Web程序又未对动态构造的语句参数进行审查，就会留下安全漏洞。当前，SQL注入的威胁主要有如下情况：

Currently, the threats of SQL injection mainly include the following situations:

- Guess the background database to steal sensitive information from the website.<br>
猜解后台数据库以盗取网站的敏感信息

- Bypass authentication, such as bypassing authentication to log in to the background of the website.<br>
绕过认证，如绕过验证登录网站后台

- Inject that uses database stored procedures to perform operations such as privilege escalation.<br>
注入可借助数据库的存储过程进行提权等操作的恶意代码

## Experimental Framework
**1. Create the database table**

Using [`sim_data.sql`](https://github.com/Rc-W024/SQL-injection/blob/main/sim_data.sql) to create a GEOINT table based on PostgreSQL, including `id`, `username`, `password`, and geometry (`geom`) fields, used to store GEOINT information.

基于PostgreSQL，使用[`sim_data.sql`](https://github.com/Rc-W024/SQL-injection/blob/main/sim_data.sql)示例代码创建一个空间情报信息表，包含`id`、`username`、`password`和`geom`字段，用于存储情报信息。

30 cases of GEOINT are randomly generated for simulation.

随机生成30组情报信息进行仿真。

![info](https://github.com/Rc-W024/SQL-injection/assets/97808991/4bf4972f-6508-40ad-b6a1-17ba2ece25c0)

**2. Create the logic script**

Create a simple Web application based on *Flask* framework in Python to implement user input and query logic, including a HTML page. It should be noted that when using *Flask*'s `render_template` function, the program will find in the `templates` folder for an HTML file that matches the specified template name. This convention is to organize and manage the Web template files and separate them from other codes to provide better maintainability and scalability. Futhermore, this also prevents the template files from being publicly accessible.

创建一个简单的基于Python *Flask*框架的Web应用程序，以实现用户输入、查询逻辑，其中包含了一个用于可视化的HTML页面。需要注意的是，当使用*Flask*的`render_template`函数时，程序会在 `templates`文件夹中查找与指定模板名称匹配的HTML文件。这种约定是为了组织和管理Web的模板文件，使其与其他代码分离，以提供更好的可维护性和扩展性。同时，这样还可以避免模板文件被公开访问。

**3. Monitoring and logging**

In particular, it is necessary to generate a corresponding log for each query process of the user and record it in a specified file, including the received malicious input and the executed query statement, so that the log can be analyzed later and the corresponding injection attack behavior can be identified and checked. In this case, the *logging* package is used to generate the logs.

As shown in the log file in the figure below, the red frame represents the query information collected from the user, and the blue frame represents the SQL statement executed by the system.

此外，需要为用户的每次查询流程生成相应的日志并记录在指定文件中，包括接收到的恶意输入和执行的查询语句，以便在后期分析日志并识别、检查相应的注入攻击行为。在本例中，利用*logging*包来设置并生成日志。如下图日志文件所示，红框表示采集到用户的查询信息，蓝框表示系统所执行的SQL语句。

![log](https://github.com/Rc-W024/SQL-injection/assets/97808991/f1ebcc9b-e2d4-4def-980b-3e1503bdcf51)

**4. Repair and defense**
In anti-SQL injection, parameterized queries, prepared statements or ORM framework are usually used to defend against attacks. For parameterized queries, it is one of the common practices to replace single quotes in input statements with double quotes:

```python
# replace a single quote with two single quotes
input_str.replace("'","''")
```

This substitution is to prevent the single quotes in the user input string from interfering with the structure of the SQL query statement. SQL query statements usually use single quotes to represent string values. If the string entered by the user contains single quotes and is not properly processed, it may cause syntax errors or unexpected behavior of the query statement. Attackers usually try to bypass the end of the string and inject malicious code by inserting single quotes in the input. By replacing, SQL injection attacks can be effectively prevented. In this case, parameterized queries are implemented using input validation and filtering.

在反SQL注入中，通常使用参数化查询、预编译语句或ORM框架来防御攻击行为。对于参数化查询，将输入语句的单引号替换为双引号是一种常见的做法之一。这种替换是为了防止用户输入字符串中的单引号干扰SQL查询语句的结构。SQL查询语句通常使用单引号来表示字符串值，如果用户输入的字符串包含单引号且没有进行适当处理，就可能导致查询语句的语法错误或意外行为。攻击者通常会尝试通过在输入中插入单引号来绕过字符串的结束并注入恶意代码，通过替换，可有效防止SQL注入攻击。在本例中，使用了输入验证和过滤的方式实现参数化查询。

![log_defense](https://github.com/Rc-W024/SQL-injection/assets/97808991/05ae59a7-30e9-4a72-bf9d-b8b0fc3e4aa1)

## Defense of Injection
### Object–relational mapping (ORM)
ORM prevents SQL injection attacks by separating variable parts of SQL statements, such as parameters in query conditions, from code. ORM will convert the variable part into a precompiled statement, and then send it and parameters to the database for execution, which can prevent malicious users from attacking the database by constructing SQL statements.

ORM通过将SQL语句中的变量部分（例如查询条件中的参数）与代码分离，来防止SQL注入攻击。ORM工具会将变量部分转换成预编译语句，然后将预编译语句和参数分别发送到数据库中执行。这样可以避免恶意用户通过构造SQL语句来攻击数据库。

In this case, *SQLAlchemy* can be used, which is a popular Python ORM library that provides a safe and convenient way to interact with databases. The modules provided by [`ORM.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/ORM.py) in the `scripts` folder can be embedded into the main program code, and only need to add the following statement in `def query()`:

本例中，可使用*SQLAlchemy*，是一个流行的Python ORM库，提供了一种安全和方便的方式来与数据库交互。可将`scripts`文件夹中[`ORM.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/ORM.py)提供的模块嵌入到主程序代码中，并只需要在`def query()`部分添加如下语句即可：

```python
# create session object
session=Session()
# execute query
results=session.query(SimData).filter_by(username=filtered_username).first()
```

### Minimize SQL server user permissions
Use [`MinPermissions.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/MinPermissions.py) to create a database user with only execute view permissions, and use the user's credentials when connecting to the database, which prevents malicious users from injecting malicious code in queries. In addition, parameterized query can be used in combination to ensure that user input is treated as a parameter rather than a part of the code during the query process, which is helpful for the defense of SQL injection attacks.

使用[`MinPermissions.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/MinPermissions.py)创建一个只具有执行查看权限的数据库用户，并在连接数据库时使用该用户的凭据，这样可以防止恶意用户在查询中注入恶意代码。另外，可结合使用参数化查询，确保用户输入在查询过程中被视为参数而不是代码的一部分，助于SQL注入攻击的防御。

### Avoid dynamic SQL queries
When the system directly splices the input content provided by the user into the query statement, the attacker can use the input special characters to modify the query logic to execute malicious SQL code, which will lead to database data leakage or tampering, and illegal access to full access rights. By dynamically building SQL queries, the system can more easily filter and validate user input, reducing the risk of SQL injection.

当系统直接将用户提供的输入内容拼接到查询语句中时，攻击者可利用输入的特殊字符来修改查询逻辑来执行恶意SQL代码，这会导致数据库数据泄露或篡改、非法获取完全访问权限等问题。通过动态构建SQL查询，系统可更容易地过滤和验证用户输入，从而降低SQL注入的风险。

In this case, query statements are constructed dynamically using parameterized queries rather than string concatenation. In *psycopg2*, the `%s` placeholder is used to denote query parameters and passed as a tuple to `execute()`.

在本例中，使用参数化查询而不是通过字符串拼接动态构建查询语句。在*psycopg2*中，使用`%s`占位符来表示查询参数，并将其作为元组传递给`execute()`。
