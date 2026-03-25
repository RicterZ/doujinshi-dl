# coding: utf-8
"""DB and Singleton utilities."""
import os
import sqlite3


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton(str('SingletonMeta'), (object,), {})):
    pass


class DB(object):
    conn = None
    cur = None

    def __enter__(self):
        from doujinshi_dl.core import config
        history_path = config.get(
            'history_path',
            os.path.expanduser('~/.doujinshi-dl/history.sqlite3'),
        )
        self.conn = sqlite3.connect(history_path)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS download_history (id text)')
        self.conn.commit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def clean_all(self):
        self.cur.execute('DELETE FROM download_history WHERE 1')
        self.conn.commit()

    def add_one(self, data):
        self.cur.execute('INSERT INTO download_history VALUES (?)', [data])
        self.conn.commit()

    def get_all(self):
        data = self.cur.execute('SELECT id FROM download_history')
        return [i[0] for i in data]
