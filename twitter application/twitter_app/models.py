from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle as pickle

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String)
    full_name = db.Column(db.String)
    followers = db.Column(db.Integer)
    location = db.Column(db.String)

    def __repr__(self):
        return "<User {} {} >".format(self.id, self.username)

class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    embedding = db.Column(db.PickleType)

    def __repr__(self):
        return "< Tweet {} >".format(self.id) 
       
def parse_records(db_records):
    # breakpoint()
    parsed_list = []
    for record in db_records:
        parsed_record = record.__dict__
        print(parsed_record)
        del parsed_record["_sa_instance_state"]
        parsed_list.append(parsed_record)

    # breakpoint()
    return parsed_list


def get_data():
    return User.query.all()
