import sqlite3


# --- MAIN SYSTEM CLASS ---
class ShopManager:
    def __init__(self, db_name="store_db.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cart = []  # We keep the active cart in memory, products in SQL
        self.setup_database()

    def setup_database(self):
        # 1. Create the Products Table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                category TEXT
            )
        """
        )

        # 2. Seed Data (Only if table is empty, so we don't duplicate items)
        self.cursor.execute("SELECT count(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            print("⚙️ Initializing Database with Stock...")
            items = [
                (101, "Dell Laptop", 1000.0, "Electronics"),
                (102, "iPhone 15", 900.0, "Electronics"),
                (201, "Gucci Shirt", 100.0, "Fashion"),
                (202, "Levis Jeans", 80.0, "Fashion"),
                (203, "Nike Cap", 40.0, "Fashion"),
                (301, "Coffee Mug", 15.0, "Home"),
                (302, "Bed Sheet", 50.0, "Home"),
            ]
            self.cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", items)
            self.conn.commit()

    def show_catalog(self):
        print("\n--- 📦 PRODUCT CATALOG ---")
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        for r in rows:
            # r[0]=ID, r[1]=Name, r[2]=Price, r[3]=Category
            print(f"🆔 {r[0]} | {r[1]} | 💲{r[2]} | [{r[3]}]")
        print("--------------------------")

    def add_to_cart(self, product_id):
        # 3. Fetch Product details from SQL using ID
        self.cursor.execute(
            "SELECT name, price, category FROM products WHERE id=?", (product_id,)
        )
        item = self.cursor.fetchone()

        if item:
            # Add to our local cart list
            self.cart.append({"name": item[0], "price": item[1], "category": item[2]})
            print(f"✅ Added to Cart: {item[0]} (${item[1]})")
        else:
            print("❌ Error: Product ID not found!")

    def view_cart(self):
        if not self.cart:
            print("\n🛒 Cart is empty.")
        else:
            print(f"\n🛒 Items in Cart: {len(self.cart)}")
            for item in self.cart:
                print(f" - {item['name']} (${item['price']})")

    def clear_cart(self):
        self.cart = []
        print("🗑️ Cart Emptied.")

    def checkout(self):
        if not self.cart:
            print("⚠️ Your cart is empty!")
            return

        total = 0
        fashion_items = []

        print("\n--- 🧾 FINAL RECEIPT ---")

        # Step 1: Separate Fashion Items from Others
        for item in self.cart:
            if item["category"] == "Fashion":
                fashion_items.append(item)
            else:
                total += item["price"]
                print(f"🔹 {item['name']}: ${item['price']}")

        # Step 2: BOGO Logic (Sort High -> Low)
        # This ensures you pay for the expensive one, and get the cheaper one free
        fashion_items.sort(key=lambda x: x["price"], reverse=True)

        i = 0
        while i < len(fashion_items):
            item1 = fashion_items[i]

            if i + 1 < len(fashion_items):
                item2 = fashion_items[i + 1]

                # Pair Found! Buy 1, Get 1
                total += item1["price"]
                print(f"🔹 {item1['name']}: ${item1['price']}")
                print(f"🎁 {item2['name']}: $0.00 (BOGO Promo!)")
                i += 2
            else:
                # No Pair (Odd item out)
                total += item1["price"]
                print(f"🔹 {item1['name']}: ${item1['price']}")
                i += 1

        print("--------------------------")
        print(f"💰 GRAND TOTAL: ${total}")
        print("--------------------------")

        self.cart = []  # Reset cart after purchase
        print("✅ Transaction Saved.")


# --- EXECUTION ---
system = ShopManager()

while True:
    print("\n1. View Catalog   2. Add Item (ID)   3. View Cart   4. Checkout   5. Exit")
    choice = input("Enter Choice: ")

    if choice == "1":
        system.show_catalog()

    elif choice == "2":
        try:
            pid = int(input("Enter Product ID: "))
            system.add_to_cart(pid)
        except ValueError:
            print("❌ Error: Please enter a numeric ID.")

    elif choice == "3":
        system.view_cart()

    elif choice == "4":
        system.checkout()

    elif choice == "5":
        system.conn.close()
        print("👋 Exiting Store.")
        break
