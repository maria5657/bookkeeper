"""
Модуль описывает репозиторий, работающий в памяти постоянно запоминающего устройства.
"""

from typing import Any
from inspect import get_annotations
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в памяти постоянно запоминающего устройства.
    Хранит данные с помощью СУБД sqlite3.
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls
        self.names = ', '.join(self.fields.keys())
        self.filler = ', '.join("?" * len(self.fields))

    def add(self, obj: T) -> int:
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} ' +
                self.table_types_creator(self.fields)
            )
            cur.execute(
                f'INSERT INTO {self.table_name} ({self.names}) VALUES ({self.filler})',
                values
            )
            pk = cur.lastrowid
        con.close()
        if pk is None:
            raise ValueError
        return pk

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                try:
                    cur.execute(f'SELECT *, rowid FROM {self.table_name}')
                    records = cur.fetchall()
                    result = []
                    for element in records:
                        result.append(self.cls(*element))
                except sqlite3.OperationalError:
                    print('The table probably does not exist. Try to add smth first.')
                    result = []
            con.close()
        else:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                names = ', '.join(where.keys())
                values = "'" + "', '".join(where.values()) + "'"
                try:
                    cur.execute('PRAGMA foreign_keys = ON')
                    cur.execute(
                        f'SELECT *, rowid FROM {self.table_name}' +
                        f' WHERE ({names}) = ({values});'
                    )
                    records = cur.fetchall()
                    result = []
                    for element in records:
                        result.append(self.cls(*element))
                except sqlite3.OperationalError:
                    print('The table probably does not exist. Try to add smth first.')
                    result = []
            con.close()
        return result

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'DELETE FROM {self.table_name} WHERE rowid = {pk}')
                if cur.rowcount == 0:
                    raise KeyError('Unable to delete non-existent object')
            except sqlite3.OperationalError as exc:
                print(exc)
                print('The table probably does not exist. Try to add smth first.')
        con.close()

    def get(self, pk: int) -> T | None:
        result = None
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'SELECT *, rowid FROM {self.table_name}' +
                            f' WHERE rowid = {pk}')
                records = cur.fetchall()
                result = self.cls(*records[0])  # unpack List[Tuple]
            except sqlite3.OperationalError as exc:
                print(exc)
                print('The table probably does not exist. Try to add smth first.')
                result = None
            except IndexError:
                result = None
        con.close()
        return result

    def update(self, obj: T) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            names = ', '.join(self.fields.keys())
            filler = ', '.join("?" * len(self.fields))
            values = [getattr(obj, x) for x in self.fields]
            try:
                cur.execute(
                    f'UPDATE {self.table_name} SET ({names}) = ({filler})' +
                    f'WHERE rowid = {obj.pk}',
                    values
                )
            except sqlite3.OperationalError as exc:
                print(exc)
                print('The record probably does not exist. Try to add smth first.')
            if obj.pk is None:
                raise TypeError
        con.close()

    def delete_all(self) -> None:
        """
        This procedure cleans up the existing database.
        Makes database empty.
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.executescript(f'DROP TABLE IF EXISTS {self.table_name};')
            except sqlite3.OperationalError as exc:
                print(exc)
                print('The table probably does not exist. Try to add smth first.')
        con.close()

    def table_types_creator(self, fields: dict[str, Any]) -> str:
        """
        Converts python data types into sql data type names;
        for use in forming sql queries.
        """
        result = '('
        for key, value in fields.items():
            result += key
            if 'str' in str(value):
                result += ' TEXT'
            if 'int' in str(value):
                result += ' INTEGER'
            if 'datetime' in str(value):
                result += ' DATETIME'
            result += ', '
        return result[:-2] + ')'
