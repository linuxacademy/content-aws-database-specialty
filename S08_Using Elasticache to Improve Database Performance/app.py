# /usr/bin/python2.7
import psycopg2
from configparser import ConfigParser
from flask import Flask   

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def fetch(sql):
    # connect to database listed in database.ini
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    # fetch one row
    result = cur.fetchone()
    print('Closing connection to database...')
    cur.close() 
    conn.close()

    return result

def connect():
    """ Connect to the PostgreSQL database server and return a cursor """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # return a conn
        return conn
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

app = Flask(__name__) 
@app.route("/")     
def index():         
    retval = ''
    sql = 'SELECT slow_version();'
    db_result = fetch(sql)
    
    retval = 'DB Version = ' + ''.join(db_result) 
    return retval
if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app
