from flask import Flask,render_template
from forms import RegisterForm, LoginForm
app = Flask(__name__)
app.config["SECRET_KEY"] = "slahGHGTY6IY75"

about_people = [
    {
        "name" : "Ali",
        "title" : "How the Web Became Unreadable",
        "decription" : "This is much more straightforward, and relies on an interesting topic. You may read this headline and think.",
        "date" : "11/09/19",
        "class" : "list-group-item-success"
    },
    {
        "name" : "John",
        "title" : "What % Wednesday Adams Are You",
        "decription" : "Buzzfeed strikes again with a completely nonsensical, highly trending question article.",
        "date" : "07/03/20",
        "class" : "list-group-item-info"
    },
    {
        "name" : "Andrew",
        "title" : "Patagonia’s New Study Finds Fleece Jackets Are a Serious Pollutant",
        "decription" : "In the above case, it’s not a study conducted by Outside Magazine itself, but by an outdoor brand, Patagonia.",
        "date" : "11/11/19",
        "class" : "list-group-item-warning"
    },
    {
        "name" : "Phillip",
        "title" : "The Best Productivity Habits of Famous Writers",
        "decription" : "While not a strict study, this article collects quotes and concepts from famous writers to create interesting content that is informative to a specific profession.",
        "date" : "11/01/19",
        "class" : "list-group-item-secondary"
    },
    {
        "name" : "Phillip",
        "title" : "The Best Productivity Habits of Famous Writers",
        "decription" : "While not a strict study, this article collects quotes and concepts from famous writers to create interesting content that is informative to a specific profession.",
        "date" : "11/01/19",
        "class" : "list-group-item-danger"
    },

]
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html", infos= about_people)

@app.route("/login")
def login():
    login_form = LoginForm()
    return render_template("account/login.html", login = login_form)

@app.route("/register")
def register():
    form = RegisterForm()
    return render_template("account/register.html" , form = form)

if __name__ == "__main__":
    app.run(debug=True)