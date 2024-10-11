## Asset Inventory Management System

## Description

This project implements an Asset Inventory Management System using Python and SQLite. The system allows users to interact with an SQL relational database to manage asset records, providing the ability to insert, modify, delete, and retrieve asset data. Additionaly, users are able manage the users associated with each asset in the same manner. This project demonstrates a working interaction between Python and an SQLite database.

## Features

- Add new assets to the inventory.
- Edit existing asset records (assets or users).
- Delete assets from the inventory.
- Query and retrieve asset details from the database.
- View a list of users that have ownership of assets.
- View a list of assets along with the user assigned to each asset.

## Technologies Used

- **Python**: Used as the primary programming language to create the system.
- **SQLite**: The database engine used for storing and managing asset and user data.

## Installation and Setup

To run this project, you need the following installed on your system:

- **Python 3.x** (You can download it from [python.org](https://www.python.org))
- **SQLite** (You can download it from [sqlite.org](https://www.sqlite.org))

### Steps to Run:

1. Clone or download the repository.
2. Ensure you have sqlite3 installed in your Python environment by running:
   ```bash
   pip install pysqlite3
   ```
3. Open a terminal and navigate to the project directory.
4. Run the Python script to start the asset inventory system:
   ```bash
   python start.py
   ```

## Usage

Once the project is running, you can perform the following operations:

- **Add Asset**: Enter details such as asset name, ID, category, purchase date, purchase price, status, location, and assign a user to store new records in the database.
- **Edit Asset or User**: Modify existing asset or user details by specifying the ID of the asset or user you want to edit. You will be prompted to update the relevant information.
- **Delete Asset**: Remove assets from the database using the asset ID.
- **Query Asset**: Retrieve and display specific asset details or lists of all assets. You can search by asset ID or view all assets in the inventory.
- **View Asset List with User Details**: View a complete list of assets along with the assigned user details by joining the users and assets tables.

## Database Schema

The SQLite database consists of two tables for managing users and assets with the following schema:

### Users Table

| Column Name | Data Type | Description |
| ----------- | --------- | ----------- |
| user_id     | INTEGER   | Primary Key, Unique User ID |
| name        | TEXT      | Name of the user |
| email       | TEXT      | Email address of the user |
| department  | TEXT      | Department to which the user belongs |

### Assets Table

| Column Name    | Data Type | Description |
| -------------- | --------- | ----------- |
| id             | INTEGER   | Primary Key, Unique Asset ID |
| name           | TEXT      | Name of the asset |
| category       | TEXT      | Category of the asset |
| purchase_date  | TEXT      | Purchase date of the asset |
| purchase_price | REAL      | Purchase price of the asset |
| status         | TEXT      | Operational status of the asset |
| location       | TEXT      | Location of the asset |
| user_id        | INTEGER   | Foreign Key, references `user_id` in users table |

## Stretch Challenges

- **Join Operations**: This project has been extended to demonstrate SQL joins between the users and assets tables. Specifically, it retrieves assets along with their assigned owners by joining the asset and user tables.
- **Error Handling**: Along with this project specific attention has been implemented to ensure user actions do not negatively affect the data being stored and manipulated in the database. 

## Video Demonstration
A full demonstration of the system can be viewed [here](https://studio.youtube.com/video/-kzoPFdEQHY/edit).

## Contribution

If you would like to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.