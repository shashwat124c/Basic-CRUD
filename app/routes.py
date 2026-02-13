from flask import Blueprint, render_template, request, redirect
from .models import MyTask
from . import db

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
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
    return render_template('index.html', 
                           active_tasks=active_tasks, 
                           completed_tasks=completed_tasks)

@main.route("/delete/<int:id>")
def delete(id:int):
  delete_task = MyTask.query.get_or_404(id)
  try:
    delete_task.complete = 1
    db.session.commit()
    return redirect('/')
  except Exception as e:
    return f"Error: {e}"
  
@main.route("/edit/<int:id>", methods=["POST", "GET"])
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
    return render_template('edit.html', 
                           task=edit_task)
  
@main.route("/completed_delete")
def completed_delete():
  try:
    MyTask.query.filter_by(complete=1).delete()
    db.session.commit()
  except Exception as e:
    return f"ERROR: {e}"
  return redirect('/')