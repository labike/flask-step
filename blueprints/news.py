from flask import Blueprint

news_bp = Blueprint('news', __name__, url_prefix='/news')

@news_bp.route('/list/')
def list():
  return 'news list'


@news_bp.route('/detail/')
def detail():
  return 'news detail'