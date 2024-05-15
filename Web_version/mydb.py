import sqlite3
from flask import g

class Database:
    def __init__(self, db):
        self.db = db

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.db)
        return db

    def close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def fetchRecord(self, query):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
        cur.close()
        return records

    def fetchBudget(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT budget FROM budget_table")
        result = cur.fetchone()
        cur.close()
        if result:
            return result[0]
        else:
            return 0

    def insertRecord(self, item_name, item_price, purchase_date):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO expense_record VALUES (?, ?, ?)", (item_name, item_price, purchase_date))
        conn.commit()
        cur.close()

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ? WHERE rowid = ?", (item_name, item_price, purchase_date, rid))
        conn.commit()
        cur.close()

    def removeRecord(self, rid):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM expense_record WHERE rowid = ?", (rid,))
        conn.commit()
        cur.close()

    def insertBudget(self, budget):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO budget_table (budget) VALUES (?)", (budget,))
        conn.commit()
        cur.close()

    def updateBudget(self, budget):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("UPDATE budget_table SET budget = ?", (budget,))
        conn.commit()
        cur.close()

    def authenticate_user(self, username, password):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        result = cur.fetchone()
        cur.close()
        return result is not None

    def add_user(self, username, password):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO user VALUES (?, ?)", (username, password))
        conn.commit()
        cur.close()


    def saveBudget(self, budget):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT budget FROM budget_table")
        result = cur.fetchone()
        if result:
            cur.execute("UPDATE budget_table SET budget = ?", (budget,))
        else:
            cur.execute("INSERT INTO budget_table (budget) VALUES (?)", (budget,))
        conn.commit()
        cur.close()