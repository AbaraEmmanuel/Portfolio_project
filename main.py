from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from datetime import date
from mydb import Database

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Spendwise - Portfolio project')

        # Create database object
        self.data = Database(db='myexpense.db')

        # Initialize budget
        self.budget = self.data.fetchBudget()  # Fetch budget from the database

        # Frame widgets
        self.f1 = Frame(
            root,
            padx=10,
            pady=10,
        )
        self.f1.pack(expand=True, fill=BOTH)

        # Label Widget
        Label(self.f1, text='ITEM NAME').grid(row=0, column=0, sticky=W)
        Label(self.f1, text='ITEM PRICE').grid(row=1, column=0, sticky=W)
        Label(self.f1, text='PURCHASE DATE').grid(row=2, column=0, sticky=W)

        # Entry Widgets
        self.item_name = Entry(self.f1)
        self.item_amt = Entry(self.f1)
        self.transaction_date = Entry(self.f1)

        # Entry grid placement
        self.item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
        self.item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
        self.transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

        # Action buttons
        self.cur_date = Button(
            self.f1,
            text='Current Date',
            bg='#04C4D9',
            command=self.set_date,
            width=15
        )

        self.submit_btn = Button(
            self.f1,
            text='Save Record',
            command=self.save_record,
            bg='#42602D',
            fg='white'
        )

        self.clear_btn = Button(
            self.f1,
            text='Clear Entry',
            command=self.clear_entries,
            bg='#D9B036',
            fg='white'
        )

        self.update_btn = Button(
            self.f1,
            text='Update',
            command=self.update_record,
            bg='#C2BB00',
            fg='white'
        )

        self.delete_btn = Button(
            self.f1,
            text='Delete',
            command=self.delete_record,
            bg='#BD2A2E',
            fg='white'
        )

        self.exit_btn = Button(
            self.f1,
            text='Exit',
            command=self.on_exit,
            bg='#D33532',
            fg='white'
        )

        self.total_bal_btn = Button(
            self.f1,
            text='Total Balance',
            command=self.show_total_balance,
            bg='#486966',
            fg='white'
        )

        self.budget_btn = Button(
            self.f1,
            text='Set Budget',
            command=self.set_budget,
            bg='#0066ff',
            fg='white'
        )

        # Button grid placement
        self.cur_date.grid(row=3, column=0, sticky=EW, padx=(10, 0))
        self.submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
        self.clear_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
        self.update_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
        self.delete_btn.grid(row=3, column=2, sticky=EW, padx=(10, 0))
        self.exit_btn.grid(row=4, column=2, sticky=EW, padx=(10, 0))
        self.total_bal_btn.grid(row=4, column=0, sticky=EW, padx=(10, 0))
        self.budget_btn.grid(row=5, column=0, sticky=EW, padx=(10, 0))

        # New "Save" button
        self.save_btn = Button(
            self.f1,
            text='Save',
            command=self.save_data,
            bg='#FFA500',
            fg='white'
        )
        self.save_btn.grid(row=5, column=2, sticky=EW, padx=(10, 0))

        # Reset button
        self.reset_btn = Button(
            self.f1,
            text='Reset',
            command=self.reset_application,
            bg='#FF6347',
            fg='white'
        )
        self.reset_btn.grid(row=5, column=1, sticky=EW, padx=(10, 0))

        # Treeview to view the record
        self.tv = ttk.Treeview(root, selectmode='browse', columns=(1, 2, 3, 4), show='headings', height=8)
        self.tv.pack(side="left")

        self.tv.column(1, anchor=CENTER, stretch=NO, width=70)
        self.tv.column(2, anchor=CENTER)
        self.tv.column(3, anchor=CENTER)
        self.tv.column(4, anchor=CENTER)
        self.tv.heading(1, text="Serial no")
        self.tv.heading(2, text="Item Name")
        self.tv.heading(3, text="Item Price")
        self.tv.heading(4, text="Purchase Date")

        self.scrollbar = Scrollbar(root, orient='vertical')
        self.scrollbar.configure(command=self.tv.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tv.config(yscrollcommand=self.scrollbar.set)

        # Fetch and display records
        self.fetch_records()

        # Bind select record function
        self.tv.bind("<ButtonRelease-1>", self.select_record)

    def set_date(self):
        # Set current date to transaction_date entry
        self.transaction_date.delete(0, END)
        self.transaction_date.insert(END, date.today().strftime("%Y-%m-%d"))

    def save_record(self):
        # Fetch values from entries
        item_name = self.item_name.get()
        item_price = float(self.item_amt.get())
        purchase_date = self.transaction_date.get()

        # Check if the total expense exceeds the budget
        total_expense_row = self.data.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
        total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0
        if total_expense + item_price > self.budget:
            messagebox.showwarning('Budget Exceeded', f'The total expense will exceed the monthly budget of {self.budget}.')
        else:
            # Insert record into database
            self.data.insertRecord(item_name=item_name, item_price=item_price, purchase_date=purchase_date)

            # Update the budget in the database
            self.budget -= item_price  # Deduct item_price from budget
            self.data.updateBudget(self.budget)

            # Refresh record list
            self.fetch_records()

            # Clear entries after saving
            self.clear_entries()

    def fetch_records(self):
        # Clear existing records
        for item in self.tv.get_children():
            self.tv.delete(item)

        # Fetch records from database and display in Treeview
        records = self.data.fetchRecord('SELECT rowid, * FROM expense_record')
        for rec in records:
            self.tv.insert(parent='', index='end', values=(rec[0], rec[1], rec[2], rec[3]))

    def select_record(self, event):
        # Get selected record from Treeview
        selected_item = self.tv.selection()[0]
        record_values = self.tv.item(selected_item, 'values')

        # Update entry fields with selected record values
        self.selected_rowid = record_values[0]
        self.item_name.delete(0, END)
        self.item_name.insert(END, record_values[1])
        self.item_amt.delete(0, END)
        self.item_amt.insert(END, record_values[2])
        self.transaction_date.delete(0, END)
        self.transaction_date.insert(END, record_values[3])

    def clear_entries(self):
        # Clear entry fields
        self.item_name.delete(0, END)
        self.item_amt.delete(0, END)
        self.transaction_date.delete(0, END)

    def update_record(self):
        # Fetch values from entries
        item_name = self.item_name.get()
        item_price = float(self.item_amt.get())
        purchase_date = self.transaction_date.get()

        # Update record in database
        self.data.updateRecord(item_name=item_name, item_price=item_price, purchase_date=purchase_date, rid=self.selected_rowid)

        # Refresh record list
        self.fetch_records()

        # Clear entries after updating
        self.clear_entries()

    def delete_record(self):
        # Delete selected record from database
        self.data.removeRecord(self.selected_rowid)

        # Refresh record list
        self.fetch_records()

    def show_total_balance(self):
        # Fetch total expense from database
        total_expense_row = self.data.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0]
        total_expense = total_expense_row[0] if total_expense_row[0] is not None else 0

        # Fetch monthly budget from database each time the method is called
        monthly_budget = self.data.fetchBudget()

        # Calculate balance correctly
        total_balance = monthly_budget - total_expense
        total_balance = max(total_balance, 0)  # Ensure balance doesn't go below 0

        messagebox.showinfo('Total Balance', f'Monthly Budget: {monthly_budget}\nTotal Expense: {total_expense}\nBalance Remaining: {total_balance}')

    def set_budget(self):
        # Prompt user to set monthly budget
        budget = simpledialog.askfloat("Set Monthly Budget", "Enter the monthly budget: ")
        if budget is not None:
            self.budget = budget
            self.data.updateBudget(self.budget)  # Update budget in the database
            messagebox.showinfo('Budget Set', f'Monthly budget set to {budget}')

    def save_data(self):
        # Save budget
        self.data.updateBudget(self.budget)
        messagebox.showinfo('Save', 'Data saved successfully!')

    def reset_application(self):
        # Reset all entries, budget, and history
        self.clear_entries()
        self.budget = 0
        self.data.updateBudget(self.budget)  # Update budget in the database
        self.data.removeRecord('DELETE FROM expense_record')

    def on_exit(self):
        if self.root.winfo_exists():
            if self.data.fetchBudget() != self.budget or self.data.fetchRecord('SELECT COUNT(*) FROM expense_record')[0][0] > 0:
                if messagebox.askyesno('Exit', 'Do you want to save before exiting?'):
                    self.save_data()
                    self.root.destroy()
                else:
                    self.root.destroy()
            else:
                self.root.destroy()



class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")  # Set the size of the login window

        self.data = Database(db='myexpense.db')

        self.username_label = Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = Entry(root)
        self.username_entry.pack()

        self.password_label = Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = Button(root, text="Login", command=self.login)
        self.login_button.pack()

        self.signup_button = Button(root, text="Sign Up", command=self.signup)
        self.signup_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.data.authenticate_user(username, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.root.destroy()
            self.app = ExpenseApp(Tk())
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and password are required")
            return
        if self.data.user_exists(username):
            messagebox.showerror("Sign Up Failed", "Username already exists")
            return
        self.data.add_user(username, password)
        messagebox.showinfo("Sign Up Successful", "User registered successfully")


# Create main window
root = Tk()
login_window = LoginWindow(root)
root.mainloop()
