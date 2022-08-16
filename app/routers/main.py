from .. import db
from ..models import Tasks
from flask import render_template, request, redirect, Blueprint
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home', methods=['POST', 'GET'])
# @login_required
def home():

    if not current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        task_content = request.form['content']
        owner_id = current_user.id
        new_task = Tasks(content=task_content, owner_id=owner_id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home')
        except Exception as e:
            return f'Issue adding your task!'

    else:
        owner_id = current_user.id
        nick = current_user.nick
        tasks = Tasks.query.filter_by(owner_id=owner_id).order_by(Tasks.created_at).all()
        return render_template('home.html', tasks=tasks, nick=nick)