import os


# Database: SQL Server
db_host = os.getenv('CONFERENCE_DB_HOST', '127.0.0.1')
db_user = os.getenv('CONFERENCE_DB_USER', 'sa')
db_password = os.getenv('CONFERENCE_DB_PASSWORD', '')
db_database = os.getenv('CONFERENCE_DB_NAME', 'test')
db_port = int(os.getenv('CONFERENCE_DB_PORT', '1433'))
db_charset = os.getenv('CONFERENCE_DB_CHARSET', 'cp936')


# Email verification
mail_host = os.getenv('CONFERENCE_MAIL_HOST', 'smtp.126.com')
mail_user = os.getenv('CONFERENCE_MAIL_USER', '')
mail_password = os.getenv('CONFERENCE_MAIL_PASSWORD', '')
main_sender = os.getenv('CONFERENCE_MAIL_SENDER', mail_user)
