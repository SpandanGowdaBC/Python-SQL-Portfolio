import datetime
import sqlite3  # <--- CHANGED: Replaced 'json' and 'os' with 'sqlite3'


# --- PARENT CLASS (The Blueprint) ---
class Vehicle:
    def __init__(self, plate_number, v_type, is_vip=False):
        self.plate_number = plate_number
        self.v_type = v_type
        self.is_vip = is_vip
        self.entry_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate_bill(self, entry_time_str, exit_time_str):
        # Convert strings back to time objects
        entry_obj = datetime.datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        exit_obj = datetime.datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")

        duration = (exit_obj - entry_obj).total_seconds()

        # Pricing Logic
        rate = 0.5 if self.v_type == "Bike" else 1.0

        # 💰 SURCHARGE LOGIC
        if self.is_vip:
            rate = rate * 1.5

        return round(duration * rate, 2)


# --- MAIN MANAGER CLASS (SQL Version) ---
class ParkingManager:
    def __init__(self, db_name="parking_db.db"):
        self.total_slots = 10
        # 1. CONNECT to Database (Creates file automatically if missing)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # 2. CREATE TABLE if it doesn't exist
        # This replaces the 'load_data' function
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS parking (
                plate TEXT PRIMARY KEY,
                v_type TEXT,
                entry_time TEXT,
                is_vip INTEGER
            )
        """
        )
        self.conn.commit()

    # NOTE: load_data and save_data are REMOVED because SQL saves instantly.

    def park_vehicle(self, plate, v_type, is_vip=False):
        # Check total capacity using SQL Count
        self.cursor.execute("SELECT count(*) FROM parking")
        current_count = self.cursor.fetchone()[0]

        if current_count >= self.total_slots:
            print("❌ Parking Full!")
            return

        # Check if vehicle already exists in DB
        self.cursor.execute("SELECT plate FROM parking WHERE plate=?", (plate,))
        if self.cursor.fetchone():
            print("⚠️ Vehicle already inside!")
            return

        # Create Vehicle Object (mainly to get the timestamp)
        new_vehicle = Vehicle(plate, v_type, is_vip)

        # 3. INSERT into Database (Replaces dictionary assignment)
        try:
            self.cursor.execute(
                "INSERT INTO parking VALUES (?, ?, ?, ?)",
                (
                    new_vehicle.plate_number,
                    new_vehicle.v_type,
                    new_vehicle.entry_time,
                    1 if new_vehicle.is_vip else 0,
                ),
            )  # Store boolean as 1 or 0
            self.conn.commit()
            print(f"✅ {v_type} {plate} Parked at {new_vehicle.entry_time}")
        except sqlite3.Error as e:
            print(f"❌ Database Error: {e}")

    def remove_vehicle(self, plate):
        # 4. SELECT from Database (Replaces dictionary lookup)
        self.cursor.execute("SELECT * FROM parking WHERE plate=?", (plate,))
        data = self.cursor.fetchone()

        if not data:
            print("❌ Vehicle not found!")
            return

        # Unpack the data from SQL: (plate, type, time, is_vip_int)
        _, v_type, entry_time, vip_int = data
        is_vip = bool(vip_int)  # Convert 1/0 back to True/False

        # Calculate Bill (Reuse Vehicle Class Logic)
        temp_vehicle = Vehicle(plate, v_type, is_vip)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # We pass the OLD entry time from DB and NEW exit time
        bill = temp_vehicle.calculate_bill(entry_time, current_time)

        print(f"\n--- 🧾 RECEIPT ---")
        print(f"Vehicle: {plate} ({v_type})")
        if is_vip:
            print(f"Status:  🌟 VIP (50% Surcharge Applied)")
        else:
            print(f"Status:  Standard")
        print(f"Time:    {current_time}")
        print(f"💰 TOTAL: ${bill}")
        print("------------------")

        # 5. DELETE from Database
        self.cursor.execute("DELETE FROM parking WHERE plate=?", (plate,))
        self.conn.commit()

    def view_analytics(self):
        # SQL Queries replace the Python Loop
        self.cursor.execute("SELECT count(*) FROM parking")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT count(*) FROM parking WHERE v_type='Car'")
        cars = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT count(*) FROM parking WHERE v_type='Bike'")
        bikes = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT count(*) FROM parking WHERE is_vip=1")
        vips = self.cursor.fetchone()[0]

        print(f"\n📊 Live Analytics:")
        print(f"Total: {total}/{self.total_slots}")
        print(f"🚗 Cars: {cars} | 🏍️ Bikes: {bikes}")
        print(f"🌟 VIPs currently parked: {vips}")


# --- CHILD CLASS (Unchanged Logic) ---
class VIPParking(ParkingManager):
    def park_vehicle(self, plate, v_type, is_vip=False):
        if is_vip:
            print(f"\n🌟 VIP DETECTED: Priority Service enabled for {plate} (+50% Fee)")
        else:
            print(f"\nℹ️ Standard Entry for {plate}")

        # Pass data to parent to do the actual saving in SQL
        super().park_vehicle(plate, v_type, is_vip)


# --- EXECUTION ---
manager = VIPParking()

while True:
    print("\n1. Park Car   2. Park Bike   3. Exit Vehicle   4. Analytics   5. Exit")
    choice = input("Enter Choice: ")

    if choice == "1":
        p = input("Enter Plate Number: ")
        vip_status = input("Are you VIP? (yes/no): ").lower() == "yes"
        manager.park_vehicle(p, "Car", is_vip=vip_status)

    elif choice == "2":
        p = input("Enter Plate Number: ")
        vip_status = input("Are you VIP? (yes/no): ").lower() == "yes"
        manager.park_vehicle(p, "Bike", is_vip=vip_status)

    elif choice == "3":
        p = input("Enter Plate Number: ")
        manager.remove_vehicle(p)

    elif choice == "4":
        manager.view_analytics()

    elif choice == "5":
        # It's good practice to close the connection
        manager.conn.close()
        break
