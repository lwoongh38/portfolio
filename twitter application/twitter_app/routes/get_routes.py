from flask import Blueprint, render_template, request
from twitter_app.models import db, User, Tweet, get_data

get_routes = Blueprint('get_routes', __name__)

# '/get/' -> 맨 마지막  '/'를 추가
@get_routes.route('/', methods=["GET", "POST"])
def get():
    tweet_data=None

    if request.method == "POST":
        print(dict(request.form))

        tw_user = request.form
        input_name = tw_user['tweets']
        
        user_info = User.query.filter_by(username=input_name).one()
        user_id = user_info.__dict__['id']

        tweet_data = Tweet.query.filter_by(user_id=user_id)
        # breakpoint()
    return render_template('get.html', data=tweet_data)