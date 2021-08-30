from flask import Flask, request, session, redirect, url_for
from flask import render_template

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def add_todo(form):
    if not "todos" in session:
        session["todos"] = []

    id = len(session["todos"])
    title = form["title"]

    session["todos"].append({
        "title": title, "id": id, "status": False
    })

    session.modified = True

    return f'title: {title}, id: {id}'


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':

        return add_todo(request.form)

    if "todos" in session:
        return render_template("index.html", todos=session["todos"])

    return render_template("index.html")


@app.route("/clean_todos")
def clean_todos():
    if "todos" in session:
        session.pop('todos', None)

    return redirect(url_for('home'))


@app.route("/edit_todo/", methods=["POST"])
@app.route("/edit_todo/<int:id>", methods=["GET"])
def edit_todo(id=None):
    if request.method == 'POST':
        id = int(request.form["id"])
        title = request.form["title"]
        status = request.form["status"]

        todos_filtered = [todo for todo in session["todos"] if todo['id'] != id]
        session["todos"] = todos_filtered

        session["todos"].append({
            "id": id,
            "title": title,
            "status": status,
        })

        return redirect(url_for('home'))

    if "todos" in session:
        todos_filtered = [todo for todo in session["todos"] if todo['id'] == id]

        if len(todos_filtered) == 0:
            return f"Atividade de id = {id} não foi encontrada"

        todo = todos_filtered[0]

        return render_template("edit.html", todo=todo)

    return "Não existe nenhuma atividade cadastrada"
