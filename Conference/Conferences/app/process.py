from datetime import date, datetime
from email.mime.text import MIMEText
from html import escape
from types import SimpleNamespace
import smtplib

from werkzeug.security import check_password_hash, generate_password_hash

from app import conf


USER_COLUMNS = {
    'username',
    'password',
    'email',
    'name',
    'phone',
    'member_type',
    'birthday',
    'organization',
    'title',
    'paid',
}

MODEL_COLUMNS = {
    'model_id',
    'model_name',
    'model_author',
    'dataset_id',
    'paper_name',
    'model_url',
    'paper_url',
    'model_time',
    'model_class',
}


def get_connection():
    try:
        import pymssql
    except ImportError as exc:
        raise RuntimeError(
            'Missing dependency: pymssql. Install project requirements before using database pages.'
        ) from exc

    return pymssql.connect(
        server=conf.db_host,
        user=conf.db_user,
        password=conf.db_password,
        database=conf.db_database,
        port=conf.db_port,
        charset=conf.db_charset,
    )


def row_to_namespace(columns, row):
    return SimpleNamespace(**dict(zip(columns, row)))


def normalize_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%Y-%m-%d')
    return value


class DataProcess:
    def _execute_one(self, sql, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            return cursor.fetchone()
        finally:
            conn.close()

    def _execute_write(self, sql, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
        finally:
            conn.close()

    def loginCheck(self, data, key='username'):
        if key not in {'username', 'email'}:
            return False
        sql = f'SELECT username, password FROM users WHERE {key} = %s'
        row = self._execute_one(sql, (data.get('username'),))
        if not row:
            return False
        stored_password = row[1] or ''
        password = data.get('password') or ''
        if stored_password.startswith(('pbkdf2:', 'scrypt:')):
            return check_password_hash(stored_password, password)
        return stored_password == password

    def existCheck(self, data):
        clauses = []
        params = []
        for key, value in data.items():
            if key not in USER_COLUMNS:
                continue
            clauses.append(f'{key} = %s')
            params.append(value)
        if not clauses:
            return True
        sql = 'SELECT TOP 1 username FROM users WHERE ' + ' OR '.join(clauses)
        return self._execute_one(sql, tuple(params)) is None

    def infoChange(self, data, columns, name_transfor, verifys):
        selected_columns = [column for column in columns if column in USER_COLUMNS]
        sql = 'SELECT {} FROM users WHERE username = %s'.format(','.join(selected_columns))
        result = self._execute_one(sql, (data['username'],))
        if not result:
            return ''

        values = {}
        for key, value in zip(selected_columns, result):
            values[key] = normalize_date(value) if value is not None else '无'

        readonly_template = (
            '<div class="signup-form"><label for="{0}">{1}:</label>'
            '<input type="text" id="{0}" class="email-mobile" value="{2}" disabled="disabled"></div>\n'
        )
        editable_template = (
            '<div class="signup-form"><label for="{0}">{1}:</label>'
            '<input type="text" id="{0}" class="email-mobile" value="{2}">'
            '<a class="in_box" onclick="{3}">{4}</a></div>\n'
        )

        html = []
        for key in selected_columns:
            label = escape(name_transfor.get(key, key))
            value = escape(str(values.get(key, '')))
            if columns[key] == 0:
                html.append(readonly_template.format(key, label, value))
            else:
                action_text = '确认修改' if columns[key] == 1 else '修改'
                html.append(editable_template.format(key, label, value, verifys[key], action_text))
        return ''.join(html)

    def register(self, data):
        password_hash = generate_password_hash(data['password'])
        sql = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
        try:
            self._execute_write(sql, (data['username'], password_hash, data['email']))
            return True
        except Exception:
            return False

    def updateInfo(self, data, key='username'):
        if key not in {'username', 'email'} or key not in data:
            return False
        lookup_value = data.pop(key)
        try:
            for column, value in data.items():
                if column not in USER_COLUMNS or value is None or len(str(value)) == 0:
                    return False
                if column == 'password':
                    value = generate_password_hash(value)
                sql = f'UPDATE users SET {column} = %s WHERE {key} = %s'
                self._execute_write(sql, (value, lookup_value))
            return True
        except Exception:
            return False

    def getInfo(self, username, columns, key='email'):
        if key not in {'username', 'email'}:
            return {}
        selected_columns = [column for column in columns if column in USER_COLUMNS]
        sql = 'SELECT {} FROM users WHERE {} = %s'.format(','.join(selected_columns), key)
        result = self._execute_one(sql, (username,))
        if not result:
            return {}
        return {
            column: normalize_date(value) if value is not None else '无'
            for column, value in zip(selected_columns, result)
        }

    def sendEmail(self, receivers, msg):
        if not all([conf.mail_host, conf.mail_user, conf.mail_password, conf.main_sender]):
            return False

        message = MIMEText(msg, 'plain', 'utf-8')
        message['Subject'] = '验证码'
        message['From'] = conf.main_sender
        message['To'] = receivers[0]
        try:
            smtpObj = smtplib.SMTP_SSL(conf.mail_host, 465)
            smtpObj.login(conf.mail_user, conf.mail_password)
            smtpObj.sendmail(conf.main_sender, receivers, message.as_string())
            smtpObj.quit()
            return True
        except smtplib.SMTPException:
            return False


class ModelRepository:
    columns = [
        'model_id',
        'model_name',
        'model_author',
        'dataset_id',
        'paper_name',
        'model_url',
        'paper_url',
        'model_time',
        'model_class',
    ]

    def _fetchall(self, sql, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        finally:
            conn.close()

    def _fetchone(self, sql, params=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            return cursor.fetchone()
        finally:
            conn.close()

    def _rows(self, rows):
        return [row_to_namespace(self.columns, row) for row in rows]

    def find(self, model_class, start, limit):
        sql = (
            f'SELECT * FROM models WHERE model_class = %s '
            f'ORDER BY model_id OFFSET {int(start)} ROWS FETCH NEXT {int(limit)} ROWS ONLY'
        )
        return self._rows(self._fetchall(sql, (model_class,)))

    def find_count(self, model_class):
        row = self._fetchone('SELECT COUNT(*) FROM models WHERE model_class = %s', (model_class,))
        return row[0] if row else 0

    def find_model_detail(self, model_id):
        row = self._fetchone('SELECT * FROM models WHERE model_id = %s', (model_id,))
        return row_to_namespace(self.columns, row) if row else None

    def find_limit(self, keyword1, keyword2, start, limit):
        where, params = self._search_where(keyword1, keyword2)
        sql = (
            f'SELECT * FROM models {where} '
            f'ORDER BY model_id OFFSET {int(start)} ROWS FETCH NEXT {int(limit)} ROWS ONLY'
        )
        return self._rows(self._fetchall(sql, params))

    def find_limit_count(self, keyword1, keyword2):
        where, params = self._search_where(keyword1, keyword2)
        row = self._fetchone(f'SELECT COUNT(*) FROM models {where}', params)
        return row[0] if row else 0

    def _search_where(self, keyword1, keyword2):
        clauses = []
        params = []
        for keyword in [keyword1, keyword2]:
            if keyword:
                clauses.append('(model_name LIKE %s OR model_author LIKE %s OR paper_name LIKE %s)')
                pattern = f'%{keyword}%'
                params.extend([pattern, pattern, pattern])
        if not clauses:
            return '', tuple()
        return 'WHERE ' + ' AND '.join(clauses), tuple(params)
