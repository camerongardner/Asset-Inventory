import sqlite3
import os

# Define the database filename
db_filename = 'assetInventory.db'

# Function to create the database and tables
def initialize_database():
    # Check if the database already exists
    if not os.path.exists(db_filename):
        # If the database does not exist, create it and the tables
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT NOT NULL
            )
        ''')

        # Create the assets table with a foreign key reference to the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                purchase_price REAL,
                status TEXT,
                location TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Commit the transaction
        connection.commit()
        connection.close()

        print(f"Database '{db_filename}' created along with 'users' and 'assets' tables.")
    else:
        print(f"Database '{db_filename}' loaded.")

# Function to add a new user
def add_user():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    name = input("Enter user name: ")
    email = input("Enter user email: ")
    department = input("Enter user department: ")

    cursor.execute('''
        INSERT INTO users (name, email, department)
        VALUES (?, ?, ?)
    ''', (name, email, department))

    connection.commit()
    print("User added successfully!")

    connection.close()

# Function to add a new asset
def add_asset():

    # Connect to the database to add an entry
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    name = input("Enter asset name: ")
    category = input("Enter asset category: ")
  
    while True:
        purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
        try:
            year, month, day = map(int, purchase_date.split('-'))
            if len(purchase_date) == 10 and 1000 <= year <= 9999 and 1 <= month <= 12 and 1 <= day <= 31:
                break
            else:
                print("Invalid format. Please use YYYY-MM-DD with valid year, month, and day values.")
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD with valid year, month, and day values.")
    
    while True:
        try:
            purchase_price = float(input("Enter purchase price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the purchase price.")

    status = input("Enter status (Available/In Use/Out of Service): ")
    location = input("Enter asset location: ")
    
    while True:
        try:
            user_id = int(input("Enter user ID to assign the asset to: "))
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            if user:
                break
            else:
                print("The user ID was not found. Please add the user now.")
                add_user()
        except ValueError:
            print("Invalid input. Please enter a valid integer for the user ID.")

    cursor.execute('''
        INSERT INTO assets (name, category, purchase_date, purchase_price, status, location, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, category, purchase_date, purchase_price, status, location, user_id))

    connection.commit()
    print("Asset added successfully!")

    connection.close()

# Function to remove an asset
def remove_asset():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    while True:
        try:
            asset_id = int(input("Enter asset ID to remove: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the asset ID.")

    cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
    
    if cursor.rowcount == 0:
        print("Asset not found.")
    else:
        connection.commit()
        print(f"Asset with ID {asset_id} removed successfully!")

    connection.close()

# Function to view all assets with associated users
def view_inventory():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT assets.id, assets.name, assets.category, assets.purchase_date, users.name, users.department
        FROM assets
        JOIN users ON assets.user_id = users.user_id
    ''')

    rows = cursor.fetchall()

    if rows:
        print("\nAsset Inventory:")
        print("----------------------------")
        for row in rows:
            print(f"Asset ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Purchase Date: {row[3]}, User: {row[4]}, Department: {row[5]}")
    else:
        print("No assets found.")

    connection.close()

# Function to view all users
def view_users():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT user_id, name FROM users
    ''')

    rows = cursor.fetchall()

    if rows:
        print("\nUser List:")
        print("----------------------------")
        for row in rows:
            print(f"User ID: {row[0]}, Name: {row[1]}")
    else:
        print("No users found.")

    connection.close()

# Function to display the menu
def menu():
    while True:
        print("\nAsset Inventory Management")
        print("----------------------------")
        print("1. Add User")
        print("2. Add Asset")
        print("3. Remove Asset")
        print("4. View Inventory")
        print("5. View Users")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            add_asset()
        elif choice == '3':
            remove_asset()
        elif choice == '4':
            view_inventory()
        elif choice == '5':
            view_users()
        elif choice == '6':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Program Execution
initialize_database()
menu()
