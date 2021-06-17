#########################################
#                                       #
#              GOAT-ORM                 #
#            (VERSION 1.0)              #
#                                       #
#########################################
import inspect
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
    """
    Table operations
    """

    def __init__(self, **kwargs):
        self._data = {"id": None}
        for key, value in kwargs.items():
            self._data[key] = value

    def __get_attribute__(self, key):
        _data = super().__getattribute__("_data")
        if key in _data:
            return _data[key]
        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in self._data:
            self._data[key] = value

    @classmethod
    def _get_create_sql(cls):

        CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(f"{name} {fields.sql_type}")
            elif isinstance(field, ForeignKey):
                fields.append(f"{name}_id INTEGER")

        fields = ",".join(fields)
        name = cls.__name__.lower()
        return CREATE_TABLE_SQL.format(name=name, fields=fields)

    def _get_insert_sql(self):

        INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"
        cls = self.__class__
        fields = []
        placeholders = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
                placeholders.append("?")
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)
                placeholders.append("?")

        fields = ",".join(fields)
        placeholders = ",".join(placeholders)

        sql = INSERT_SQL.format(
            name=cls.__name__.lower(), fields=fields, placeholders=placeholders
        )

        return sql, values

    @classmethod
    def _get_select_all_sql(cls):

        SELECT_ALL_SQL = "SELECT {fields} FROM {name};"

        fields = ["id"]
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")

        sql = SELECT_ALL_SQL.format(name=cls.__name__.lower(), fields=",".join(fields))

    @classmethod
    def get_select_where_sql(cls):

        SELECT_WHERE_SQL = "SELECT {fields} FROM {name} WHERE id= ?;"
        fields = ["id"]

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
            if isinstance(field, ForeignKey):
                fields.append(name + "_id")

        sql = SELECT_WHERE_SQL.format(name=cls.__name.lower(), fields=",".join(fields))
        params = [id]

        return sql, fields, params

    def _get_update_sql(self):
        UPDATE_SQL = "UPDATE {name} SET {fields} WHERE id = ?"
        cls = self.__class__
        fields = []
        values = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values.append(getattr(self, name))
            elif isinstance(field, ForeignKey):
                fields.append(name + "_id")
                values.append(getattr(self, name).id)
        values.append(getattr(self, "id"))

        sql = UPDATE_SQL.format(
            name=cls.__name__.lower(),
            fields=",".join([f"{field} = ?" for field in fields]),
        )

        return sql, values

    def _get_delete_sql(cls, id):
        DELETE_SQL = "DELETE FROM {name} WHERE id = ?"

        sql = DELETE_SQL.format(name=cls.__name__.lower())

        return sql, [id]


class Column:
    """
    Class to store column.
    """

    def __init__(self, column_name):
        self.column_name = column_name

    @property
    def sql_type(self, type):
        SQL_TYPE_MAP = {
            int: "INTEGER",
            float: "FLOAT",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",
        }
        return SQL_TYPE_MAP[self.type]


class ForeignKey:
    """
    Foreignkey relation
    """

    def __init__(self, table):
        self.table = table
