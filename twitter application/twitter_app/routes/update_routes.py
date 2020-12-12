from flask import Blueprint, render_template, request
from twitter_app.models import db, User, Tweet, get_data

update_routes = Blueprint('update_routes', __name__)

@update_routes.route('/', methods=["GET", "POST"])
def update():
    if request.method == "POST":
        print(dict(request.form))

        update_user = request.form
        before_name = update_user['input_before']
        after_name = update_user['input_after']
        print(before_name, after_name)

        User.query.filter_by(full_name=before_name).update({'full_name':after_name})

        db.session.commit()

    data = get_data()
    return render_template('update.html', data=data)