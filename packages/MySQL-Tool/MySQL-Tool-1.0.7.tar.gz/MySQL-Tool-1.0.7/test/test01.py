
from mysql_tool.mysql_tool import my_mysql
host = "server04"
password = "bestwond2019"
db = my_mysql(host=host, user="root", port=3306, database="gaas", password=password)

sql = "select * from device where device_number=%s;"
data = db.my_fetchone(sql, ['2000000036'], return_type='dict')
print(data)

sql = "select * from device where device_number=%(device_number)s;"
data = db.my_fetchone(sql, {"device_number":'2000000036'}, return_type='dict')
print(data)

