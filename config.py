import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xabB\xc9\x83\xa8:\x17\x1e\xc5sf\xb0\x05\xdc7 '

    SEND_FILE_MAX_AGE_DEFAULT = 0

    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'Broadway_DB'
    MYSQL_CURSORCLASS = 'DictCursor'

    SQLALCHEMY_DATABASE_URI = 'mysql://spurzack:password@localhost:3306/broadway_db'
    # SQLALCHEMY_ECHO = 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    # SQLALCHEMY_ENGINE_OPTIONS = 