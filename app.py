from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SDLALCHEMY_TRACK_MODIFICATIONS"] =False

db= SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(200),nullable=False)
    done= db.Column(db.Boolean,default=False)

@app.route("/" , methods=["GET" , "POST"])
def home():
    if request.method == "POST":
        todo_text= request.form.get("todo")
        if todo_text:
             new_todo= Todo(text=todo_text)
             db.session.add(new_todo)
             db.session.commit()

    todos= Todo.query.all()
    return render_template("index.html", todos=todos)




@app.route("/delete/<int:todo_id>")
def delete(todo_id):
        todo= Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    

if __name__ == "__main__":
    with app.app_context():
         db.create_all()

    app.run(debug=True)