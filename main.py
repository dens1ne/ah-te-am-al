from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import json
import random

app = Flask(__name__)
urls = ['https://million-wallpapers.ru/wallpapers/4/37/10737825692406921179/bolshoe-more-krasivyj-zakat.jpg',
        'https://gas-kvas.com/uploads/posts/2023-02/1675496354_gas-kvas-com-p-oboi-na-rabochii-stol-dlya-fonovogo-risunk-30.jpg',
        'https://wallpapers.com/images/hd/best-background-q6yyd1kpbb841wyl.jpg']


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



class LoginForm(FlaskForm):
    astronaut_id = StringField('ID астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = StringField('ID капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


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


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/systems')
    return render_template('login.html', title='Аварийный доступ', form=form)


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


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'random_key'
    app.run(port=8080, host='127.0.0.1')
