from ast import Pass
from crypt import methods
from nis import cat
from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Neo:passneo@127.0.0.1/MATRIX'
db = SQLAlchemy(application)



class Todo(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) :
        return '<Task %r>' % self.id
    


with application.app_context():
    db.create_all()
print("Database tables created successfully")

@application.route('/', methods=['POST','GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@application.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting that task'
    
@application.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    application.run(debug=True)