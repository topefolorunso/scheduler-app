from .. import db
from ..models import Tasks
from flask import render_template, request, redirect, Blueprint


task = Blueprint('task', __name__)

@task.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Tasks.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/home')
    except:
        return "Issue deleting the task"


@task.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):

    task = Tasks.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/home')
        except:
            return 'Issue updating task!'

    else:
        return render_template('update.html', task=task)
