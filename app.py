from flask import Flask, render_template, request, redirect, url_for
from source.dao.orm.entities import *
from source.dao.db import PostgresDb
from datetime import date
from source.dao.data import *
from source.forms.new_form import TableForm
from source.forms.professor_form import ProfessorForm
from source.forms.student_form import StudentForm
from source.forms.discipline_form import DisciplineForm
from source.forms.search_student_form import StudentSearchForm
from source.forms.search_student_record_from import StudentSearchRecordForm
import json
import plotly
import plotly.graph_objs as go
import os
from sqlalchemy import func


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "jkm-vsnej9l-vm9sqm3:lmve")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{host}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/get', methods=['GET'])
def index_show():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Univer).all()

    return render_template('new.html', univers=result)


@app.route('/edit_table', methods=['GET', 'POST'])
def edit_table():
    form = TableForm()

    if request.method == 'GET':

        id = request.args.get('id')

        db = PostgresDb()
        table_obj = db.sqlalchemy_session.query(Univer).filter(Univer.id == id).one()

        # fill form and send to user
        form.id.data = id
        form.name.data = table_obj.name
        form.address.data = table_obj.address
        form.year.data = table_obj.year
        form.degree.data = table_obj.degree

        return render_template('new_form.html', form=form, form_name="Edit ", action="edit_table")

    else:
        if not form.validate():
            # form.job_name.errors.append('vova')
            return render_template('new_form.html', form=form, form_name="Edit",
                                   action="edit_table")
        else:
            if form.year.data.year < 2000 or form.year.data.year > 2019:
                form.year.errors.append('year shoud be in interval [2000-2019]')
                return render_template('new_form.html', form=form, form_name="Edit",
                                       action="edit_table")

            db = PostgresDb()

            table_obj = db.sqlalchemy_session.query(Univer).filter(Univer.id == form.id.data).one()

            # update fields from form data
            table_obj.name = form.name.data
            table_obj.address = form.address.data
            table_obj.year = form.year.data
            table_obj.degree = form.degree.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_show'))


@app.route('/map', methods=['GET'])
def install():
    db = PostgresDb()

    uni1 = Univer(name="new_uni_1",
                  address="new_uni_1",
                  year=date.today(),
                  degree="uni")

    uni2 = Univer(name="new_uni_2",
                  address="new_uni_2",
                  year=date.today(),
                  degree="uni")

    uni3 = Univer(name="new_uni_3",
                  address="new_uni_3",
                  year=date.today(),
                  degree="uni")

    session = db.sqlalchemy_session
    session.add_all([uni1, uni2, uni3])
    session.commit()

    # delete from "Univer" where id=4;
    # delete from "Univer" where id=5;
    # delete from "Univer" where id=6;

    return redirect(url_for('root'))


@app.route('/plot', methods=['GET', 'POST'])
def plot():
    pie_labels = []
    data = {}
    db = PostgresDb()

    # scatter plot ---------------------------------------------------------------------------------------------------
    query = db.sqlalchemy_session.query(func.count(Univer.id), Univer.year).group_by(Univer.year).all()

    count_uni, year = zip(*query)

    bar = go.Scatter(
        x=year,
        y=count_uni
        # mode='markers'
    )

    data["bar"] = [bar]

    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot.html', json=json_data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    pie_labels = []
    data = {}

    # pie plot -------------------------------------------------------------------------------------------------------
    student_form = StudentSearchForm()
    student_form.init()

    for query, label in zip(*student_form.search(method=request.method)):

        if not query:
            continue

        groups, counts = zip(*query)
        pie = go.Pie(
            labels=[f'group = {group}' for group in groups],
            values=counts
        )
        data[label] = [pie]
        pie_labels.append(label)

    # scatter plot ---------------------------------------------------------------------------------------------------
    record_book_form = StudentSearchRecordForm()
    record_book_form.init()

    return_val = record_book_form.search(method=request.method)
    if return_val:
        semester, final = zip(*return_val)
        bar = go.Scatter(
            x=semester,
            y=final,
            mode='markers'
        )

        data["bar"] = [bar]

    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', json=json_data, pie_labels=pie_labels, student_form=student_form,
                           record_book_form=record_book_form)


# PROFESSOR ORIENTED QUERIES ------------------------------------------------------------------------------------------


@app.route('/professor', methods=['GET'])
def index_professor():
    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Professor).all()
    else:
        deleted = False
        result = db.sqlalchemy_session.query(Professor).filter(Professor.professor_date_expelled == None).all()

    return render_template('professor.html', professors=result, deleted=deleted)


@app.route('/new_professor', methods=['GET', 'POST'])
def new_professor():
    form = ProfessorForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('professor_form.html', form=form, form_name="New professor", action="new_professor")
        else:

            professor_obj = Professor(
                professor_university=form.professor_university.data,
                professor_department=form.professor_department.data,
                professor_name=form.professor_name.data,
                professor_surname=form.professor_surname.data,
                professor_birthday=form.professor_birthday.data,
                professor_date_enrollment=form.professor_date_enrollment.data.strftime("%d-%b-%y"),
                professor_degree=form.professor_degree.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(professor_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_professor'))

    return render_template('professor_form.html', form=form, form_name="New professor", action="new_professor")


@app.route('/edit_professor', methods=['GET', 'POST'])
def edit_professor():
    form = ProfessorForm()

    if request.method == 'GET':

        professor_id = request.args.get('professor_id')
        db = PostgresDb()
        professor_obj = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id == professor_id).one()

        # fill form and send to user
        form.professor_id.data = professor_obj.professor_id
        form.professor_university.data = professor_obj.professor_university
        form.professor_department.data = professor_obj.professor_department
        form.professor_name.data = professor_obj.professor_name
        form.professor_surname.data = professor_obj.professor_surname
        form.professor_birthday.data = professor_obj.professor_birthday
        form.professor_date_enrollment.data = professor_obj.professor_date_enrollment
        form.professor_degree.data = professor_obj.professor_degree

        return render_template('professor_form.html', form=form, form_name="Edit professor", action="edit_professor")

    else:
        if not form.validate():
            return render_template('professor_form.html', form=form, form_name="Edit professor",
                                   action="edit_professor")
        else:
            db = PostgresDb()
            # find professor
            professor_obj = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id ==
                                                                          form.professor_id.data).one()

            # update fields from form data
            professor_obj.professor_id = form.professor_id.data
            professor_obj.professor_university = form.professor_university.data
            professor_obj.professor_department = form.professor_department.data
            professor_obj.professor_name = form.professor_name.data
            professor_obj.professor_surname = form.professor_surname.data
            professor_obj.professor_birthday = form.professor_birthday.data
            professor_obj.professor_date_enrollment = form.professor_date_enrollment.data.strftime("%d-%b-%y")
            professor_obj.professor_degree = form.professor_degree.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_professor'))


@app.route('/delete_professor')
def delete_professor():
    professor_id = request.args.get('professor_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Professor).filter(Professor.professor_id == professor_id).one()

    result.professor_date_expelled = date.today()
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_professor'))


# END PROFESSOR ORIENTED QUERIES --------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/student', methods=['GET'])
def index_student():
    db = PostgresDb()

    deleted = request.args.get('deleted')

    if deleted:
        result = db.sqlalchemy_session.query(Student).all()
    else:
        deleted = False
        result = db.sqlalchemy_session.query(Student).filter(Student.student_date_expelled == None).all()

    return render_template('student.html', students=result, deleted=deleted)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            student_obj = Student(
                student_university=form.student_university.data,
                student_faculty=form.student_faculty.data,
                student_group=form.student_group.data,
                student_name=form.student_name.data,
                student_surname=form.student_surname.data,
                student_birthday=form.student_birthday.data,
                student_date_enrollment=form.student_date_enrollment.data.strftime("%d-%b-%y"))

            db = PostgresDb()
            db.sqlalchemy_session.add(student_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = StudentForm()

    if request.method == 'GET':

        student_id = request.args.get('student_id')
        db = PostgresDb()
        student = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()

        # fill form and send to student
        form.student_id.data = student.student_id
        form.student_name.data = student.student_name
        form.student_surname.data = student.student_surname
        form.student_group.data = student.student_group
        form.student_university.data = student.student_university
        form.student_faculty.data = student.student_faculty
        form.student_birthday.data = student.student_birthday
        form.student_date_enrollment.data = student.student_date_enrollment

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")

    else:

        if not form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            db = PostgresDb()
            # find student
            student = db.sqlalchemy_session.query(Student).filter(Student.student_id == form.student_id.data).one()

            # update fields from form data
            student.student_id = form.student_id.data
            student.student_university = form.student_university.data
            student.student_faculty = form.student_faculty.data
            student.student_group = form.student_group.data
            student.student_name = form.student_name.data
            student.student_surname = form.student_surname.data
            student.student_birthday = form.student_birthday.data
            student.student_date_enrollment = form.student_date_enrollment.data.strftime("%d-%b-%y")

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_student'))


@app.route('/delete_student')
def delete_student():
    student_id = request.args.get('student_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Student).filter(Student.student_id == student_id).one()
    result.student_date_expelled = date.today()

    db.sqlalchemy_session.commit()

    return redirect(url_for('index_student'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# DISCIPLINE ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/discipline', methods=['GET'])
def index_discipline():
    db = PostgresDb()

    discipline = db.sqlalchemy_session.query(Discipline).all()

    return render_template('discipline.html', disciplines=discipline)


@app.route('/new_discipline', methods=['GET', 'POST'])
def new_discipline():
    form = DisciplineForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="New discipline",
                                   action="new_discipline")
        else:
            discipline_obj = Discipline(
                discipline_university=form.discipline_university.data,
                discipline_faculty=form.discipline_faculty.data,
                discipline_name=form.discipline_name.data,
                discipline_exam=form.discipline_exam.data,
                univ_fk=1,
                discipline_hours_for_semester=form.discipline_hours_for_semester.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(discipline_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")


@app.route('/edit_discipline', methods=['GET', 'POST'])
def edit_discipline():
    form = DisciplineForm()

    if request.method == 'GET':

        discipline_university, discipline_faculty, discipline_name = request.args.get('discipline_university'), \
                                                                     request.args.get('discipline_faculty'), \
                                                                     request.args.get('discipline_name')
        db = PostgresDb()

        discipline = db.sqlalchemy_session.query(Discipline).filter(
            Discipline.discipline_university == discipline_university,
            Discipline.discipline_faculty == discipline_faculty,
            Discipline.discipline_name == discipline_name).one()

        # fill form and send to discipline
        form.discipline_university.data = discipline.discipline_university
        form.discipline_faculty.data = discipline.discipline_faculty
        form.discipline_name.data = discipline.discipline_name
        form.discipline_exam.data = discipline.discipline_exam
        form.discipline_hours_for_semester.data = discipline.discipline_hours_for_semester

        return render_template('discipline_form.html', form=form, form_name="Edit discipline", action="edit_discipline")

    else:

        if not form.validate():
            return render_template('discipline_form.html', form=form, form_name="Edit discipline",
                                   action="edit_discipline")
        else:
            db = PostgresDb()
            # find discipline
            discipline = db.sqlalchemy_session.query(Discipline).filter(
                Discipline.discipline_university == form.discipline_university.data,
                Discipline.discipline_faculty == form.discipline_faculty.data,
                Discipline.discipline_name == form.discipline_name.data).one()

            # update fields from form data
            discipline.discipline_university = form.discipline_university.data
            discipline.discipline_faculty = form.discipline_faculty.data
            discipline.discipline_name = form.discipline_name.data
            discipline.discipline_exam = form.discipline_exam.data
            discipline.discipline_hours_for_semester = form.discipline_hours_for_semester.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_discipline'))


@app.route('/delete_discipline')
def delete_discipline():
    discipline_university, discipline_faculty, discipline_name = request.args.get('discipline_university'), \
                                                                 request.args.get('discipline_faculty'), \
                                                                 request.args.get('discipline_name')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Discipline).filter(
        Discipline.discipline_university == discipline_university,
        Discipline.discipline_faculty == discipline_faculty,
        Discipline.discipline_name == discipline_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_discipline'))


# END DISCIPLINE ORIENTED QUERIES -----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
