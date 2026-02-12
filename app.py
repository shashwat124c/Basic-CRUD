from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

# @app.route("/")
# def welcome():
#   return "Welcom Nigger"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MyTask(db.Model): #Create a TABLE called MyTask in the database.
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100), nullable = False)
  complete = db.Column(db.Integer, default=0)
  created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self)->str:
    return f"Task {self.id}"

@app.route("/", methods=["POST", "GET"])
def index():
  #Adding a task
  if request.method=="POST":
    current_task = request.form['content']
    new_task = MyTask(content=current_task) #Here content is the column content in the db
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect("/")
    except Exception as e:
      print(f"ERROR: {e}")
      return f"ERROR: {e}"

  else:
    active_tasks = MyTask.query.filter_by(complete=0).order_by(MyTask.created).all()
    completed_tasks = MyTask.query.filter_by(complete=1).order_by(MyTask.created).all()
    return render_template('index.html', active_tasks=active_tasks, completed_tasks=completed_tasks)

#Deleting a task
@app.route("/delete/<int:id>")
def delete(id:int):
  delete_task = MyTask.query.get_or_404(id)
  try:
    delete_task.complete = 1
    db.session.commit()
    return redirect('/')
  except Exception as e:
    return f"Error: {e}"

#Editing a task
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):
  edit_task = MyTask.query.get_or_404(id)
  if request.method == "POST":
    edit_task.content = request.form['content']
    try:
      db.session.commit()
      return redirect("/")
    except Exception as e:
      return f"ERROR: {e}"
  else:
    return render_template('edit.html', task=edit_task)
  
@app.route("/completed_delete")
def completed_delete():
  try:
    MyTask.query.filter_by(complete=1).delete()
    db.session.commit()
  except Exception as e:
    return f"ERROR: {e}"
  return redirect('/')


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True) 