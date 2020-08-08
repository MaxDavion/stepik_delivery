from functools import wraps
# from flask import abort, flash, session, redirect, request, render_template
# from app import app, db










@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html'), 404
