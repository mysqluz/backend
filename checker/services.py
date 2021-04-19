import os

from django.conf import settings
from django.db import connection

from api.models import Problem


def import_from_sql_file(problem: Problem):
    cursor = connection.cursor()
    filename = f"{problem.dump_file}"
    print(filename)
    if not os.path.exists(filename):
        return False
    with open(filename) as f:
        return cursor.execute(f.read())


def select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def delete(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
