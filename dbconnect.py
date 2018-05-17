import MySQLdb

# mysql --user=root -p
def connection():
    conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="cookies", # your password
                      db="vocabbird") # name of the data base
    c = conn.cursor()

    return c, conn
