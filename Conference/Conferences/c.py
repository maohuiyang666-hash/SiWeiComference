import os

import pymssql


conn = pymssql.connect(
    server=os.getenv('CONFERENCE_DB_HOST', '127.0.0.1'),
    user=os.getenv('CONFERENCE_DB_USER', 'sa'),
    password=os.getenv('CONFERENCE_DB_PASSWORD', ''),
    database=os.getenv('CONFERENCE_DB_NAME', 'test'),
    port=int(os.getenv('CONFERENCE_DB_PORT', '1433')),
)

print("connected")
conn.close()
