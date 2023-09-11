from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, Response, jsonify
import config
from werkzeug.routing import BaseConverter

movies = [
    {
        'id': '123',
        'thumbling': 'https://gimg3.baidu.com/search/src=http%3A%2F%2Fpics1.baidu.com%2Ffeed%2Fdc54564e9258d109dad324a26e0b09b36c814d4a.jpeg%40f_auto%3Ftoken%3D921adfeb82738a8511abbfe7689b413c&refer=http%3A%2F%2Fwww.baidu.com&app=2021&size=f360,240&n=0&g=0n&q=75&fmt=auto?sec=1694538000&t=9be706d634eeea468f0087e53d922994',
        'title': '吃了吗',
        'rating': '1.2',
        'comment_count': 100,
        'authors': 'heihei'
    }
]
tvs = [
    {
        'id': '234',
        'thumbling': 'https://gimg3.baidu.com/search/src=http%3A%2F%2Fpics7.baidu.com%2Ffeed%2Feaf81a4c510fd9f9e5e0f80e9a7e11262934a446.jpeg%40f_auto%3Ftoken%3D025a36e78152a33cb976d044249ffa41&refer=http%3A%2F%2Fwww.baidu.com&app=2021&size=f360,240&n=0&g=0n&q=75&fmt=auto?sec=1694538000&t=90f86f28c77c896d5367c3495173ef0b',
        'title': '李光洁',
        'rating': '90',
        'comment_count': 100,
        'authors': 'haha'
    }
]

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

@app.route('/douban')
def douban():
    context = {
        'movies': movies,
        'tvs': tvs
    }
    return render_template('douban.html', **context)

@app.route('/douban_list')
def douban_list():
    category = int(request.args.get('category'))
    items = None
    if category == 1:
        items = movies
    else:
        items = tvs
    return render_template('list.html', items = items)

if __name__ == '__main__':
    app.run()
