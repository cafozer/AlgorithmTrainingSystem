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

app = Flask(__name__, static_url_path='/static')
app.config.from_object("settings")
app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/problemset/<string:sort>", view_func=views.problemset_page, methods=["GET", "POST"])
app.add_url_rule("/rating", view_func=views.rating_page)
app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=views.register_page, methods=["GET", "POST"])
app.add_url_rule("/problem_add", view_func=views.problem_add_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=views.logout_page)
app.add_url_rule("/addnewtopic", view_func=views.new_topic_page, methods=["GET", "POST"])
app.add_url_rule("/like/<string:probid>/<string:nextsort>", view_func=views.like_page)
app.add_url_rule("/dislike/<string:probid>/<string:nextsort>", view_func=views.dislike_page)
app.add_url_rule("/solved/<string:probid>/<string:nextsort>", view_func=views.solved_page)
app.add_url_rule("/cantsolved/<string:probid>/<string:nextsort>", view_func=views.cant_solved_page)
app.add_url_rule("/profile/<string:userid>", view_func=views.profile_page)
app.add_url_rule("/profile/<string:userid>/problems", view_func=views.problems_of_a_user)
app.add_url_rule("/update_problem/<string:probid>", view_func=views.update_problem_page, methods=["GET", "POST"])
app.add_url_rule("/delete/<string:probid>", view_func=views.delete_problem_page)
app.add_url_rule("/analyze_me", view_func=views.analyze_me_page)
    
    #print(os.getenv('DATABASE_URL'))
lm.init_app(app)
lm.login_view = "login_page"

db = Database()
app.config["db"] = db




if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)