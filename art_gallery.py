# Joshua Villareal
# CPSC 332-02
# 2023-12-06
# jvillareal@csu.fullerton.edu
# @Onceuuu
#
# This file contains the program to run the Art Gallery Database
#

# make sure mysql.connector is installed by using: pip install mysql-connector-python
import mysql.connector

# List of table names
table_names = ['ARTIST', 'ART_WORK', 'CUSTOMER', 'ART_SHOWS']

# Function that will print out all the records in a table from the DB
def print_records(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    records = cursor.fetchall()
    for record in records:
        print(record)

# Function that will Access any record based on attribute values
def access_by_attr(cursor, attribute, value):
    found = False
    for table_name in table_names:
        try:
            query = f"SELECT * FROM {table_name} WHERE {attribute} = '{value}'"
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                print(f'Records in {table_name}:')
                for record in records:
                    print(record)
                found = True
    
        except mysql.connector.Error as err:
            pass
    if found == False:
        print("No records found for attribute {attribute} with a value of {value} in the Database...")
# Function
def main():
    # connect to the database using the host, user, and password info
    cnx = mysql.connector.connect(host = 'localhost', user = 'root', password = 'Chaewon', database = 'art_gallery')

    print(cnx)

    # Create cursor object to be able to execute SQL statements
    # menu choice variable to save from user input
    cursor = cnx.cursor()
    menu_choice = ''
    # Bool variable if the user's input is valid
    valid = False
    # Give user a choice menu to pick what actions they want to do
    while(menu_choice != 'Q'):
        print("1. Print records from the Database")
        print("2. Access record by attribute")
        print("3. Sort report by art style")
        print("Q. Quit ")

        menu_choice = input("Enter your choice: ")

        # If user wants to print records from the DB
        if menu_choice == '1':
            # Checks if the user inputted a valid table name
            # Continues to prompt the user for a valid table name if input is invalid
            while(valid == False):
                table_name = input("Enter table name (ARTIST, ART_WORK, CUSTOMER, or ART_SHOWS): ")
                table_name = table_name.upper()
                if table_name in table_names:
                    valid = True
                else:
                    print("Invalid table name. Please enter the table name again...")
            print(f'\nPrinting records from the {table_name} table\n')
            print_records(cursor, table_name)
            valid = False
            print()
        elif menu_choice == '2':
            attribute = input("Enter attribute name: ")
            value = input("Enter attribute value: ")
            access_by_attr(cursor, attribute, value)
    """    elif menu_choice == '3':
            sort_by_art_style(cursor)
"""
    # close the cursor and connector to the database
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()