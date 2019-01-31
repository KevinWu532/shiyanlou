from flask import Blueprint, render_template
from simpledu.models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def index(username):
    userdata = User.query.filter_by(username = username).first()
    print(userdata)
    return render_template('user/detail.html', userdata = userdata)
