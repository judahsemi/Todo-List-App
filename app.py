
import os

from flask import Flask
from flask import request, session, url_for
from flask import jsonify, make_response, redirect, abort
from flask import render_template, flash

import config as cfg
from models import db, Task, Category



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(cfg.config[config_name])
    cfg.config[config_name].init_app(app)

    db.init_app(app)
    return app

def clean_text(text):
    return text.strip() if isinstance(text, str) else text


app = create_app(os.environ.get("CONFIG_NAME") or "default")


@app.route("/")
def home():
    task_list = Task.query.all()
    return render_template("home.html", task_list=task_list)


@app.route("/add", methods=["GET", "POST"])
def add():
    kwargs = {}
    kwargs = {"categories": Category.query.all()}
    if request.method == "POST":
        cat_name = clean_text(request.form.get("category"))
        cat = Category.query.filter_by(name=cat_name).first()

        # Create new category if "Create New Category" is selected
        if cat_name == "--new-category--":
            cat_name = clean_text(request.form.get("new_category_name"))
            if not cat_name:
                flash("Field, 'Category Name', cannot be empty.")
                return redirect("add")

            cat = Category.query.filter_by(name=cat_name).first()
            if cat:
                flash("Category with name, '{}', already exists.".format(cat_name))
                return redirect("add")

            new_category = Category(name=cat_name)
            db.session.add(new_category)
            db.session.commit()

            cat = new_category

        # Get selected category
        if not cat:
            flash("Category with name, '{}', does not exists.".format(cat_name))
            return redirect("add")

        # Create task
        title = request.form.get("title")
        if not title:
            flash("Field, 'Title', cannot be empty.")
            return redirect("add")

        new_task = Task(title=title, complete=False, cat_id=cat.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task Added.")
        return redirect(url_for("home"))
    return render_template("task.html", **kwargs)


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Task.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5005)
