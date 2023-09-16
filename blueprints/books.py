from flask import Blueprint

books_bp = Blueprint('users', __name__)

@books_bp.route('/profile/')
def profile():
  return 'books profile'


@books_bp.route('/setting/')
def setting():
  return 'books settings'