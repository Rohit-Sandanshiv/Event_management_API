from flask import jsonify, request, Blueprint
import json
from services.event_service import insert_events

create_event = Blueprint('event', __name__)


@create_event.route('/', methods=['POST'])
def create():
    request_body = json.loads(request.data)
    data = request_body.get("payload")

    status = insert_events(data)

    if status:
        return jsonify({"message": "Event Created", "event": status}), 201
    else:
        return jsonify({"message": "Insert Failed", "status": "error"}), 500