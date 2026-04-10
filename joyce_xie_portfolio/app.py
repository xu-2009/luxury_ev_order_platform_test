from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_title="Home")


@app.route("/about")
def about():
    return render_template("about.html", page_title="About Joyce")


@app.route("/education")
def education():
    return render_template("education.html", page_title="Education")


@app.route("/activities")
def activities():
    return render_template("activities.html", page_title="Activities")


@app.route("/awards")
def awards():
    return render_template("awards.html", page_title="Awards and Honors")


@app.route("/skills")
def skills():
    return render_template("skills.html", page_title="Skills")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    success = False
    form_data = {"name": "", "email": "", "message": ""}

    if request.method == "POST":
        form_data["name"] = request.form.get("name", "").strip()
        form_data["email"] = request.form.get("email", "").strip()
        form_data["message"] = request.form.get("message", "").strip()
        success = True

    return render_template("contact.html", page_title="Contact", success=success, form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)