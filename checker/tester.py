from .db import Database
from api import models


class Tester:

    def __init__(self, task):
        self.task = task
        self.db = Database(task)

    def select(self, root_sql, user_sql):
        data1 = self.db.select(root_sql)
        try:
            data2 = self.db.select(user_sql)
            print(data2)
            return data1 == data2
        except Exception as e:
            print('User Script Error', e)
            return False

    def execute(self, root_sql, user_sql, table_name):
        self.db.execute(root_sql)
        data1 = self.db.select(f"SELECT * FROM {table_name}")
        try:
            self.db = Database(self.task)
            self.db.execute(user_sql)
            data2 = self.db.select(f"SELECT * FROM {table_name}")
            return data1 == data2
        except Exception as e:
            print('User Script Error', e)
            return False

    def test(self):
        problem = self.task.problem
        if problem.permissions == models.Constants.PERMISSION_SELECT:
            return self.select(problem.answer, self.task.source)
        if problem.permissions == models.Constants.PERMISSION_EXECUTE:
            return self.execute(problem.answer, self.task.source, problem.execute_table)
        return False
