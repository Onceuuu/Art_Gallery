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
from prettytable import PrettyTable

# List of table names
table_names = ['ARTIST', 'ART_WORK', 'CUSTOMER', 'ART_SHOWS']
attributes = ['Aname', 'Phone', 'Address', 'Birth_Place', 'Age', 'Art_style', 'Title', 'Artist', 'Type_of_art',
              'Date_of_creation', 'Date_acquired', 'Price', 'Location', 'Cnumber', 'Phone', 'Art_preferences',
              'Artist', 'Date_and_time', 'Location', 'Contact', 'Contact_phone']

# Function that will print out all the records in a table from the DB
def print_records(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    records = cursor.fetchall()
    for record in records:
        print(record)

# Function that will Access any record based on attribute values
def access_by_attr(cursor, attribute, value):
    # Bool variable if the the attribute value has been found
    found = False
    # Go through all tables to find all entries with the matching attribute and value
    for table_name in table_names:
        # Try and except so that the program doesn't end when a query error occurs
        try:
            # query for user's attribute and value
            query = f"SELECT * FROM {table_name} WHERE {attribute} = '{value}'"

            cursor.execute(query)
            records = cursor.fetchall()

            # if entries with the matching attribute and value were found, it will print it out
            if records:
                print(f'Records in {table_name}:')
                for record in records:
                    print(record)
                found = True
        # Catch sql error
        except mysql.connector.Error as err:
            # prints error, commenting out so output is cleaner
            #print(f"Error: {err}")
            pass
    # If no entries were found, display error message    
    if found == False:
        print(f"\nNo records found for attribute {attribute} with a value of {value} in the Database...")
    print()

# Function that sorts a report according to style
def sort_by_art_style(cursor):
    try:
        # Query to select the Type of Art, Art Work Title, Artist Name, Artist Art Style, Show Location, and Room
        query = f"""
            SELECT
                ART_WORK.Type_of_art, 
                ART_WORK.Title, 
                ART_WORK.Artist, 
                ARTIST.Art_style, 
                ART_SHOWS.Location, 
                ART_WORK.Location as Room 
            FROM
                ART_WORK
                JOIN ARTIST ON ART_WORK.Artist = ARTIST.Aname
                LEFT JOIN ART_SHOWS ON ART_WORK.Artist = ART_SHOWS.Artist
            WHERE
                ART_WORK.Type_of_art IS NOT NULL
            ORDER BY
                ART_WORK.Type_of_art;
        """
        # Execute the query and fetch all records
        cursor.execute(query)
        records = cursor.fetchall()

        # Print out the report
        if records:
            print("\nReport of all Art Works sorted by Art Style\n")
            # Print header with formatted spaces
            print("-" * 149)
            print("| {:<15} | {:<30} | {:<20} | {:<20} | {:<30} | {:<15} |".format(
                "Type of Art", "Title", "Artist Name", "Artist Art Style", "Show Location", "Room"))
            print("-" * 149)

            # Print the entries
            for record in records:
                print("| {:<15} | {:<30} | {:<20} | {:<20} | {:<30} | {:<15} |".format(*record))
                print("-" * 149)
            print()

            """ Using the prettytable library

            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = ["Type of Art", "Title", "Artist Name", "Artist Art Style", "Show Location", "Room"]

            # Add rows to the table
            for record in records:
                table.add_row(record)

            # Print the table
            print("Sorted report for art works by artist's art style:")
            print(table)
            """
        else:
            print("No records found")

    # catch any error
    except mysql.connector.Error as err:
        # Prints the error, commenting out to make output cleaner
        print(f"Error: {err}")


def matching_art_shows(cursor):
    try:
        # Query to select customers whose art preferences match those shown in art shows by a specific artist
        query = f"""
            SELECT
                CUSTOMER.Cnumber, 
                CUSTOMER.Phone, 
                CUSTOMER.Art_preferences, 
                ART_SHOWS.Artist, 
                ART_SHOWS.Location,
                DATE_FORMAT(ART_SHOWS.Date_and_time, '%Y-%m-%d %H:%i:%s')
            FROM
                CUSTOMER
                JOIN ARTIST ON FIND_IN_SET(ARTIST.Art_style, CUSTOMER.Art_preferences)
                JOIN ART_SHOWS ON ART_SHOWS.Artist = ARTIST.Aname
        """

        cursor.execute(query)
        records = cursor.fetchall()

        # Print out report if entries were found
        if records:
            print("\nPrinting report showing customers whose art preference is the same as any of the art shows...\n")
            # Print header
            print("-" * 164)
            print("| {:<15} | {:<15} | {:<40} | {:<20} | {:<30} | {:<25} |".format(
                "Customer Number", "Customer Phone", "Customer Preferences", "Artist", "Art Show Location", "Art Show Date and Time"))
            print("-" * 164)  # Separator line

            # Print rows
            for record in records:
                print("| {:<15} | {:<15} | {:<40} | {:<20} | {:<30} | {:<25} |".format(*record))
                print("-" * 164)  # Separator line

            print()
        # Print message if no entries were found
        else:
            print(f"Customers' art preferences do not match with any of the art shows.\n")

    except mysql.connector.Error as err:
        # Handle the error
        print(f"Error: {err}")

# Main function for program
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
    while(menu_choice != 'Q' and menu_choice != 'q'):
        print("1. Print records from the Database")
        print("2. Access record by attribute")
        print("3. Sort report by art style")
        print("4. Produce a report showing customers whose art perferences is the same in any given show")
        print("Q. Quit ")

        menu_choice = input("Enter your choice (1, 2, 3, 4, or Q): ")

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
            print("List of attributes in the Art Gallery Database")
            print(*attributes, sep = ", ")
            print()
            attribute = input("Enter attribute name: ")
            #while(attribute.lower() in attr.lower() for attr in attributes):
            #    attribute = input("Attribute does not exist. Enter a different attribute: ") 
            if(attribute.lower() == 'date_of_creation' or attribute.lower() == 'date_acquired'):
                value = input("Enter Date (YYYY-MM-DD i.e. 2023-11-15): ")
            elif(attribute.lower() == 'date_and_time'):
                value = input("Enter Date and Time (YYYY-MM-DD HH:MM:SS i.e. 2023-12-02 19:00:00): ")
            elif(attribute.lower() == 'phone' or attribute.lower() == 'contact_phone'):
                value = input("Enter Phone Number (10 digits): ")
            else:
                value = input("Enter attribute value: ")
            access_by_attr(cursor, attribute, value)
        elif menu_choice == '3':
            sort_by_art_style(cursor)
        elif menu_choice == '4':
            matching_art_shows(cursor)

    # close the cursor and connector to the database
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
