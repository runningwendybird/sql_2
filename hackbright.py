import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])


def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Max Grade: %s"""%(row[0], row[1], row[2])

def get_grade_by_project(title):
    query = """SELECT students.first_name, students.last_name, Projects.title, grades.grade,Projects.max_grade
                FROM Students
                INNER JOIN Grades
                ON students.github = grades.student_github
                INNER JOIN Projects
                ON Grades.project_title = Projects.title
                WHERE title = ?"""
    DB.execute(query, (title,))
    rows = DB.fetchall()

    for row in rows:
        print """\
        Student: %s %s
        Project: %s
        Grade: %d out of %d\n"""%(row[0], row[1], row[2], row[3], row[4])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added %s project." % (title)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(',')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args)
        if command == "project":
            get_project_by_title(*args)
        if command == "new_project":
            make_new_project(*args)
        if command == "grade":
            get_grade_by_project(*args)
        elif command == "new_student":
            make_new_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()