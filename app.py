from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, Response, jsonify
import config
from werkzeug.routing import BaseConverter

app = Flask(__name__)
# app.config.from_object(config)
app.config.from_pyfile('config.py', silent=True)

class TemplatePhoneConverter(BaseConverter):
    regex = r'1[583746]\d{9}'

app.url_map.converters['tel'] = TemplatePhoneConverter

class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ = None):
        if (isinstance(response, dict)):
            response = jsonify(response)
        # print(response)
        # print(type(response))
        return super(JSONResponse, cls).force_type(response, environ)
    
app.response_class = JSONResponse

@app.route('/')
def index():
    return render_template('index.html', username = 'admin')

@app.route('/list/')
def list():
    return 'list'

@app.route('/article/<int:id>/')
def article(id):
    return 'article id %s' % id

# @app.route('/<any(blog, user): url_path>/<id>/')
# def detail(url_path, id):
#     if url_path == 'blog':
#         return 'detail id %s' % id
#     else:
#         return 'user id %s' % id

# 以?a=b方式传参    
@app.route('/d/<tel:tel_id>/')
def d(tel_id):
    # wd = request.args.get('wd')
    return 'd tel %s' % tel_id

# @app.route('/login/', methods = ['POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         return 'success'

@app.route('/login/<id>')
def login(id):
    print(id)
    return 'login page'

@app.route('/profile/')
def profile():
    name = request.args.get('name')
    if name:
        return 'profile page'
    else:
        return redirect(url_for('login'), code = 302)
    
@app.route('/list2/')
def list2():
    return {'username': 'koa', 'age': 18}

@app.route('/page/')
def page():
    content = {
        'username': 'koa',
        'age': 15,
        'sex': 'male',
        'created_at': datetime(2023, 9, 7, 22, 50, 30),
        'members': [
            'koa',
            'koa2',
            'egg',
            'express',
            'hapi'
        ]
    }
    return render_template('page.html', **content)

@app.template_filter('handle_time')
def handle_time(time):
    if isinstance(time, datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return '刚刚'
        elif timestamp >= 60 and timestamp < 60 * 60:
            minutes = timestamp / 60
            return '%s分钟前' % int(minutes)
        elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
            hours = timestamp / 60 / 60
            return '%s小时前' % int(hours)
        elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
            month = timestamp / 60 / 60 / 24
            return '%s天前' % int(month)
        else:
            return time.strftime('%y/%m/%d %H:%M')
    else:
        return time
    
@app.route('/count')
def count():
    return render_template('count.html', username = 'koa')
    
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
