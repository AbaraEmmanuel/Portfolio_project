import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS expense_record (item_name TEXT, item_price REAL, purchase_date TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS budget_table (budget REAL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS user (username TEXT PRIMARY KEY, password TEXT)")
        self.conn.commit()

    def user_exists(self, username):
        self.cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        return self.cur.fetchone() is not None

    def add_user(self, username, password):
        self.cur.execute("INSERT INTO user VALUES (?, ?)", (username, password))
        self.conn.commit()

    def insertRecord(self, item_name, item_price, purchase_date):
        self.cur.execute("INSERT INTO expense_record VALUES (?, ?, ?)", (item_name, item_price, purchase_date))
        self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        self.cur.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ? WHERE rowid = ?", (item_name, item_price, purchase_date, rid))
        self.conn.commit()

    def removeRecord(self, rid):
        self.cur.execute("DELETE FROM expense_record WHERE rowid = ?", (rid,))
        self.conn.commit()

    def updateBudget(self, budget):
        self.cur.execute("UPDATE budget_table SET budget = ?", (budget,))
        self.conn.commit()

    def fetchBudget(self):
        self.cur.execute("SELECT budget FROM budget_table")
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def authenticate_user(self, username, password):
        self.cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        return self.cur.fetchone() is not None

    def __del__(self):
        self.conn.close()