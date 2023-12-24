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
        grade INTEGER,
        registration_date INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        student_id INTEGER,
        lesson_name TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
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
            name = input("Please enter the name : ")
            last_name = input("Please enter the last Name : ")
            age = int(input("Please enter the age : "))
            grade = int(input("Please enter the grade : "))
            registration_date = int(input("Please enter the registration Date : "))
            lesson_name = input("Please enter the lessons : ")

            return student_id, name, last_name, age, grade, registration_date, lesson_name
        except ValueError:
            print("Error in input. Please make sure all values are true !")

def add_student(cursor, conn):
    
    print("To add Student :- ")
    student_info = get_student_input()

    if student_info:
        student_id, name, last_name, age, grade, registration_date, lesson_name = student_info

        if not student_exists(cursor, student_id):
            
            cursor.execute('''
            INSERT INTO students (id, name, last_name, age, grade, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, last_name, age, grade, registration_date))

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
            
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student_data = cursor.fetchone()

            print(f"Student Information: {student_data}")

            new_info = get_student_input()

            if new_info:
                cursor.execute('''
                UPDATE students
                SET name=?, last_name=?, age=?, grade=?, registration_date=?
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
            print(f"Grade: {student_data[4]}")
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