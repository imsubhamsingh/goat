#########################################
#                                       #
#              GOAT-ORM                 #
#            (VERSION 1.0)              #
#                                       #
#########################################

import sqlite3


class Database:
    def __init__(self, path):
        self.connection = sqlite3.Connection(path)

    def tables(self):
        pass

    def create_table(self):
        pass

    def save(self):
        pass

    def all(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class Table:
    def get_attributes(self):
        pass

    def set_attributes(self):
        pass

    def insert_sql(self):
        pass

    def select_sql(self):
        pass

    def select_all_sql(self):
        pass

    def select_where_sql(self):
        pass

    def update_sql(self):
        pass

    def delete_sql(self):
        pass


class Column:
    """
    Class to store column.
    """

    def __init__(self, column_name):
        self.column_name = column_name


class ForeignKey:
    """
    Foreignkey relation
    """

    def __init__(self, table):
        self.table = table
