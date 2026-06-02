import os

from app import app


if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '#'
    host = os.getenv('CONFERENCE_HOST', '127.0.0.1')
    port = int(os.getenv('CONFERENCE_PORT', '5000'))
    debug = os.getenv('CONFERENCE_DEBUG', 'false').lower() in {'1', 'true', 'yes', 'on'}
    app.run(host, port=port, debug=debug)
