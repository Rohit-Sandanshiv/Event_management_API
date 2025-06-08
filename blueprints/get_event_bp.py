from flask import jsonify, Blueprint
from services.event_service import get_events


get_event = Blueprint('get_event', __name__)


@get_event.route('/', methods=['GET'])
def create():
    status = get_events()
    print(status)
    if status:
        return jsonify({"message": "Events :", "sections": status}), 200
    else:
        return jsonify({"message": "Something went wrong! Please come back later"}), 404