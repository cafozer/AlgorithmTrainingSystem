from flask import Flask
from flask_login import LoginManager, login_required
from database import Database
from problem import Problem
from user import get_user
import views
import forms
import psycopg2
import forms
import os

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    print(user_id)
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/problemset/<string:sort>", view_func=views.problemset_page, methods=["GET", "POST"])
    app.add_url_rule("/rating", view_func=views.rating_page)
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/problem_add", view_func=views.problem_add_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/addnewtopic", view_func=views.new_topic_page, methods=["GET", "POST"])
    app.add_url_rule("/like/<string:probid>/<string:nextsort>", view_func=views.like_page)
    app.add_url_rule("/dislike/<string:probid>/<string:nextsort>", view_func=views.dislike_page)
    app.add_url_rule("/solved/<string:probid>/<string:nextsort>", view_func=views.solved_page)
    app.add_url_rule("/cantsolved/<string:probid>/<string:nextsort>", view_func=views.cant_solved_page)
    #app.add_url_rule("/problemset/sort_by_difficulty_ascending", view_func=views.problemset_sort_diff_asc)
    #app.add_url_rule("/problemset/sort_by_difficulty_descending", view_func=views.problemset_sort_diff_des)
    #app.add_url_rule("/problemset/sort_by_like", view_func=views.problemset_sort_like)
    
    #print(os.getenv('DATABASE_URL'))
    lm.init_app(app)
    lm.login_view = "login_page"

    db = Database()
    db.add_problem(Problem("Hello World Challenge!", "https://www.hackerrank.com/challenges/30-hello-world/problem", 1,123,2,3))
    db.add_problem(Problem("Hello World Challenge2!", "https://www.hackerrank.com/challenges/30-hello-world/problem", 2,123,3,3))
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)