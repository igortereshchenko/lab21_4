from flask import Flask, flash, render_template, request, redirect, url_for
import sqlalchemy.sql as sql
from sqlalchemy import func
from dao.orm.entities import *
from dao.db import PostgresDb
from datetime import date
from forms.teacher_form import TeacherForm
from forms.group_form import GroupForm
from forms.subject_form import SubjectForm
from forms.car_form import CarForm
from forms.univer_form import UniverForm
from forms.work_form import Work1Form
from forms.search_group_form import GroupSearchForm
import json
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    db = PostgresDb()
    group_form = GroupSearchForm()
    group_form.init()

    pie_labels = []
    data = {
        "bar": []
    }

    for query, label in zip(*group_form.search(method=request.method)):

        if not query:
            continue

        groups, counts = zip(*query)
        pie = go.Pie(
            labels=[f'group = {group}' for group in groups],
            values=counts
        )
        data[label] = [pie]
        pie_labels.append(label)

    points = db.sqlalchemy_session.query(Subject.subj_name, Subject.subj_hours).distinct(
        Subject.subj_name, Subject.subj_hours).filter(Subject.subj_name != '').all()

    semester, final = zip(*points)
    bar = go.Scatter(
        x=semester,
        y=final,
        mode='markers'
    )

    data["bar"].append(bar)
    json_data = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', json=json_data, pie_labels=pie_labels, group_form=group_form)


@app.route('/teacher', methods=['GET'])
def index_teacher():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).all()

    return render_template('teacher.html', teachers=result)


@app.route('/new_teacher', methods=['GET', 'POST'])
def new_teacher():
    form = TeacherForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")
        else:

            teacher_obj = Teacher(
                teach_name=form.teacher_name.data,
                teach_faculty=form.teacher_faculty.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(teacher_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))

    return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")


@app.route('/edit_teacher', methods=['GET', 'POST'])
def edit_teacher():
    form = TeacherForm()

    if request.method == 'GET':

        teacher_id = request.args.get('teacher_id')
        db = PostgresDb()
        teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one()

        # fill form and send to user
        form.teacher_id.data = teacher_obj.teacher_id
        form.teacher_faculty.data = teacher_obj.teach_faculty
        form.teacher_name.data = teacher_obj.teach_name

        return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")

    else:
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="Edit teacher",
                                   action="edit_teacher")
        else:
            db = PostgresDb()
            # find professor
            teacher_obj = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id ==
                                                                          form.teacher_id.data).one()

            # update fields from form data
            teacher_obj.teacher_id = form.teacher_id.data
            teacher_obj.teach_faculty = form.teacher_faculty.data
            teacher_obj.teach_name = form.teacher_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_teacher'))


@app.route('/delete_teacher')
def delete_teacher():
    teacher_id = request.args.get('teacher_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Teacher).filter(Teacher.teacher_id == teacher_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_teacher'))


# END PROFESSOR ORIENTED QUERIES --------------------------------------------------------------------------------------

# STUDENT ORIENTED QUERIES --------------------------------------------------------------------------------------------


@app.route('/group', methods=['GET'])
def index_group():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Group).all()

    return render_template('group.html', groups=result)


@app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    form = GroupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('group_form.html', form=form, form_name="New group", action="new_group")
        else:
            group_obj = Group(
                group_faculty=form.group_faculty.data,
                group_name=form.group_name.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(group_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")


@app.route('/edit_group', methods=['GET', 'POST'])
def edit_group():
    form = GroupForm()

    if request.method == 'GET':

        group_id = request.args.get('group_id')
        db = PostgresDb()
        group = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to student
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name
        form.group_faculty.data = group.group_faculty

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")

    else:

        if not form.validate():
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:
            db = PostgresDb()
            # find student
            group = db.sqlalchemy_session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_faculty = form.group_faculty.data
            group.group_name = form.group_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_group'))


@app.route('/delete_group')
def delete_group():
    group_id = request.args.get('group_id')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Group).filter(Group.group_id == group_id).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_group'))


# END STUDENT ORIENTED QUERIES ----------------------------------------------------------------------------------------

# DISCIPLINE ORIENTED QUERIES ---------------------------------------------------------------------------------------

@app.route('/subject', methods=['GET'])
def index_subject():
    db = PostgresDb()

    subject = db.sqlalchemy_session.query(Subject).all()

    return render_template('subject.html', subjects=subject)


@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    form = SubjectForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('subject_form.html', form=form, form_name="New subject",
                                   action="new_subject")
        else:
            subject_obj = Subject(
                subj_name=form.subject_name.data,
                subj_faculty=form.subject_faculty.data,
                subj_hours=form.subject_hours.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(subject_obj)
            db.sqlalchemy_session.commit()

            return redirect(url_for('index_subject'))

    return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")


@app.route('/edit_subject', methods=['GET', 'POST'])
def edit_subject():
    form = SubjectForm()

    if request.method == 'GET':

        subject_faculty, subject_name = request.args.get('subj_faculty'), \
                                                                     request.args.get('subj_name')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        subject = db.sqlalchemy_session.query(Subject).filter(
            Subject.subj_faculty == subject_faculty,
            Subject.subj_name == subject_name).one()

        # fill form and send to discipline
        form.subject_faculty.data = subject.subj_faculty
        form.subject_name.data = subject.subj_name
        form.subject_hours.data = subject.subj_hours

        return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject")

    else:

        if not form.validate():
            return render_template('subject_form.html', form=form, form_name="Edit subject",
                                   action="edit_subject")
        else:
            db = PostgresDb()
            # find discipline
            subject = db.sqlalchemy_session.query(Subject).filter(
                Subject.subj_faculty == form.subject_faculty.data,
                Subject.subj_name == form.subject_name.data).one()

            # update fields from form data
            subject.subj_faculty = form.subject_faculty.data
            subject.subj_name = form.subject_name.data
            subject.subj_hours = form.subject_hours.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_subject'))


@app.route('/delete_subject')
def delete_subject():
    subject_faculty, subject_name = request.args.get('subj_faculty'), \
                                                                 request.args.get('subj_name')

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Subject).filter(
        Subject.subj_faculty == subject_faculty,
        Subject.subj_name == subject_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('index_subject'))


@app.route('/inserts', methods=['GET'])
def index_car():
    db = PostgresDb()

    car = db.sqlalchemy_session.query(Car).all()

    return render_template('car.html', cars=car)


@app.route('/new_car', methods=['GET'])
def new_car():
    car_obj = Car(
        model="A",
        color="green",
        numb=1234,
        manuf=100,
        teacher_id_fk=2
    )

    db = PostgresDb()
    db.sqlalchemy_session.add(car_obj)
    db.sqlalchemy_session.commit()
    return redirect(url_for('index_car'))


@app.route('/edit_car', methods=['GET', 'POST'])
def edit_car():
    form = CarForm()

    if request.method == 'GET':

        model = request.args.get('model')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        car = db.sqlalchemy_session.query(Car).filter(
            Car.model == model).one()

        # fill form and send to discipline
        form.model.data = car.model
        form.color.data = car.color
        form.numb.data = car.numb
        form.manuf.data = car.manuf
        form.teacher_id_fk.data = car.teacher_id_fk
        form.old_model.data = car.model

        return render_template('car_form.html', form=form, form_name="Edit car", action="edit_car")

    else:
        if not form.validate():
            return render_template('car_form.html', form=form, form_name="Edit car", action="edit_car")
        else:
            db = PostgresDb()
            # find discipline
            car = db.sqlalchemy_session.query(Car).filter(
                Car.model == form.old_model.data).one()

            # update fields from form data
            car.model = form.model.data
            car.color = form.color.data
            car.numb = form.numb.data
            car.manuf = form.manuf.data
            car.teacher_id_fk = form.teacher_id_fk.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_car'))


@app.route('/univer', methods=['GET'])
def index_univer():
    db = PostgresDb()

    univer = db.sqlalchemy_session.query(Univer).all()

    return render_template('univer.html', univers=univer)


@app.route('/new_univer', methods=['GET'])
def new_univer():
    univer_obj = Univer(
        name="KPI",
        addr="Polytech Street",
        counter=1000,
        teacher_id_fk=2
    )

    db = PostgresDb()
    db.sqlalchemy_session.add(univer_obj)
    db.sqlalchemy_session.commit()
    return redirect(url_for('index_univer'))


@app.route('/edit_univer', methods=['GET', 'POST'])
def edit_univer():
    form = UniverForm()

    if request.method == 'GET':

        name = request.args.get('name')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        univer = db.sqlalchemy_session.query(Univer).filter(
            Univer.name == name).one()

        # fill form and send to discipline
        form.name.data = univer.name
        form.addr.data = univer.addr
        form.counter.data = univer.counter
        form.teacher_id_fk.data = univer.teacher_id_fk
        form.old_name.data = univer.name

        return render_template('univer_form.html', form=form, form_name="Edit univer", action="edit_univer")

    else:
        if not form.validate():
            return render_template('univer_form.html', form=form, form_name="Edit univer", action="edit_univer")
        else:
            db = PostgresDb()
            # find discipline
            univer = db.sqlalchemy_session.query(Univer).filter(
                Univer.name == form.old_name.data).one()

            # update fields from form data
            univer.name = form.name.data
            univer.addr = form.addr.data
            univer.counter = form.counter.data
            univer.teacher_id_fk = form.teacher_id_fk.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_univer'))


@app.route('/show', methods=['GET'])
def index_work():
    db = PostgresDb()

    work = db.sqlalchemy_session.query(Work1).all()

    return render_template('work.html', works=work)


@app.route('/new_work', methods=['GET'])
def new_work():
    work_obj = Work1(
        name="AAA",
        company="Epam",
        salary=20000,
        subj_name_fk = "MATH",
        subj_faculty_fk = "AM",
        open_date = '2019-01-01'
    )

    db = PostgresDb()
    db.sqlalchemy_session.add(work_obj)
    db.sqlalchemy_session.commit()
    return redirect(url_for('index_work'))

@app.route('/edit_work', methods=['GET', 'POST'])
def edit_work():
    form = Work1Form()

    if request.method == 'GET':

        subj_faculty_fk, subj_name_fk = request.args.get('subj_faculty_fk'), \
                                        request.args.get('subj_name_fk')
        db = PostgresDb()

        # -------------------------------------------------------------------- filter for "and" google
        work = db.sqlalchemy_session.query(Work1).filter(
            Work1.subj_faculty_fk == subj_faculty_fk,
            Work1.subj_name_fk == subj_name_fk).one()

        # fill form and send to discipline
        form.name.data = work.name
        form.company.data = work.company
        form.salary.data = work.salary
        form.open_date.data = work.open_date
        form.subj_name_fk.data = work.subj_name_fk
        form.subj_faculty_fk.data = work.subj_faculty_fk
        form.old_subj_faculty_fk.data = work.subj_faculty_fk
        form.old_subj_name_fk.data = work.subj_name_fk

        return render_template('work_form.html', form=form, form_name="Edit work", action="edit_work")

    else:
        if not form.validate():
            return render_template('work_form.html', form=form, form_name="Edit work", action="edit_work")
        else:
            db = PostgresDb()
            # find discipline
            work = db.sqlalchemy_session.query(Work1).filter(
                Work1.subj_faculty_fk == form.old_subj_faculty_fk.data,
                Work1.subj_name_fk == form.old_subj_name_fk.data).one()

            # update fields from form data
            work.name = form.name.data
            work.company = form.company.data
            work.salary = form.salary.data
            work.open_date = form.open_date.data
            work.subj_name_fk = form.subj_name_fk.data
            work.subj_faculty_fk = form.subj_faculty_fk.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('index_univer'))
# END DISCIPLINE ORIENTED QUERIES -----------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
