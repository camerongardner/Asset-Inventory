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

        # Add the tables to the database
        connection.commit()
        connection.close()

    # Inform the user the status of the database when the program starts
        print(f"Database '{db_filename}' created along with 'users' and 'assets' tables.")
    else:
        print(f"Database '{db_filename}' loaded.")

# Function to provide a user menu of which table to add to.
def adding_to_database():
    while True:
        print("\nAdding assets and/or users")
        print("----------------------------")
        print("1. Add User or Asset")
        print("2. Add Asset")
        print("3. Return to Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            add_asset()
        elif choice == '3':
            print("Returning to menu...")
            break
        else:
            print("Invalid choice. Please try again.")

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
  
    # Error handling to ensure that the date value is provided in the format demonstrated in the prompt to the user
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
    
    # Error Handlong to prevent string values from being provided
    while True:
        try:
            purchase_price = float(input("Enter purchase price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the purchase price.")

    status = input("Enter status (Available/In Use/Out of Service): ")
    location = input("Enter asset location: ")
    
    while True:
        # Error handling to ensure that the user ID associated with the newly created asset exists and prompts the user to create the user if the
        # user does not currently exsiist
        try:
            user_id = int(input("Enter user ID to assign the asset to: "))
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()

            #Logic to determine if the user input is associated with an exsisting user
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

# Function to prompt the user to remove an entry from one of the tables in the database
def remove_entry():
    while True:
        print("\nAsset Inventory Management")
        print("----------------------------")
        print("1. Remove an Asset")
        print("2. Remove a User")
        print("3. Return to Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            remove_asset()
        elif choice == '2':
            remove_user()   
        elif choice == '3':
            print("Returning to Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to remove an asset
def remove_asset():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Check to see if there are assets in the inventory
    cursor.execute('SELECT * FROM assets')
    assets = cursor.fetchall()

    # Error handlong to inform the user if there are no assets, otherwise allowes the user to delete an asset.
    if not assets:
        print("There are no assets in the inventory")
    else:
        view_inventory()
        # Error handlong to ensure the user choice is an exsisting inventory item
        while True:
            try:
                asset_id = int(input("Enter asset ID to remove or type 0 to cancel: "))
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

# Function to remove a user if they are not linked to an existing asset
def remove_user():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Check if there are users without assets
    cursor.execute('''
        SELECT user_id, name FROM users
        WHERE user_id NOT IN (SELECT DISTINCT user_id FROM assets)
    ''')
    users = cursor.fetchall()

    # Logic to inform the user if there are no users in the users table
    if not users:
        print("There are no users that can be removed as all are linked to existing assets.")
    else:
        print("\nUsers without assets:")
        for user in users:
            print(f"User ID: {user[0]}, Name: {user[1]}")
        
        # Error handlong to ensure that only a valid user ID can be selected
        while True:
            try:
                user_id = int(input("Enter user ID to remove or type 0 to cancel: "))
                if user_id == 0:
                    print("Operation cancelled.")
                    return
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the user ID.")

        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        
        # Error checking to prevent a user from being deleted if they are associated to an asset/don't exsist
        if cursor.rowcount == 0:
            print("User not found or user is linked to an asset.")
        else:
            connection.commit()
            print(f"User with ID {user_id} removed successfully!")

    connection.close()

# Menu to choose which SQL table to view
def view_tables():
    while True:
        print("\nViewing asset or user tables")
        print("----------------------------")
        print("1. View Inventory")
        print("2. View Users")
        print("3. Return to Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_inventory()
        elif choice == '2':
            view_users()
        elif choice == '3':
            print("Returning to Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

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

    # Logic to check if there are any assets to be displayed. If there are no assets the user is informed
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

    # Logic used to inform the user if there are no users in the users tabe. If there are users they are listed
    if rows:
        print("\nUser List:")
        print("----------------------------")

        # Loop to iterate through each row of the entries in the asset table
        for row in rows:
            print(f"User ID: {row[0]}, Name: {row[1]}")
    else:
        print("No users found.")

    connection.close()

# Function to prompt the user which database they want to edit an entry from
def edit_entry():
    while True:
        print("\nEdit Entries")
        print("----------------------------")
        print("1. Edit User Entry")
        print("2. Edit Asset Entry")
        print("3. Return to Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            edit_user()
        elif choice == '2':
            edit_asset()
        elif choice == '3':
            print("Returning to Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to edit an entry in the users table
def edit_user():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    view_users()
    
    # Error handlng to ensiure that the user ID selected exsists
    while True:
        try:
            user_id = int(input("Enter the user ID to edit: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the user ID.")

    # Code to initiate the SQL querry to get the desired entry
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        new_name = input(f"Enter new name (current: {user[1]}): ") or user[1]
        new_email = input(f"Enter new email (current: {user[2]}): ") or user[2]
        new_department = input(f"Enter new department (current: {user[3]}): ") or user[3]

        cursor.execute('''
            UPDATE users
            SET name = ?, email = ?, department = ?
            WHERE user_id = ?
        ''', (new_name, new_email, new_department, user_id))
        connection.commit()
        print("User updated successfully!")
    else:
        print("User not found.")

    connection.close()

# Function to edit an entry in the assets table
def edit_asset():
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    view_inventory()
    while True:
        try:
            asset_id = int(input("Enter the asset ID to edit: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the asset ID.")

    cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
    asset = cursor.fetchone()

    # Allow the user to change any value of the entry but also allow the user tp press enter
    #to keep the original valie unaltered
    if asset:
        new_name = input(f"Enter new asset name (current: {asset[1]}): ") or asset[1]
        new_category = input(f"Enter new category (current: {asset[2]}): ") or asset[2]

        # Error handlong to ensure that the purchase date is n accordance witht he defined outline
        while True:
            new_purchase_date = input(f"Enter new purchase date (current: {asset[3]}): ") or asset[3]
            try:
                year, month, day = map(int, new_purchase_date.split('-'))
                if len(new_purchase_date) == 10 and 1000 <= year <= 9999 and 1 <= month <= 12 and 1 <= day <= 31:
                    break
                else:
                    print("Invalid format. Please use YYYY-MM-DD with valid year, month, and day values.")
            except ValueError:
                print("Invalid format. Please use YYYY-MM-DD with valid year, month, and day values.")
        while True:
            try:
                new_purchase_price = float(input(f"Enter new purchase price (current: {asset[4]}): ") or asset[4])
                break
            except ValueError:
                print("Invalid input. Please enter a valid number for the purchase price.")
        new_status = input(f"Enter new status (current: {asset[5]}): ") or asset[5]
        new_location = input(f"Enter new location (current: {asset[6]}): ") or asset[6]

        # Error handlong to ensure that the user assigned to the asset exists
        while True:
            try:
                new_user_id = int(input(f"Enter new user ID (current: {asset[7]}): ") or asset[7])
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (new_user_id,))
                user = cursor.fetchone()
                if user:
                    break
                else:
                    print("The user ID was not found. Please enter a valid user ID.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the user ID.")

        cursor.execute('''
            UPDATE assets
            SET name = ?, category = ?, purchase_date = ?, purchase_price = ?, status = ?, location = ?, user_id = ?
            WHERE id = ?
        ''', (new_name, new_category, new_purchase_date, new_purchase_price, new_status, new_location, new_user_id, asset_id))
        connection.commit()
        print("Asset updated successfully!")
    else:
        print("Asset not found.")

    connection.close()

# Function to display the menu
def menu():
    while True:
        print("\nAsset Inventory Management")
        print("----------------------------")
        print("1. Add Users and/or Assets")
        print("2. Remove an entry from the Database")
        print("3. View Database Tables")
        print("4. Edit an Entry")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            adding_to_database()
        elif choice == '2':
            remove_entry()
        elif choice == '3':
            view_tables()      
        elif choice == '4':
            edit_entry()
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

# Main Program Execution
initialize_database()
menu()