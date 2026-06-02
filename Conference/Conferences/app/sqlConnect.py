# -- coding: utf-8 --
from app import conf


class Mssql(object):
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            import pymssql
        except ImportError as exc:
            raise RuntimeError(
                'Missing dependency: pymssql. Install project requirements before using database pages.'
            ) from exc

        self.conn = pymssql.connect(
            server=conf.db_host,
            user=conf.db_user,
            password=conf.db_password,
            database=conf.db_database,
            port=conf.db_port,
            charset=conf.db_charset,
        )
        self.cursor = self.conn.cursor()

    def getItems(self, sql=None, params=None):
        if not sql:
            return []
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
