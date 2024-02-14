from flask import Flask, render_template, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=8080, host='127.0.0.1')
