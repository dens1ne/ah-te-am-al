from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title: str = 'Миссия Колонизация Марса'):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof: str):
    if 'инженер' in prof or 'строитель' in prof:
        img = url_for('static', filename='img/iiiite.jpg')
    else:
        img = url_for('static', filename='img/anas.jpg')

    return render_template('training.html', title='НУЖНО БОЛЬШЕ ТРЕНИРОВАТЬСЯ', prof=prof, img=img)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=8080, host='127.0.0.1')
