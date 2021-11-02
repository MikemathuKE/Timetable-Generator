import sqlite3
from sqlite3 import Error


class Column:
    id: int
    name: str
    type: str
    not_null: bool
    default_value: str
    primary_key: bool

    def __init__(self, id_, name, type_, not_null, default_value, primary_key):
        self.id = id_
        self.name = name
        self.type = type_
        self.not_null = not_null
        self.default_value = default_value
        self.primary_key = primary_key


class Table:
    name: str

    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.columns = {}

        try:
            command = "PRAGMA table_info(" + self.name + ")"
            cur = self.db.cursor()
            cur.execute(command)

            cols = cur.fetchall()
            for col in cols:
                self.columns[col[1]] = Column(col[0], col[1], col[2], col[3], col[4], col[5])
        except Error as e:
            print(e)

    def get_columns(self):
        return self.columns

    def select_record(self, columns, conditions):
        """
        select data from table
        :param columns: name of fields
        :param conditions: conditions for selection
        :return:
        """
        command = "SELECT " + columns + " FROM " + self.name
        if not conditions == None:
            command += " WHERE " + conditions

        try:
            cur = self.db.cursor()
            cur.execute(command)
            records = cur.fetchall()
            return records
        except Error as e:
            print(e)

    def update_record(self, updates, conditions):
        """
        update the current table
        :param updates: new values to be set
        :param conditions: set of conditions for setting updates
        :return:
        """
        command = "UPDATE " + self.name + " SET " + updates + " WHERE " + conditions

        try:
            cur = self.db.cursor()
            cur.execute(command)
            self.db.commit()
        except Error as e:
            print(e)

    def insert_record(self, attributes, values):
        """
        update the current table
        :param attributes: bracket enclosed attributes that are to be changed in order
        :param values: bracket enclosed values assigned to attributes in order
        :return:
        """
        command = "INSERT INTO " + self.name + " " + attributes + " VALUES " + values

        try:
            cur = self.db.cursor()
            cur.execute(command)
            self.db.commit()
        except Error as e:
            print(e)

    def delete_record(self, conditions):
        """
        update the current table
        :param conditions: conditions that will qualify deletion
        :return:
        """
        command = "DELETE FROM " + self.name + " WHERE " + conditions

        try:
            cur = self.db.cursor()
            cur.execute(command)
            self.db.commit()
        except Error as e:
            print(e)

    def add_column(self, name, definition):
        """
        add a column to the tables
        :param name: name of new column
        :param definition: defining attributes of new column
        :return:
        """
        command = "ALTER TABLE " + self.name + " ADD COLUMN " + name + " " + definition

        try:
            cur = self.db.cursor()
            cur.execute(command)
            self.db.commit()
        except Error as e:
            print(e)

    def rename_column(self, name, new_name):
        """
        add a column to the tables
        :param name: name of column to be changed
        :param new_name: new name of column
        :return:
        """
        command = "ALTER TABLE " + self.name + " RENAME COLUMN " + name + " TO " + new_name

        try:
            cur = self.db.cursor()
            cur.execute(command)
            self.db.commit()
        except Error as e:
            print(e)


class Database:
    db: sqlite3.Connection
    table = dict()
    active: str

    def __init__(self, db_file):
        """
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return:
        """
        try:
            self.db = sqlite3.connect(db_file)
            self.active = ""
            cur = self.db.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            list_tables = cur.fetchall()
            for t in list_tables:
                tb_name = str(t)
                tb_name = tb_name.replace("('", "")
                tb_name = tb_name.replace("',)", "")
                if tb_name == "sqlite_sequence":
                    continue
                self.table[tb_name] = Table(self.db, tb_name)
        except Error as e:
            print(e)

    def setActiveTable(self, name):
        self.active = name

    def create_table(self, table_name, fields):
        """
        create a table and add to the SQLite database
        specified by the self.db
        :param table_name: name of table
        :param fields: definition of fields in sqlite format
        :return:
        """
        command = "CREATE TABLE IF NOT EXISTS'" + table_name + "'(" + fields + ");"

        try:
            self.db.execute(command)
            self.table[table_name] = Table(self.db, table_name)
        except Error as e:
            print(e)

    def delete_table(self, table_name):
        """
        delete a table from the SQLite database
        :param table_name: name of table
        :return:
        """
        command = "DROP TABLE IF EXISTS'" + table_name + "'"

        try:
            self.db.execute(command)
            try:
                del self.table[table_name]
            except KeyError:
                pass
        except Error as e:
            print(e)

    def rename_table(self, table_name, new_name):
        """
        Change table column attributes
        :param table_name: current name of table
        :param new_name: new name of table
        :command: Command of Alteration
        """
        command = "ALTER TABLE " + table_name + " RENAME TO " + new_name

        try:
            self.db.execute(command)
            self.table[new_name] = self.table[table_name].pop()
        except Error as e:
            print(e)

    def has_table(self, table_name):
        """
        Check if table exists in SQLite database
        :param table_name: name of table
        :return: True if table exists in database, False otherwise
        """
        if table_name in self.table.keys():
            return True
        return False
