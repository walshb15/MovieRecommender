import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
#test = ['3932', 'Invisible Man, The (1933)', 'Horror|Sci-Fi\n']
#testLine = "INSERT into ratings(movieId, title, genre) VALUES(" + test[0] + ",'" + test[1] +"'," + test[2]+" );"
#print(testLine)
database = "C://Users//kirbypar//MovieRecommender//db.sqlite3"
con = create_connection(database)
cursor = con.cursor()
cursor.execute("SELECT * FROM ratings")
print(cursor.fetchall())
#f = open("C:\\Users\\kirbypar\\Desktop\\CSE482\Ml-1m\\ratings.dat")
#for line in f:
#    line = line.replace("\n", "")
#    line = line.split("::")
#    insert = "INSERT into ratings(userid, movieid, rating) VALUES((?), (?), (?))"
#    cursor.execute(insert, (line[0], line[1], line[2]))
#con.commit()
#sql_create_projects_table = """ CREATE TABLE ratings (
#                                    userid integer,
#                                    movieid integer,
#                                    rating integer
#                                ); """
#conn = create_connection(database)
#create_table(conn, sql_create_projects_table)
#con.commit()

