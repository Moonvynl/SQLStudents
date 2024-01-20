import sqlite3

db = sqlite3.connect('university.db')

db.execute('''CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        age INTEGER,
        major VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS courses(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name VARCHAR(50),
        instructor VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS student_course(
        student_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id));''')


def add_user(db, name, age, major):
    db.execute(f'''INSERT INTO students(name, age, major)
            VALUES  (?, ?, ?)''', (name, age, major))
    db.commit()
    

def add_course(db, course_name, instructor):
    db.execute(f'''INSERT INTO courses(course_name, instructor)
            VALUES  (?, ?)''', (course_name, instructor))
    db.commit()

def add_to_student_course(db, student_id, course_id):
    db.execute(f'''INSERT INTO student_course(student_id, course_id)
            VALUES  (?, ?)''', (student_id, course_id))
    db.commit()

def get_students(db):
    return [f"i\n" for i in db.execute('''SELECT * FROM students''')]

def get_courses(db):
    return [f"i\n" for i in db.execute('''SELECT * FROM courses''')]


def get_student_courses(db, course_id):
    # courses_ids = db.execute(f'''SELECT student_id FROM student_course WHERE course_id == {course_id}''')
    # students = [db.execute(f'''SELECT * FROM students WHERE id == {i}''') for i in courses_ids]
    # return students
    return [i for i in db.execute(f'SELECT name FROM students WHERE id = (SELECT student_id FROM student_course WHERE course_id = {course_id})')]


while True:
    print("\n1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Показати список студентів")
    print("4. Показати список курсів")
    print("5. Зареєструвати студента на курс")
    print("6. Показати студентів на конкретному курсі")
    print("7. Вийти")

    choice = input("Оберіть опцію (1-7): ")
    
    match choice:
        case "1":
            name = input("Введіть ім'я студента:")
            age = int(input("Введіть вік студента:"))
            major = input("Введіть дисципліну студента:")
            add_user(db, name, age, major)
            print(f"Студент {name} успішно доданий")
        case "2":
            name = input("Введіть ім'я курсу:")
            instructor = input("Введіть вчителя курсу:")
            add_course(db, name, instructor)
            print(f"Курс {name} успішно створений")
        case "3":
            print("Ось список студентів:",get_students(db))
        case "4":
            print("Ось список курсів:", get_courses(db))
        case "5":
            student_id = int(input("Введіть id студента"))
            course_id = int(input("Введіть id курсу"))
            add_to_student_course(db, student_id, course_id)
            print("YAY")
        case "6":
            course_id = int(input("Введіть айді курса:"))
            selected_course = db.execute(f'SELECT course_name FROM courses WHERE course_id == {course_id}')
            print(f'На курсі {[i for i in selected_course.fetchone()]} знаходяться учні:')
            print(get_student_courses(db, course_id))
        case "7":
            break
        case _:
            print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")
