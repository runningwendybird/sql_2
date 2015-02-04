from flask import Flask, render_template, request
import hackbright

app = Flask(__name__)

@app.route("/")
def get_student():
    hackbright.connect_to_db()
    student_github = request.args.get("student")
    return hackbright.get_student_by_github(student_github)

if __name__ == "__main__":
    app.run(debug=True)