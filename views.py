from flask import render_template

def home_page():
    return render_template("home.html")

def problemset_page():
    return render_template("problemset.html")

def rating_page():
    return render_template("rating.html")

def profile_page():
    return render_template("profile.html")