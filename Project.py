import sqlite3
import sys

def connect_database():

    conn = sqlite3.connect('school.db')
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
        student_id INTEGER,
        lesson_name TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    ''')

    cursor.execute( '''
    SELECT students.id, students.name, students.last_name, students.age, students.school_year, students.registration_date, lessons.lesson_name
    FROM students
    INNER JOIN lessons ON students.id = lessons.student_id
''')

    conn.commit()
    return conn, cursor

def student_exists(cursor, student_id):

    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    return cursor.fetchone() is not None

def get_student_input():
    while True:
        try:
            student_id = int(input("Please enter the student ID : "))
            break 
        except ValueError:
            print("Sorry but please enter a numeric value only ! ")

    while True:
        try:
            name = input("Please enter the name : ")

            if name.isalpha():
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid input , Please make sure that the name contains letters only !")

    while True:
        try:
            last_name = input("Please enter the last Name : ")

            if last_name.isalpha():
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
            break
        except ValueError:
            print("Invalid input")

    while True:
        try:
            lesson_name = input("Please enter the lessons of the student : ")

            if lesson_name.isalpha():
                break
            else:
                raise ValueError
        except ValueError:
            print("Sorry but please make sure that the input contains letters")

        return student_id, name, last_name, age, school_year, registration_date, lesson_name

def add_student(cursor, conn):
    
    print("To add Student :- ")
    student_info = get_student_input()

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

            print("Student added successfully.")
            conn.commit()
        else:
            print("Student already exists.")

def delete_student(cursor, conn):
    
    print("To delete Student :- ")
    try:
            student_id = int(input("Please enter the student ID : "))

            if student_exists(cursor, student_id):
        
                cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))

                cursor.execute('DELETE FROM lessons WHERE student_id = ?', (student_id,))

                print("Student deleted successfully.")
                conn.commit()
            else:
                print("Student not found.")
    except ValueError:
            print("Error in entering the student ID. Please make sure the value is a valid number.")

def update_student(cursor, conn):
    
    print("To update student information :- ")
    try:
            student_id = int(input("Please enter the student ID : "))
            
            if student_exists(cursor, student_id):
            
                cursor.execute('SELECT * FROM students, lessons WHERE id = ?', (student_id,))
                student_data = cursor.fetchone()

                print(f"Student Information: {student_data}")

                new_info = get_student_input()

                if new_info:
                    cursor.execute('''
                    UPDATE students
                    SET name=?, last_name=?, age=?, school_year=?, registration_date=?
                    WHERE id=?
                    ''', (*new_info[1:-1], student_id))

                    cursor.execute('''
                    UPDATE lessons
                    SET lesson_name=?
                    WHERE student_id=?
                    ''', (new_info[-1].strip(), student_id))

                    print("Updated successfuly.")
                    conn.commit()

            else:
                print("Student not found.")
    except ValueError:
            print("Error in entering the student ID. Please make sure the value is a valid number.")
        
def show_student(cursor):

    print("To show student information :- ")
    try:
        student_id = int(input("Please enter the student ID : "))

        if student_exists(cursor, student_id):
            
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student_data = cursor.fetchone()

            print('''

            ''')
            print("Student Information :- ")
            print("")
            print(f"Student ID: {student_data[0]}")
            print(f"Name: {student_data[1]}")
            print(f"Last Name: {student_data[2]}")
            print(f"Age: {student_data[3]}")
            print(f"School year: {student_data[4]}")
            print(f"Registration Date: {student_data[5]}")

            cursor.execute('SELECT lesson_name FROM lessons WHERE student_id = ?', (student_id,))
            lessons_data = cursor.fetchall()

            if lessons_data:
                lessons_list = [lesson[0] for lesson in lessons_data]
                print(f"Lessons: {', '.join(lessons_list)}")
            else:
                print("No lessons found.")

        else:
            print("Student not found.")
    except ValueError:
            print("Error in entering the student ID. Please make sure the value is a valid number.")
        
def main():
    conn, cursor = connect_database()

    while True:

        print('''

        ''')
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