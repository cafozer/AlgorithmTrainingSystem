from flask import Flask
import views

def create_app():
    app = Flask(__name__)

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/problemset", view_func=views.problemset_page)
    app.add_url_rule("/rating", view_func=views.rating_page)
    app.add_url_rule("/profile", view_func=views.profile_page)
    app.add_url_rule("/login", view_func=views.login_page)
    app.add_url_rule("/register", view_func=views.register_page)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)