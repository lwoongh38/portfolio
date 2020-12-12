from flask import Blueprint, render_template, request
from twitter_app.models import db, User, Tweet, get_data

delete_routes = Blueprint('delete_routes', __name__)

@delete_routes.route('/', methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        try:
            tw_user = request.form
            input_name = tw_user['delete_info']
            # breakpoint()
            user_info = User.query.filter_by(username=input_name).one()
            user_id = user_info.__dict__['id']
            User.query.filter_by(username=input_name).delete()
            Tweet.query.filter_by(user_id=user_id).delete()
            # breakpoint()
            db.session.commit()
            msg = "delete 기능이 작동합니다."
            print(msg)

        except Exception as e:
            db.session.rollback()
            print("실패했습니다")
            print(e)
            msg = "Please enter the valid username"
    data = get_data()
    return render_template('delete.html', data=data)