# connect to PostgreSQL database
conn=psycopg2.connect(
    host="localhost",
    database="postgres",
    user="limited_user", # use a view-only user
    password="XXXXXX"
)