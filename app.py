from flask import Flask, render_template, request, redirect
import sqlite3
import os

print("Current Path:", os.path.abspath(os.path.dirname(__file__)))
print("Templates Folder Exists:",
      os.path.exists(os.path.join(os.path.dirname(__file__), "templates")))
app = Flask(__name__, template_folder='templates')

def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS students(
        roll_no TEXT PRIMARY KEY,
        name TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS grades(
        roll_no TEXT,
        subject TEXT,
        marks INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO students VALUES (?,?)",
            (roll,name)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_student.html')

@app.route('/add_grades', methods=['GET','POST'])
def add_grades():
    if request.method == 'POST':
        roll = request.form['roll']
        subject = request.form['subject']
        marks = request.form['marks']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO grades VALUES (?,?,?)",
            (roll,subject,marks)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_grades.html')

@app.route('/view_student', methods=['GET','POST'])
def view_student():

    if request.method == 'POST':

        roll = request.form['roll']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE roll_no=?",
            (roll,)
        )

        student = cur.fetchone()

        cur.execute(
            "SELECT subject,marks FROM grades WHERE roll_no=?",
            (roll,)
        )

        grades = cur.fetchall()

        conn.close()

        avg = 0

        if grades:
            avg = sum([g[1] for g in grades]) / len(grades)

        return render_template(
            'view_student.html',
            student=student,
            grades=grades,
            average=avg
        )

    return render_template(
        'view_student.html',
        student=None
    )

if __name__ == '__main__':
    app.run(debug=True)
import os

print("Current Folder:", os.getcwd())
print("Templates Exists:", os.path.exists("templates"))
print("Files in templates:", os.listdir("templates"))
