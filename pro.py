import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sys

connection = psycopg2.connect('dbname=proyecto')

app = Flask(__name__)               
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fabian:12345@localhost:5432/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    edad = db.Column(db.Integer)
    carrera = db.Column(db.String())
    sexo = db.Column(db.String())
    curso1 = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso2 = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso3 = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso4 = db.Column(db.Integer, db.ForeignKey('curso.id'))
    def __repr__(self):
        return f'<Student: {self.id}, {self.name}, {self.password}, {self.edad}, {self.carrera}, {self.sexo}, {self.curso1}, {self.curso2}, {self.curso3}, {self.curso4}>'


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    edad = db.Column(db.Integer)
    carrera = db.Column(db.String())
    sexo = db.Column(db.String())
    curso_dictado = db.Column(db.Integer, db.ForeignKey('curso.id'))
    def __repr__(self):
        return f'<Teacher: {self.id}, {self.name}, {self.password}, {self.edad}, {self.carrera}, {self.sexo}, {self.curso_dictado}>'


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    duracion = db.Column(db.Integer)
    costo = db.Column(db.Integer)
    def __repr__(self):
        return f'<Curso: {self.id}, {self.name}, {self.duracion}, {self.costo}>'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/create')
def index0():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register/teacher')
def index2():
    teacher = Teacher.query.all()
    return render_template('teacher.html', data=teacher)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register/student')
def index1():
    student = Student.query.all()
    return render_template('student.html', data=student)

@app.route('/Student/create', methods=['POST'])
def create_student():
    try:
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        edad = request.form.get("edad", "")
        carrera = request.form.get("carrera", "")
        sexo = request.form.get("sexo", "")
        curso1 = request.form.get("curso1", "")
        curso2 = request.form.get("curso2", "")
        curso3 = request.form.get("curso3", "")
        curso4 = request.form.get("curso4", "")
        est1 = Student(name=name, password=password, edad=edad, carrera=carrera, sexo=sexo, curso1=curso1, curso2=curso2, curso3=curso3, curso4=curso4)

        db.session.add(est1)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index1'))

@app.route('/Teacher/create', methods=['POST'])
def create_teacher():
    try:
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        edad = request.form.get("edad", "")
        carrera = request.form.get("carrera", "")
        sexo = request.form.get("sexo", "")
        curso_dictado = request.form.get("curso_dictado", "")
        tea1 = Teacher(name=name,password=password, edad=edad, carrera=carrera, sexo=sexo, curso_dictado=curso_dictado)

        db.session.add(tea1)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index2'))



@app.route('/login/autenticate', methods=['GET', 'POST'])
def login_autenticate():
    if request.method == 'POST':
        username=request.form.get("name")
        password = request.form.get("password")
        stu= Student.query.filter_by(name=username)
        students = Student.query.all()
        teachers = Teacher.query.all()
        if stu.count()==0:
            a=[x for x in teachers if x.name == username][0]
            if a and a.password == password:
                return render_template('profile.html',identi=True,person=a)
            
            return redirect(url_for('login'))
        else:
            user=[x for x in students if x.name == username][0]
            if user and user.password == password:
                return render_template('profile.html',identi=False,person=user)
            return redirect(url_for('login'))
        return render_template('login.html')

@app.route('/update_stu/create/<id>', methods = ['GET', 'POST'])
def update_stu(id):
    password = request.form.get("password")
    carrera = request.form.get('carrera')
    curso1 = request.form.get('curso1')
    curso2 = request.form.get('curso2')
    curso3 = request.form.get('curso3')
    curso4 = request.form.get('curso4')

    cursor = connection.cursor()
    cursor.execute('select * from student where id = %s', (id))
    data = cursor.fetchall()
    cursor.execute("""
            UPDATE student
            SET password = %s,
                carrera = %s,
                curso1 = %s,
                curso2 = %s,
                curso3 = %s,
                curso4 = %s
                WHERE id = %s
            """, (password, carrera, curso1, curso2, curso3, curso4, id))
    connection.commit()
    cursor.close()
    return render_template('update_student.html', stu=data[0])


@app.route('/update_tea/create/<id>', methods = ['GET', 'POST'])
def update_tea(id):

    password = request.form.get('password')
    carrera = request.form.get('carrera')
    curso_dictado = request.form.get('curso_dictado')


    cursor = connection.cursor()
    cursor.execute('select * from teacher where id = %s', (id))
    data2 = cursor.fetchall()
    cursor.execute("""
            UPDATE teacher
            SET password = %s,
                carrera = %s,
                curso_dictado = %s
                WHERE id = %s
            """, (password, carrera, curso_dictado, id))
    connection.commit()
    cursor.close()
    return render_template('update_teacher.html', tea=data2[0])


@app.route('/delete/student/<id>', methods = ['POST','GET'])
def delete_student(id):
    cur = connection.cursor()
    cur.execute('DELETE FROM student WHERE id = {0}'.format(id))
    connection.commit()
    cur.close()
    return redirect(url_for('login'))


@app.route('/delete/teacher/<id>', methods = ['POST','GET'])
def delete_teacher(id):
    cur = connection.cursor()
    cur.execute('DELETE FROM teacher WHERE id = {0}'.format(id))
    connection.commit()
    cur.close()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


connection.close()


if __name__ == '__main__':
    app.run(debug=True)