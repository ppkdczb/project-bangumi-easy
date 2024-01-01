HOSTNAME = "localhost"
PORT = '3306'
DATABASE = "anime"
USERNAME = "root"
PASSWORD = "123456"
DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
