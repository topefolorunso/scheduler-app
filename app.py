from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # created_at = db.Column(db.Integer, default=db.text('now()'))

    def __repr__(self) -> str:
        return '<Task %r>' %self.id



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Issue adding your task!'

    else:
        tasks = ToDo.query.order_by(ToDo.created_at).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Issue deleting the task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):

    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating task!'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)