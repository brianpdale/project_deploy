from flask import render_template, request, redirect, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show



@app.route("/dashboard")
def dashboard():
    shows = Show.get_all_shows()

    if "uuid" not in session:
        return redirect("/")

    
    return render_template("dashboard.html", all_shows = shows, user = User.get_by_id({"id": session['uuid']}))

@app.route("/new/show")
def new_show():
    if 'uuid' not in session:
        return redirect("/")

    return render_template("new_show.html", user = User.get_by_id({"id": session['uuid']}))

@app.route("/show/create", methods = ['POST'])
def show_create():
    if 'uuid' not in session:
        return redirect("/")
    if not Show.show_validator(request.form):
            return redirect("/new/show")

    data = {
        "user_id": session['uuid'],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description']
    }
    Show.create(data)

    return redirect("/dashboard")

@app.route("/show/<int:id>")
def  show_view(id):
    if 'uuid' not in session:
        return redirect("/")

    return render_template("view_show.html", show = Show.get_one({"id": id}))



@app.route("/show/<int:id>/delete")
def delete_show(id):
    Show.delete({"id": id})

    return redirect("/dashboard")


@app.route("/show/<int:id>/edit")
def update(id):
    if 'uuid' not in session:
        return redirect("/")
    
    return render_template(
        "edit_show.html",
        show = Show.get_one({"id": id}),
        user = User.get_by_id({"id": session['uuid']})
    )

@app.route("/show/<int:id>/update",  methods = ["POST"])
def update_show(id):
    if 'uuid' not in session:
        return redirect("/")
    if not Show.show_validator(request.form):
        return redirect(f"/show/{id}/edit")

    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'id': id
    }
    Show.update_show(data)

    return redirect("/dashboard")







