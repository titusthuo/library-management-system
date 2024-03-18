import mysql.connector

# Establishing connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="107220Mwangi@",
    database="library_management_system"
)

# Creating cursor object to execute SQL queries
mycursor = mydb.cursor()

# Function for teacher session
def teacher_session():
    while True:
        print("....WELCOME TO THE LIBRARY......")
        print(".  1. Borrow books   .")
        print(".  2. Return a book .")
        print(".  3. Log out        .")
        insert_option = input("Choose service: ")
        if insert_option == "1":
            borrow_books()
        elif insert_option == "2":
            return_book()
        elif insert_option == "3":
            break
        else:
            print("Invalid service")

# Function for borrowing books
def borrow_books():
    print("........................NOTE...........................")
    print("A book can only be borrowed for a maximum of 10 days. More than that, the book ")
    print("will be counted overdue after 10 days and will be penalized upon returning")

    mycursor.execute("SELECT * FROM bookrecord")
    for x in mycursor:
        print(x)

    book = input("Enter book title: ")
    author = input("Enter author: ")
    year = input("Enter Year: ")
    days = input("Enter number of days: ")

    query_values = (book, author)
    query_values1 = (book, author, year, days)

    mycursor.execute("DELETE FROM bookRecord WHERE title = %s AND author = %s", query_values)
    mydb.commit()

    if mycursor.rowcount < 1:
        print("The book is not available")
    else:
        mycursor.execute("INSERT INTO issue (title, author, year, days) VALUES (%s, %s, %s, %s)", query_values1)
        mydb.commit()

        if mycursor.rowcount < 1:
            print("A book can only be borrowed for a maximum of 10 days")
        else:
            print("Get the book at the front desk of the library")

# Function for returning books
def return_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    year = input("Enter book year: ")
    school = input("Enter book department: ")
    book_type = input("Enter book type: ")

    query_values = (title, author, year)
    query_values1 = (title, author, year)

    mycursor.execute("DELETE FROM issue WHERE title = %s AND author = %s AND year = %s", query_values)
    mydb.commit()

    if mycursor.rowcount < 1:
        print("The book was either removed from the shelves due to overdue or the details are incorrect")
    else:
        query_values2 = (title, author, year, school, book_type)
        mycursor.execute("INSERT INTO bookRecord (title, author, year, school, type) VALUES (%s, %s, %s, %s, %s)",
                         query_values2)
        mydb.commit()
        print("Book returned")

# Function for student session
def student_session():
    while True:
        print("....LIBRARY SERVICES......")
        print(".    1. Borrow books      .")
        print(".    2. Return a book    .")
        print(".    3. Log out           .")
        insert_option = input("Choose service: ")

        if insert_option == "1":
            borrow_books()
        elif insert_option == "2":
            return_book()
        elif insert_option == "3":
            break
        else:
            print("Invalid service")

# Function for teacher authentication
def auth_teacher():
    print("Login as a registered Teacher")
    username = input("Enter Teacher username: ")
    password = input("Enter Teacher password: ")
    query_values = (username, password)
    mycursor.execute("SELECT username FROM member WHERE username = %s and password = %s", query_values)
    user_check = mycursor.fetchall()

    if user_check:
        teacher_session()
    else:
        print("Invalid username or password. Register as teacher into the library.")

        username = input("Teacher username: ")
        password = input("Teacher password: ")
        query_values = (username, password)
        mycursor.execute("INSERT INTO member(username, password, privilege) VALUES (%s, %s, 'teacher')", query_values)
        mydb.commit()

        print("You have been registered successfully! You can now log in.")

# Function for student authentication
def auth_student():
    print("Login as a registered student")
    username = input("Enter student username: ")
    password = input("Enter student password: ")
    query_values = (username, password)
    mycursor.execute("SELECT username FROM member WHERE username = %s and password = %s", query_values)
    user_check = mycursor.fetchall()

    if user_check:
        student_session()
    else:
        print("Invalid username or password. Register into the library.")

        username = input("Student username: ")
        password = input("Student password: ")
        query_values = (username, password)
        mycursor.execute("INSERT INTO member(username, password, privilege) VALUES (%s, %s, 'student')", query_values)
        mydb.commit()

        print("You have been registered successfully! You can now log in.")

# Function for admin session
def admin_session():
    while True:
        print("Admin menu")
        print("1. Register new student")
        print("2. Register new teacher")
        print("3. Deregister existing student")
        print("4. Deregister existing teacher")
        print("5. Add books delivered")
        print("6. Remove unreturned and overdue books from issued books records")
        print("7. Log out")
        user_option = input("Option: ")

        if user_option == "1":
            register_student()
        elif user_option == "2":
            register_teacher()
        elif user_option == "3":
            deregister_student()
        elif user_option == "4":
            deregister_teacher()
        elif user_option == "5":
            add_delivered_books()
        elif user_option == "6":
            remove_overdue_books()
        elif user_option == "7":
            break
        else:
            print("Invalid option")

# Function for admin authentication (with automatic login)
def auth_manager():
    print("Manager login")
    # Automatic login without credentials
    admin_session()

# Function for registering new student
def register_student():
    username = input("Student username: ")
    password = input("Student password: ")
    query_values = (username, password)
    mycursor.execute("INSERT INTO member(username, password, privilege) VALUES (%s, %s, 'student')", query_values)
    mydb.commit()
    print(username + " has been registered as a student.")

# Function for registering new teacher
def register_teacher():
    username = input("Teacher username: ")
    password = input("Teacher password: ")
    query_values = (username, password)
    mycursor.execute("INSERT INTO member(username, password, privilege) VALUES (%s, %s, 'teacher')", query_values)
    mydb.commit()
    print(username + " has been registered as a teacher.")

# Function for deregistering existing student
def deregister_student():
    username = input("Student username: ")
    query_values = (username, "student")
    mycursor.execute("DELETE FROM member WHERE username = %s AND privilege = %s", query_values)
    mydb.commit()
    if mycursor.rowcount < 1:
        print("User does not exist")
    else:
        print(username + " has been deregistered as a student.")

# Function for deregistering existing teacher
def deregister_teacher():
    username = input("Teacher username: ")
    query_values = (username, "teacher")
    mycursor.execute("DELETE FROM member WHERE username = %s AND privilege = %s", query_values)
    mydb.commit()
    if mycursor.rowcount < 1:
        print("User does not exist")
    else:
        print(username + " has been deregistered as a teacher.")

# Function for adding delivered books
def add_delivered_books():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    year = input("Enter book year: ")
    department = input("Enter book department: ")
    book_type = input("Enter book type: ")
    query_values = (title, author, year, department, book_type)
    mycursor.execute("INSERT INTO bookRecord (title, author, year, department, type) VALUES (%s, %s, %s, %s, %s)",
                     query_values)
    mydb.commit()
    if mycursor.rowcount < 1:
        print("The book record has not been added")
    else:
        print(title + " by " + author + " has been recorded.")

# Function for removing unreturned and overdue books
def remove_overdue_books():
    mycursor.execute("DELETE FROM issue WHERE days > 10")
    mydb.commit()
    if mycursor.rowcount < 1:
        print("No overdue books found")
    else:
        print("Overdue books have been removed from the book records.")

# Main function to run the program
def main():
    while True:
        print("WELCOME TO THE LIBRARY")
        print("....LOGIN AS....")
        print("1. STUDENT")
        print("2. TEACHER")
        print("3. LIBRARY MANAGER")
        print("4. LOG OUT")
        insert_choice = input("Enter your choice: ")

        if insert_choice == "1":
            auth_student()
        elif insert_choice == "2":
            auth_teacher()
        elif insert_choice == "3":
            auth_manager()
        elif insert_choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
