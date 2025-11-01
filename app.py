# imports
import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SSQLALCHEMY_TRACK_MODFICATION"] = False
db = SQLAlchemy(app)


class MyTask(db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id1}"


with app.app_context():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Print to terminal for debugging
            return f"Error: {str(e)}"  # Show actual error message
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.filter_by(id1=id).first_or_404()
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect(url_for("index"))
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    task = MyTask.query.filter_by(id1=id).first_or_404()

    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"

    return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
