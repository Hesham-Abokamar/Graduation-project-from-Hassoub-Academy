import sqlite3
import sys
import re


def connect_database():
    try:

        conn = sqlite3.connect('students system.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                school_year INTEGER,
                registration_date TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                lesson_name TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
    
        conn.commit()
        return conn, cursor
    
    except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)


def student_exists(cursor, student_id):

    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    return cursor.fetchone() is not None


def get_student_input(cursor):

    while True:
        try:
            student_id = int(input("Please enter the student ID : "))

            if student_exists(cursor, student_id):
                print("Sorry but the student id is already exists please enter another one !")
            else:
                break

        except ValueError:
            print("Sorry but please enter a numeric value only ! ")

    while True:
        try:
            name = input("Please enter the name : ")
            
            def custom_isalpha(s):

                s_without_spaces = s.replace(" ", "")
                
                return s_without_spaces.isalpha()
            
            isalpha_result = custom_isalpha(name)

            if isalpha_result:
                break
            else:
                raise ValueError

        except ValueError:
            print("Invalid input , Please make sure that the name contains letters only without spaces !")

    while True:
        try:
            last_name = input("Please enter the last Name : ")
            
            def custom_isalpha(s):

                s_without_spaces = s.replace(" ", "")
                
                return s_without_spaces.isalpha()
            
            isalpha_result = custom_isalpha(last_name)

            if isalpha_result:
                break
            else:
                raise ValueError

        except ValueError:
            print("Invalid input , Please make sure that the last name contains letters only !")
        
    while True:
        try:
            age = int(input("Please enter the age : "))
            break 
        except ValueError:
            print("Sorry but you should to enter a numeric value only !")

    while True:
        try:
            school_year = int(input("Please enter the school year : "))
            break 
        except ValueError:
            print("Sorry but you should to enter a numeric value only !")
            
    while True:
        try:
            registration_date = input("Please enter the registration Date (example: '1/1/2024' ) : ")

            if not re.match(r'\d{1,2}/\d{1,2}/\d{4}', registration_date):
                raise ValueError("Invalid input format. Please follow the example format.")
            break
        except ValueError:
            print("Invalid input . Please follow the example format !")

    while True:
        try:
            lesson_name = input("Please enter the lessons of the student (example: science, math, chemistry ... ) : ")

            def custom_isalpha(s):

                s_without_commas = s.replace(",", " ")
                s_without_spaces = s_without_commas.replace(" ", "")
                
                return s_without_commas, s_without_spaces.isalpha()
            
            s_without_commas, isalpha_result = custom_isalpha(lesson_name)

            if s_without_commas and isalpha_result:
                break
            else:
                raise ValueError

        except ValueError:
            print("Sorry, but please make sure that the input contains letters only !")

    return student_id, name, last_name, age, school_year, registration_date, lesson_name


def get_student_input_for_update():

    while True:
        try:
            print("")
            name = input("Please enter the new name : ")

            def custom_isalpha(s):

                s_without_spaces = s.replace(" ", "")
                
                return s_without_spaces.isalpha()
            
            isalpha_result = custom_isalpha(name)

            if isalpha_result:
                break
            else:
                raise ValueError
            
        except ValueError:
            print("Invalid input , Please make sure that the new name contains letters only !")

    while True:
        try:
            last_name = input("Please enter the new last Name : ")

            def custom_isalpha(s):

                s_without_spaces = s.replace(" ", "")
                
                return s_without_spaces.isalpha()
            
            isalpha_result = custom_isalpha(last_name)

            if isalpha_result:
                break
            else:
                raise ValueError
            
        except ValueError:
            print("Invalid input , Please make sure that the new last name contains letters only !")
        
    while True:
        try:
            age = int(input("Please enter the age : "))
            break 
        except ValueError:
            print("Sorry but you should to enter a numeric value only !")

    while True:
        try:
            school_year = int(input("Please enter the new school year : "))
            break 
        except ValueError:
            print("Sorry but you should to enter a numeric value only !")
            
    while True:
        try:
            registration_date = input("Please enter the new registration Date (example: '1/1/2024' ) : ")

            if not re.match(r'\d{1,2}/\d{1,2}/\d{4}', registration_date):
                raise ValueError("Invalid input format. Please follow the example format.")
            break
        except ValueError:
            print("Invalid input . Please follow the example format !")

    while True:
        try:
            lesson_name = input("Please enter the new lessons of the student (example: science, math, chemistry ... ): ")

            def custom_isalpha(s):

                s_without_commas = s.replace(",", " ")
                s_without_spaces = s_without_commas.replace(" ", "")
                
                return s_without_commas, s_without_spaces.isalpha()
            
            s_without_commas, isalpha_result = custom_isalpha(lesson_name)

            if s_without_commas and isalpha_result:
                break
            else:
                raise ValueError

        except ValueError:
            print("Sorry, but please make sure that the input contains letters only !")


    return name, last_name, age, school_year, registration_date, lesson_name


def add_student(cursor, conn):
    
    print("")
    print("To add Student :- ")
    print("")

    student_info = get_student_input(cursor)

    if student_info:
        student_id, name, last_name, age, school_year, registration_date, lesson_name = student_info

        if not student_exists(cursor, student_id):
            
            cursor.execute('''
            INSERT INTO students (id, name, last_name, age, school_year, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, last_name, age, school_year, registration_date))

            cursor.execute('''
            INSERT INTO lessons (student_id, lesson_name)
            VALUES (?, ?)
            ''', (student_id, lesson_name.strip()))

            print("")
            print("Student added successfully.")
            conn.commit()
        else:
            print("")
            print("Student already exists.")


def delete_student(cursor, conn):

    try_again_main = True

    while try_again_main:
        
        print("")
        print("To delete Student:")
        print("")
        try:
            student_id = int(input("Please enter the student ID: "))

            if student_exists(cursor, student_id):

                cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
                cursor.execute('DELETE FROM lessons WHERE student_id = ?', (student_id,))

                print("")
                print("Student deleted successfully.")

                conn.commit()

                try_again_main = False 

            else:
                print("")
                print("Student not found.")
                print("")

                while True:
                    try_again = input("Do you want to try enter the student id again? (yes/no): ").lower()

                    if try_again == 'yes':
                        break

                    elif try_again == 'no':
                        try_again_main = False  
                        break

                    else:
                        print("")
                        print("Invalid input. Please enter 'yes' or 'no'.")

        except ValueError:
            print("")
            print("Error in entering the student ID. Please make sure the value is a valid number.")


def update_student(cursor, conn):

    try_again_main = True

    while try_again_main:

        print("")
        print("To update student information:")
        print("")

        try:
            student_id = int(input("Please enter the student ID of the student you want update : "))

            if student_exists(cursor, student_id):

                new_info = get_student_input_for_update()

                if new_info:
                    
                    cursor.execute('''
                    UPDATE students
                    SET name=?, last_name=?, age=?, school_year=?, registration_date=?
                    WHERE id=?
                    ''', (*new_info[0:5], student_id))

                    cursor.execute('''
                    UPDATE lessons
                    SET lesson_name=?
                    WHERE student_id=?
                    ''', (new_info[-1].strip(), student_id))

                    conn.commit()

                    print("")
                    print("Updated successfully.")

                    try_again_main = False 
            else:
                print("")
                print("Student not found.")
                print("")
                while True:
                    try_again = input("Do you want to try enter the student id again? (yes/no): ").lower()

                    if try_again == 'yes':
                        break

                    elif try_again == 'no':
                        try_again_main = False 
                        break

                    else:
                        print("")
                        print("Invalid input. Please enter either 'yes' or 'no'.")

        except ValueError:
            print("")
            print("Error in entering the student ID. Please make sure the value is a valid number.")


def show_student(cursor):

    try_again_main = True

    while try_again_main:
        
        print("")
        print("To show student information:")
        print("")
        try:
            student_id = int(input("Please enter the student ID: "))

            if student_exists(cursor, student_id):
                cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))

                student_data = cursor.fetchone()

                print('''
    Student Information:
                      
    Student ID: {}
    Student Name: {}
    Student Last Name: {}
    Student Age: {}
    Student School year: {}
    Student Registration Date: {}
    '''.format(student_data[0], student_data[1], student_data[2], student_data[3], student_data[4], student_data[5]))

                cursor.execute('SELECT lesson_name FROM lessons WHERE student_id = ?', (student_id,))
                lessons_data = cursor.fetchall()

                if lessons_data:
                    lessons_list = [lesson[0] for lesson in lessons_data]
                    print("    Student Lessons: {}".format(', '.join(lessons_list)))
                else:
                    print("No lessons found.")

                try_again_main = False 
            else:
                print("")
                print("Student not found.")
                print("")

                while True:
                    try_again = input("Do you want to try enter the student id again? (yes/no): ").lower()

                    if try_again == 'yes':
                        break

                    elif try_again == 'no':
                        try_again_main = False  
                        break

                    else:
                        print("")
                        print("Invalid input. Please enter 'yes' or 'no'.")

        except ValueError:
            print("")
            print("Error in entering the student ID. Please make sure the value is a valid number.")


def main():
    
    conn, cursor = connect_database()

    while True:
        print("")
        print("Please choose the operation you want to perform :- ")
        print("")
        print("1- To add a student enter 'a' ")
        print("2- To delete a student enter 'd' ")
        print("3- To update student information enter 'u' ")
        print("4- To show student information enter 's' ")
        print("5- To exit program enter 'e' ")

        print("")
        choice = input("Please enter your choice : ")

        if choice == 'a':
            add_student(cursor, conn)
        elif choice == 'd':
            delete_student(cursor, conn)
        elif choice == 'u':
            update_student(cursor, conn)
        elif choice == 's':
            show_student(cursor)
        elif choice == 'e':
            print("Ok see you later , GoodBye !")
            conn.close()
            sys.exit()
        else:
            print("Invalid input , Please choose only from the options !")

        if choice == "e":
            break


if __name__ == "__main__":
    main()