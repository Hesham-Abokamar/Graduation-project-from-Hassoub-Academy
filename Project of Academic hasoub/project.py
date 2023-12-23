import sqlite3

connect = sqlite3.connect('student.db')
cursor = connect.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    last_name TEXT,
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

connect.commit()

def add_student():

    print("To add a new student :- ")
    print("")
    student_id = int(input("Please enter the Student id : "))
    name = input("Please Enter the name of the student : ")
    last_name = input("Please Enter the last name of the student : ")
    age = int(input("Please Enter the age of the student : "))
    grade = int(input("Please Enter the grade of the student : "))
    registration_date = input("Please Enter the date of registration : ")

    cursor.execute('''
    INSERT INTO students (id, name, last_name, age, grade, registration_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, name, last_name, age, grade, registration_date))

    print("")
    lessons = input("Please enter the Lessons you want to add : ").split('-')
    for lesson in lessons:
        cursor.execute('''
        INSERT INTO lessons (student_id, lesson_name)
        VALUES (?, ?)
        ''', (student_id, lesson.strip()))

    print("Added successfully !")
    connect.commit()

def delete_student():

    print("")
    print("To delete a student :- ")
    print("")
    student_id = int(input("Please Enter the student id : "))

    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))

    cursor.execute('DELETE FROM lessons WHERE student_id = ?', (student_id,))

    print("")
    print("Deleted successfully ! ")
    connect.commit()

def update_student():
    
    print("")
    print("To update the student information :- ")
    print("")
    student_id = int(input("Please enter the student id : "))

    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student_data = cursor.fetchone()

    if student_data:
        print("Please record the information you would like to update :- ")
        print("name : ", student_data[1])
        print("last name : ", student_data[2])
        print("age : ", student_data[3])
        print("grade : ", student_data[4])
        print("registration_date : ", student_data[5])

        print("")
        name = input("Please enter the new name : ") or student_data[1]
        last_name = input("Please enter the new last name : ") or student_data[2]
        age = int(input("Please enter the new age : ")) or student_data[3]
        grade = int(input("Please enter the new grade : ")) or student_data[4]
        registration_date = int(input("Please enter the new registration date : ")) or student_data[5]
        print("")

        cursor.execute('''
        UPDATE students
        SET name=?, last_name=?, age=?, grade=?
        WHERE id=?
        ''', (name, last_name, age, grade, registration_date, student_id))

        print("Updated successfully !")
        connect.commit()
    else:
        print("The student is not present !")
        print("")

def show_student():
    
    print("")
    print("To show student's information :- ")
    student_id = int(input("Please enter the student id : "))

    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student_data = cursor.fetchone()

    if student_data:
        print("student information : ")
        print("name : ", student_data[1])
        print("last name : ", student_data[2])
        print("age : ", student_data[3])
        print("grade : ", student_data[4])
        print("registration date : ", student_data[5])

        cursor.execute('SELECT lesson_name FROM lessons WHERE student_id = ?', (student_id,))
        lessons_data = cursor.fetchall()

        if lessons_data:
            print("Lessons that the student participated in : ")
            for lesson in lessons_data:
                print("")
                print("-", lesson[0])
        else:
            print("There are no lessons in which the student has participated !")
    else:
        print("The student is not present ! ")

while True:

    print("")
    print("")
    print("Welcome to the system for school students ! ")
    print('''
    This is a list of the things that you can do :-
      
        1- If you want to add students enter "a"
        2- If you want to delete a student enter "d"
        3- If you want to update information of a student enter "u"
        4- If you want to show information of a student enter "s"
        5- If you want to exit the program enter "e"
          
    ''')
    choice = input("Please enter your choice : ")
    if choice == "a":
        add_student()
    elif choice == "d":
        delete_student()
    elif choice == "u":
        update_student()
    elif choice == "s":
        show_student()
    elif choice == "e":
        print("Ok see you later , Good Bye !")
        break
    else:
        print("Please enter from ('a', 'd', 'u', 's', 'e') only !")