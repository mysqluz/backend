from django.db import connections

from . import logger


class Database:
    def __init__(self, task):
        self.problem = task.problem
        self.task = task
        self.down_db()
        self.up_db()

    def up_db(self):
        with connections['user'].cursor() as cursor:
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            logger.debug(tables)
            cursor.execute(self.problem.dump)
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            logger.debug(tables)

    def down_db(self):
        with connections['user'].cursor() as cursor:
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            logger.debug(tables)
            cursor.execute('SET FOREIGN_KEY_CHECKS=0')
            for table in tables:
                logger.debug(f'DROP TABLE `{table[0]}`')
                cursor.execute(f'DROP TABLE `{table[0]}`')
            cursor.execute('SET FOREIGN_KEY_CHECKS=1')
            cursor.execute('SHOW TABLES')
            tables = cursor.fetchall()
            logger.debug(tables)

    def select(self, sql: str):
        with connections['user'].cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    def execute(self, sql: str):
        with connections['user'].cursor() as cursor:
            cursor.execute(sql)
