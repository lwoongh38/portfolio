from flask import Blueprint, render_template, jsonify
from twitter_app.models import get_data, parse_records

main_routes = Blueprint('main_routes', __name__)

# '/'
@main_routes.route('/')
def index():
    data = get_data()
    return render_template("index.html", data=data)

# /add.json
@main_routes.route('/add.json')
def json_data():
    raw_data = get_data()
    parsed_data = parse_records(raw_data)
    
    return jsonify(parsed_data)
