from flask import Flask
from flask_login import LoginManager
from database import Database
from problem import Problem
from user import get_user
import views

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/problemset", view_func=views.problemset_page)
    app.add_url_rule("/rating", view_func=views.rating_page)
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=views.register_page)

    lm.init_app(app)
    lm.login_view = "login"

    db = Database()
    db.add_problem(Problem("Hello World Challenge!", "https://www.hackerrank.com/challenges/30-hello-world/problem", 1, ["dfs-and-similar","graph-theory", "greedy-algorithms", "math", "number-theory"],123,2,3))
    db.add_problem(Problem("Hello World Challenge2!", "https://www.hackerrank.com/challenges/30-hello-world/problem", 2, ["dfs-and-similar","graph-theory", "greedy-algorithms", "math", "number-theory"],123,3,3))
    app.config["db"] = db
    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)