from tkinter import Image

from flask import Flask, render_template, redirect, request, make_response, session, jsonify, abort
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, BooleanField
from wtforms.validators import DataRequired, Email, NumberRange
import json
import random
from data import db_session
from data.jobs import Job
from data.users import User
from data.department import Department
import datetime
import requests

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

urls = ['https://million-wallpapers.ru/wallpapers/4/37/10737825692406921179/bolshoe-more-krasivyj-zakat.jpg',
        'https://gas-kvas.com/uploads/posts/2023-02/1675496354_gas-kvas-com-p-oboi-na-rabochii-stol-dlya-fonovogo-risunk-30.jpg',
        'https://wallpapers.com/images/hd/best-background-q6yyd1kpbb841wyl.jpg']

db_session.global_init('db/database.db')
db_sess = db_session.create_session()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id: int):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/<title>')
@app.route('/index/<title>')
def index(title: str = 'Миссия Колонизация Марса'):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof: str):
    return render_template('training.html', title='НУЖНО БОЛЬШЕ ТРЕНИРОВАТЬСЯ', prof=prof)


@app.route('/list_prof/<ltype>')
def list_prof(ltype: str):
    profs = ''' менеджер по продажам,
                продавец-консультант,
                водитель,
                бухгалтер,
                программист, разработчик программного обеспечения,
                врач,
                инженер,
                повар,
                упаковщик и комплектовщик,
                слесарь,
                сантехник'''
    profs = profs.strip().split(',')
    return render_template(
        'prof_list.html', title='Профессии, которым НУЖНО БОЛЬШЕ ТРЕНИРОВАТЬСЯ', profs=profs, ltype=ltype)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    data = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'Выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', **data)


# class LoginForm(FlaskForm):
#     astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
#     astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
#     captain_id = StringField('ID капитана', validators=[DataRequired()])
#     captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
#     submit = SubmitField('Доступ')


"""
мистэ прэзэднт вот а ю финк эбаут дииз натс?..
диз- натс? хе хэд но шэнс, ноу шэнс эд олл. хи майт кол химселф натс бат хи ивен хэд нот болз.
лайф эинт изи фо э  биилльаниа сан: ю нид то ворк хард то гет а лилл сам-сам .
хэй, ду ю финк ай м дамб? ай форгот, зере воз самфинг абаут джамп
ай лав чайна! зей дид самфинг грэйт бифо! тугезер, америка, ви вил билд а грэйтер вол.
хэллоу, айм электед, ай вилл мэйк ас грейт. ай стартед фром зе ботом оф май фазерс товерс виз
э смол лоан оф а уан биллион даларс. ит воз а страгл. йэ.
ййэ
фэнкс фор электинг ми, хере из йоур квортер "эвсом!"

фол ол зе лузеес энд хэйтерс ху сэй ай вор э... воревиг

энд бикоз оф зет некст стэйдж оф афэйрс вил инклюд йоур маза
"""


# @app.route('/login')
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect('/systems')
#     return render_template('login_task.html', title='Аварийный доступ', form=form)


@app.route('/systems')
def systems():
    return '* звуки работающей системы *'


@app.route('/distribution')
def destribution():
    astronauts = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', title='Размещение', astronauts=astronauts)


@app.route('/table/<sex>/<int:age>')
def table(sex: str, age: int):
    return render_template('mars_table.html', title='Оформление кают', sex=sex, age=age)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    if request.method == 'POST':
        f = request.files['file']
        with open(f'static/img/test_image_{len(urls) - 3}.png', 'wb') as img_file:
            img_file.write(f.read())
        urls.append(f'static/img/test_image_{len(urls) - 3}.png')

    return render_template('galery.html', title='Галерея с добавлением', urls=urls)
    

@app.route('/member')
def member():
    with open('templates/comand.json') as jfile:
        astronauts = json.load(jfile)

    return render_template('member.html', title='Участник команды', astronauts=astronauts, random=random)


class RegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(1, 150)])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Работа', validators=[DataRequired()])
    address = StringField('Модуль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()

    return render_template('register.html', form=form)


@app.route('/')
def works_log():
    jobs = db_sess.query(Job).all()
    return render_template('jobs.html', title='Журнал работ', jobs=jobs)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/')

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               current_user=current_user)
    return render_template('login.html', title='Авторизация', form=form)


class JobForm(FlaskForm):
    team_leader_id = IntegerField('ID лидера', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Время на работу в часах', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    start_date = DateField('Дата начала работ', format='%Y-%m-%d')
    end_date = DateField('Дата конца работ', format='%Y-%m-%d')
    is_finished = BooleanField('Работа завершена?', default=False)
    submit = SubmitField("Готово")


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief_id = IntegerField('ID лидера', validators=[DataRequired()])
    members = StringField('Жители', validators=[DataRequired()])
    email = StringField('Почта', validators=[Email(), DataRequired()])
    submit = SubmitField("Готово")


@app.route("/job", methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Job()
        job.team_leader_id = form.team_leader_id.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = datetime.datetime.strptime(f'{form.start_date.data} 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
        job.end_date = datetime.datetime.strptime(f'{form.end_date.data} 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()

        return redirect('/')

    return render_template('add_job.html', title="Добавить работу", form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id: int):
    form = JobForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Job).filter(Job.id == id).first()
        else:
            job = db_sess.query(Job).filter(Job.id == id,
                                                 Job.team_leader == current_user).first()

        if job:
            form.team_leader_id.data = job.team_leader_id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Job).filter(Job.id == id).first()
        else:
            job = db_sess.query(Job).filter(Job.id == id,
                                            Job.team_leader == current_user).first()

        if job:
            job.team_leader_id = form.team_leader_id.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('add_job.html', title='Изменить работу', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id: int):
    db_sess = db_session.create_session()

    if current_user.id == 1:
        job = db_sess.query(Job).filter(Job.id == id).first()
    else:
        job = db_sess.query(Job).filter(Job.id == id,
                                        Job.team_leader == current_user).first()

    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/')


@app.route('/user_show/<int:id>')
def user_show(id: int):
    user = requests.get(f'http://127.0.0.1:5000/api/users/{id}').json()
    print(user)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": user['city_from'],
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    map_params = {
        "apikey": 'be02e27d-583b-4aad-b55e-9787d9d25384',
        "z": 10,
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "l": "map"
    }
    map_api_server = "https://static-maps.yandex.ru/v1?"
    response = requests.get(map_api_server, params=map_params)

    with open('static/img/temp_image.jpg', 'wb') as image_file:
        image_file.write(response.content)

    return render_template('nostalgy.html', title='Ностальгия', user=user)


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html', title='Департаменты', departments=departments)


@app.route('/add_departments', methods=['GET', 'POST'])
@login_required
def add_departments():
    form = DepartmentForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief_id = form.chief_id.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()

        return redirect('/departments')

    return render_template('add_departments.html', title="Добавить департамент", form=form)


@app.route('/edit_departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id: int):
    form = DepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == id).first()
        else:
            department = db_sess.query(Job).filter(Department.id == id,
                                                 Department.chief == current_user).first()

        if department:
            form.title.data = department.title
            form.chief_id.data = department.chief_id
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            department = db_sess.query(Department).filter(Department.id == id).first()
        else:
            department = db_sess.query(Job).filter(Department.id == id,
                                                   Department.chief == current_user).first()

        if department:
            department.title = form.title.data
            department.chief_id = form.chief_id.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)

    return render_template('add_departments.html', title='Изменить департамент', form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id: int):
    db_sess = db_session.create_session()

    if current_user.id == 1:
        department = db_sess.query(Department).filter(Department.id == id).first()
    else:
        department = db_sess.query(Job).filter(Department.id == id,
                                               Department.chief == current_user).first()

    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/departments')


if __name__ == '__main__':
    from data import api_jobs, api_users
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'random_key'
    app.register_blueprint(api_jobs.blueprint)
    app.run(port=5000, host='127.0.0.1')
