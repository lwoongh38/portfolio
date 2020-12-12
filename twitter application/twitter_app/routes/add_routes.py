from flask import Blueprint, render_template, request
from twitter_app.models import db, User, Tweet, get_data, parse_records
from twitter_app.twitter_api import api
from embedding_as_service_client import EmbeddingClient

en = EmbeddingClient(host='54.180.124.154', port=8989)

add_routes = Blueprint('add_routes', __name__)

# '/add/' -> 맨 마지막  '/'를 추가
@add_routes.route('/', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        print(dict(request.form))
        result = request.form
        # breakpoint()
        user = api.get_user(screen_name=result['user_name'])
        
        # 데이터베이스에 추가
        new_user = User(id=user.id, username=user.screen_name, full_name=user.name, followers=user.followers_count, location=user.location)
        db.session.add(new_user)
        # 저장
        db.session.commit()

        raw_tweets = api.user_timeline(screen_name=result['user_name'], count=25,
                                        include_rts=False, exclude_replies=True,
                                        tweet_mode="extended")

        tweet_texts = [_.full_text for _ in raw_tweets]

        embeddings = en.encode(texts=tweet_texts)

        for index, tweet in enumerate(raw_tweets):
            print(tweet.id, tweet.full_text, user.id, end='/n/n/n')
            new_tweets = Tweet(id=tweet.id, text=tweet.full_text, embedding=embeddings[index], user_id=tweet.user.id)
            db.session.add(new_tweets)
        
        db.session.commit()

    data = get_data()
    return render_template('add.html', data=data)

 