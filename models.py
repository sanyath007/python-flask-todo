import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "todo" (
          id INTEGER PRIMARY KEY,
          title TEXT,
          description TEXT,
          is_done boolean,
          is_deleted boolean,
          created_on Date DEFAULT CURRENT_DATE,
          due_date Date,
          user_id INTEGER FOREIGNKEY REFERENCES user(id)  
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "user" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        created_on DATE DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)


class TodoModel:
    TABLENAME = "todo"

    def __init__(self):
        self.conn = sqlite3.connect("todo.db")

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND (id={_id})"
        return self.list_items(where_clause)

    def create(self, params):
        print(params)
        query = f'INSERT INTO {self.TABLENAME} ' \
                f'(title, description, due_date, user_id) ' \
                f'VALUES ("{params.get("title")}","{params.get("description")}", ' \
                f'"{params.get("due_date")}","{params.get("user_id")}")'
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET is_deleted={1} " \
                f"WHERE (id={item_id}) "
        print(query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, item_id, update_dict):
        """
        column: value
        title: new title
        """
        set_update = " ".join([f'{column} = {value}'
                        for column, value in update_dict.items()])
        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_update} " \
                f"WHERE (id={item_id}) "
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, title, description, due_date, is_done " \
                f"FROM {self.TABLENAME} WHERE is_deleted != {1} " + where_clause

        print(query)
        result_set = self.conn.execute(query).fetchall()
        #result = [{column: row[i] for i, column in enumerate(result_set[0].keys())} for row in result_set]
        result = [row for row in enumerate(result_set)]
        return result_set


class User:
    TABLENAME = "user"

    def create(self, name, email):
        query = f"INSERT INTO {self.TABLENAME} " \
                f"(name, email) " \
                f"VALUES ({name}, {email})"

        result = self.conn.execute(query)
        return result
