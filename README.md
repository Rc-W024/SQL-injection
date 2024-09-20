# SQL Injection and Anti-Injection
English | [中文](README_CN.md)

![](https://skillicons.dev/icons?i=py,postgres)

In the field of cybersecurity, SQL injection is a security vulnerability that occurs in the database layer of a Web program, which is the most common and simplest vulnerability in a website. SQL attack-defense is the basis of spatial information security, which can effectively protect the data of GEOINT. In order to study SQL injection, a basic simulation framework based on PostgreSQL injection attack is experimented. In the follow-up, embed simple parameterized queries in web application code to defend against injection.

## Injection Principle
When accessing a dynamic web page, the web server will initiate a SQL query request to the data access layer. If the permission verification is passed, the SQL statement will be executed. In practice, if the data entered by the user is constructed into malicious SQL code, while the Web program does not review the dynamically constructed statement parameters, a security hole will be left.

Currently, the threats of SQL injection mainly include the following situations:

- Infer and decipher the backend database to steal sensitive information from the website.

- Bypass authentication, such as bypassing authentication to log in to the background of the website.

- Inject that uses database stored procedures to perform operations such as privilege escalation.

## Experimental Framework
**1. Create the database table**

Using [`sim_data.sql`](https://github.com/Rc-W024/SQL-injection/blob/main/sim_data.sql) to create a GEOINT table based on PostgreSQL, including `id`, `username`, `password`, and geometry (`geom`) fields, used to store GEOINT information. And 30 cases of data are randomly generated for simulation.

![info](https://github.com/Rc-W024/SQL-injection/assets/97808991/4bf4972f-6508-40ad-b6a1-17ba2ece25c0)

**2. Create the logic script**

Create a simple Web application based on *Flask* framework in Python to implement user input and query logic, including a HTML page. It should be noted that when using *Flask*'s `render_template` function, the program will find in the `templates` folder for an HTML file that matches the specified template name. This convention is to organize and manage the Web template files and separate them from other codes to provide better maintainability and scalability. Futhermore, this also prevents the template files from being publicly accessible.

**3. Monitoring and logging**

In particular, it is necessary to generate a corresponding log for each query process of the user and record it in a specified file, including the received malicious input and the executed query statement, so that the log can be analyzed later and the corresponding injection attack behavior can be identified and checked. In this case, the *logging* package is used to generate the logs.

As shown in the log file in the figure below, the red frame represents the query information collected from the user, and the blue frame represents the SQL statement executed by the system.

![log](https://github.com/Rc-W024/SQL-injection/assets/97808991/4011b517-62a8-4719-aa62-c49cda22bbad)

**4. Repair and defense**
In anti-SQL injection, parameterized queries, prepared statements or ORM framework are usually used to defend against attacks. For parameterized queries, it is one of the common practices to replace single quotes in input statements with double quotes:

```python
# replace a single quote with two single quotes
input_str.replace("'","''")
```

This substitution is to prevent the single quotes in the user input string from interfering with the structure of the SQL query statement. SQL query statements usually use single quotes to represent string values. If the string entered by the user contains single quotes and is not properly processed, it may cause syntax errors or unexpected behavior of the query statement. Attackers usually try to bypass the end of the string and inject malicious code by inserting single quotes in the input. By replacing, SQL injection attacks can be effectively prevented. In this case, parameterized queries are implemented using input validation and filtering.

![log_defense](https://github.com/Rc-W024/SQL-injection/assets/97808991/05ae59a7-30e9-4a72-bf9d-b8b0fc3e4aa1)

## Defense of Injection
### Object–relational mapping (ORM)
ORM prevents SQL injection attacks by separating variable parts of SQL statements such as parameters in query conditions from code. ORM will convert the variable part into a precompiled statement, and then send it and parameters to the database for execution, which can prevent malicious users from attacking the database by constructing SQL statements.

In this case, *SQLAlchemy* can be used, which is a popular Python ORM library that provides a safe and convenient way to interact with databases. The modules provided by [`ORM.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/ORM.py) in the `scripts` folder can be embedded into the main program code, and only need to add the following statement in `def query()`:

```python
# create session object
session=Session()
# execute query
results=session.query(SimData).filter_by(username=filtered_username).first()
```

### Minimize SQL server user permissions
Use [`MinPermissions.py`](https://github.com/Rc-W024/SQL-injection/blob/main/scripts/MinPermissions.py) to create a database user with only execute view permissions, and use the user's credentials when connecting to the database, which prevents malicious users from injecting malicious code in queries. In addition, parameterized query can be used in combination to ensure that user input is treated as a parameter rather than a part of the code during the query process, which is helpful for the defense of SQL injection attacks.

### Avoid dynamic SQL queries
When the system directly splices the input content provided by the user into the query statement, the attacker can use the input special characters to modify the query logic to execute malicious SQL code, which will lead to database data leakage or tampering, and illegal access to full access rights. By dynamically building SQL queries, the system can more easily filter and validate user input, reducing the risk of SQL injection.

In this case, query statements are constructed dynamically using parameterized queries rather than string concatenation. In *psycopg2*, the `%s` placeholder is used to denote query parameters and passed as a tuple to `execute()`.

