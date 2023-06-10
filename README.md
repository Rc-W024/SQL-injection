# SQL Injection and Anti-Injection
In the field of cybersecurity, SQL injection is a security vulnerability that occurs in the database layer of a Web program, and it is the most common and simplest vulnerability in a website. This is the basis of spatial information security, which can effectively protect GEOINT data. In order to study SQL injection, a basic simulation framework based on PostgreSQL injection attack is experimented. Finally, embed simple parameterized queries in web application code to prevent SQL injection behavior.

在网络空间安全领域，SQL注入是发生在Web程序中数据库层的安全漏洞，是网站存在最多也是最简单的漏洞。这是空间信息安全的基础，可有效保护空间情报数据。为了学习、研究SQL注入，本项目仿真了一个基于PostgreSQL注入攻击的基本框架。最后，在Web程序代码中嵌入简单的参数化查询来防止SQL注入行为。

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
In anti-SQL injection, parameterized queries, prepared statements or ORM frameworks are usually used to defend against attacks. For parameterized queries, it is one of the common practices to replace single quotes in input statements with double quotes:

```python
# replace a single quote with two single quotes
input_str.replace("'","''")
```

This substitution is to prevent the single quotes in the user input string from interfering with the structure of the SQL query statement. SQL query statements usually use single quotes to represent string values. If the string entered by the user contains single quotes and is not properly processed, it may cause syntax errors or unexpected behavior of the query statement. Attackers usually try to bypass the end of the string and inject malicious code by inserting single quotes in the input. By replacing, SQL injection attacks can be effectively prevented.

在反SQL注入中，通常使用参数化查询、预编译语句或ORM框架来防御攻击行为。对于参数化查询，将输入语句的单引号替换为双引号是一种常见的做法之一。这种替换是为了防止用户输入字符串中的单引号干扰SQL查询语句的结构。SQL查询语句通常使用单引号来表示字符串值，如果用户输入的字符串包含单引号且没有进行适当处理，就可能导致查询语句的语法错误或意外行为。攻击者通常会尝试通过在输入中插入单引号来绕过字符串的结束并注入恶意代码，通过替换，可有效防止SQL注入攻击。

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

### A
