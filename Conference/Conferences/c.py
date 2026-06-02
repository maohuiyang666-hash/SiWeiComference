import pymssql

conn = pymssql.connect(
    server='127.0.0.1',
    user='SA',
    password='Iotlab2019@217',
    database='test',
    port=1433  # 明确端口
)

print("连接成功")
conn.close()