# make sure mysql.connector is installed by using: pip install mysql-connector-python
import mysql.connector

# Function that will 
def print_records(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    records = cursor.fetchall()
    for record in records:
        print(record)

def main():
    # connect to the database using the host, user, and password info
    cnx = mysql.connector.connect(host = 'localhost', user = 'root', password = 'Chaewon', database = 'art_gallery')

    print(cnx)

    # Create cursor object to be able to execute SQL statements
    # menu choice variable to save from user input
    cursor = cnx.cursor()
    menu_choice = ''

    print_records(cursor, 'ART_WORK')
    """
    while(menu_choice != 'Q'):
        print("1. Print records from the Database")
        print("2. Access record by attribute")
        print("3. Sort report by art style")
        print("Q. Quit ")

        menu_choice = input("Enter your choice: ")

        if menu_choice == '1':
            table_name = input("Enter table name (ARTIST, ART_WORK, CUSTOMER, or ART_SHOWS): ")
            print_records(cursor, table_name)
        elif menu_choice == '2':
            attribute = input("Enter attribute name: ")
            value = input("Enter attribute value: ")
            access_by_attr(cursor, attribute, value)
        elif menu_choice == '3':
            sort_by_art_style(cursor)
"""
    # close the cursor and connector to the database
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()