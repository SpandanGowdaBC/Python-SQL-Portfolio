import sqlite3


# --- MAIN SYSTEM CLASS ---
class LeaveManager:
    def __init__(self, db_name="company_db.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.max_cap = 30  # Business Rule: Max 30 days
        self.setup_database()

    def setup_database(self):
        # 1. Create Table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT,
                balance INTEGER
            )
        """
        )

        # 2. Seed Initial Data (Only if empty)
        self.cursor.execute("SELECT count(*) FROM employees")
        if self.cursor.fetchone()[0] == 0:
            print("⚙️ Initializing Database with Staff...")
            staff = [
                (101, "Alice", 12),
                (102, "Bob", 29),  # Close to cap
                (103, "Charlie", 5),  # Low balance
                (104, "Diana", 0),  # No balance
            ]
            self.cursor.executemany("INSERT INTO employees VALUES (?, ?, ?)", staff)
            self.conn.commit()

    def add_employee(self, emp_id, name, balance):
        try:
            # SQL INSERT (Replaces dictionary assignment)
            self.cursor.execute(
                "INSERT INTO employees VALUES (?, ?, ?)", (emp_id, name, balance)
            )
            self.conn.commit()
            print(f"✅ Employee Added: {name}")
        except sqlite3.IntegrityError:
            print(f"⚠️ Error: Employee ID {emp_id} already exists in Database!")

    def show_all_employees(self):
        print("\n--- 📋 COMPANY ROSTER (SQL) ---")
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        for r in rows:
            print(f"🆔 {r[0]} | 👤 {r[1]} | 🏖️ Balance: {r[2]}")
        print("-------------------------------")

    def apply_for_leave(self, emp_id, days_requested):
        # 1. Fetch current balance from SQL
        self.cursor.execute(
            "SELECT name, balance FROM employees WHERE emp_id=?", (emp_id,)
        )
        result = self.cursor.fetchone()

        if not result:
            print("❌ Error: Employee not found!")
            return

        name, current_balance = result

        # 2. Validation Logic
        if days_requested <= 0:
            print("❌ Error: Invalid days.")
            return

        # 3. Check Balance & Update
        if current_balance >= days_requested:
            new_balance = current_balance - days_requested

            # SQL UPDATE
            self.cursor.execute(
                "UPDATE employees SET balance=? WHERE emp_id=?", (new_balance, emp_id)
            )
            self.conn.commit()

            print(f"✅ APPROVED: {name} took {days_requested} days.")
            print(f"   📉 New Balance: {new_balance} days.")
        else:
            print(
                f"🚫 DENIED: {name} requested {days_requested}, but has only {current_balance}."
            )

    def end_of_month_rollover(self):
        print("\n📅 --- RUNNING AUTOMATED ROLLOVER ---")

        # --- PRO DEVELOPER MOVE ---
        # Instead of looping in Python (slow), we use SQL Math (fast).
        # Logic: "Set balance = balance + 2, but do not exceed 30."

        self.cursor.execute(
            f"""
            UPDATE employees 
            SET balance = MIN(balance + 2, {self.max_cap})
        """
        )
        self.conn.commit()

        print("✅ SQL BATCH PROCESS COMPLETE.")
        print("   -> All employees received +2 days.")
        print(f"   -> Caps enforced at {self.max_cap} days.")


# --- EXECUTION ---
system = LeaveManager()

while True:
    print(
        "\n1. Apply Leave   2. View Roster   3. Add Employee   4. Simulate Month End   5. Exit"
    )
    choice = input("Enter Choice: ")

    if choice == "1":
        try:
            e_id = int(input("Enter Employee ID: "))
            days = int(input("Days needed: "))
            system.apply_for_leave(e_id, days)
        except ValueError:
            print("❌ Error: Please enter numbers only.")

    elif choice == "2":
        system.show_all_employees()

    elif choice == "3":
        try:
            e_id = int(input("New ID: "))
            name = input("Name: ")
            bal = int(input("Starting Balance: "))
            system.add_employee(e_id, name, bal)
        except ValueError:
            print("❌ Error: ID and Balance must be numbers.")

    elif choice == "4":
        system.end_of_month_rollover()

    elif choice == "5":
        system.conn.close()
        print("👋 System Shutdown.")
        break

    else:
        print("❌ Invalid Choice.")
