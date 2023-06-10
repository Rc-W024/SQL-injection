from flask import Flask, request, render_template
import psycopg2
from shapely.wkb import loads
import logging
import os

# log file setting
log_directory=r'C:\Users\吴\Desktop\sql\logs'
log_filename='web.log'
log_file_path=os.path.join(log_directory,log_filename)

# check if the path is exit
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# check the write permission
if os.access(log_directory,os.W_OK):
    # log setting
    logging.basicConfig(filename=log_file_path,level=logging.INFO)
    logger=logging.getLogger(__name__)
else:
    print(f'No write permission to directory: {log_directory}')

######MAIN######

app=Flask(__name__)

def connect_to_db():
    try:
        psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="padxzmvm"
        )
        logging.info('Connected!')
        #return conn
    except psycopg2.Error as e:
        logging.error('Unable to connect to database!')
        raise e

# connect to PostgreSQL database
conn=psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="padxzmvm"
        )
    
# desconnecting...
def disconnect_from_db(conn):
    conn.close()
    logging.info('Desconnected!')

# mainpage
@app.route('/')
def index():
    return render_template('index.html')
    
######SQL######

# handle user input and execute queries
@app.route('/query',methods=['POST'])
def query():
    if request.method=='POST':
        # obtain usern and pswd
        username=request.form['username']
        password=request.form['password']
        logging.info(f'Query request - Original enter - Username: {username}, Password: {password}')

        # filtering & validation
        filtered_username=filter_input(username)
        filtered_password=filter_input(password)
        logging.info(f'Query request - Username: {filtered_username}, Password: {filtered_password}')

        # execute queries
        cursor=conn.cursor()
        query="SELECT * FROM sim_data WHERE username = %s"
        complete_query=cursor.mogrify(query,(filtered_username,))
        logging.info(f'System query - SQL: {complete_query.decode()}')
        #logging.info(f'System query - SQL: {query}')
        cursor.execute(query,(filtered_username,))
        results=cursor.fetchall()
        cursor.close()
        logging.info(f'Query executed successfully')

        if results:
            result=results[0]
            # validation
            if result[2]==filtered_password:
                geom=result[3]
                # parsing geometry data
                point=loads(geom)
                # obtain the coordinates
                coord=point.coords
                # convert to readable coordinate form
                readable_coord=", ".join(f"{x:.2f}, {y:.2f}" for x,y in coord)
                logging.info(f'Query result - Geometry: {geom}')
                return render_template('index.html',geom=readable_coord)
            else:
                error_message="Wrong password!"
                logging.warning(f'Query result - {error_message}')
                return render_template('index.html',error=error_message)
        else:
            error_message="User does not exist!"
            logging.warning(f'Query result - {error_message}')
            return render_template('index.html',error=error_message)
    else:
        return render_template('index.html')

######DEFENSE######

# filter user input
def filter_input(input_str):
    # use parameterized queries to prevent SQL injection
    filtered_str=input_str.replace("'","''") # replace a single quote with two single quotes
    return filtered_str

if __name__=='__main__':
    app.run(debug=True)
