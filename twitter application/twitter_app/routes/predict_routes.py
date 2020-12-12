from flask import Blueprint, render_template, request
from twitter_app.models import db, User, Tweet, get_data
from embedding_as_service_client import EmbeddingClient
from sklearn.linear_model import LogisticRegression
from twitter_app.twitter_api import api

predict_routes = Blueprint('predict_routes', __name__)

# host 주소 설정
en = EmbeddingClient(host='54.180.124.154', port=8989)
print('Connected with server')
print('-' * 40)

@predict_routes.route('/', methods=['GET', 'POST'])
def predict():
    statement = ''
    if request.method == 'POST':
        print(dict(request.form))
        X=[]
        y=[]

        prediction = request.form
        user_1 = prediction['user_1']
        user_2 = prediction['user_2']
        tweet_predict = prediction['input_tweet']

        user_1_tweet = User.query.filter_by(username=user_1).one().tweets
        user_1_id = User.query.filter_by(username=user_1).one().id
        
        for tweet in user_1_tweet:
            X.append(tweet.embedding)
            y.append(user_1_id)

        user_2_tweet = User.query.filter_by(username=user_2).one().tweets
        user_2_id = User.query.filter_by(username=user_2).one().id
        for tweet in user_2_tweet:
            X.append(tweet.embedding)
            y.append(user_2_id)

        classifier = LogisticRegression()
        classifier.fit(X, y)

        em_pred_val = en.encode(texts=[tweet_predict])
        pred_result = classifier.predict(em_pred_val)

        user_info = User.query.filter_by(id=int(pred_result)).one()
        user_name = user_info.__dict__['username']

        statement = f" {user_1}유저와 {user_2}유저 중 {tweet_predict} 트윗을 작성했을 것으로 예상되는 유저는 {user_name} 입니다."

    data = User.query.all()
    return render_template('predict.html', data = data, statement=statement)






















        # user_1_id = api.get_user(screen_name=prediction['user_1'])
        # tweet_1 = api.user_timeline(screen_name=prediction['user_1'], count=25,
        #                                 include_rts=False, exclude_replies=True,
        #                                 tweet_mode="extended")
        # tweet_2 = api.user_timeline(screen_name=prediction['user_2'], count=25,
        #                                 include_rts=False, exclude_replies=True,
        #                                 tweet_mode="extended")

        # for tweet in tweet_1:
        #     X.append(tweet.embedding)
        #     y.append(tweet.embedding)

        # em_X_1 = en.encode(texts=[tweet_1.text])
        # em_X_2 = en.encode(texts=[tweet_2.text])
        # append_to_with_label(X, vecs, y, user_1)
        # append_to_with_label(X, vecs2, y, user_2)
        

