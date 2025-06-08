from flask import jsonify, request, Blueprint
import json
from services.event_service import insert_attendees


register_attendee = Blueprint('attendee', __name__)


@register_attendee.route('/<string:event_id>/register', methods=['POST'])
def create(event_id):
    request_body = json.loads(request.data)
    data = request_body.get('payload')
    status = insert_attendees(data, event_id)
    print(status)
    if status:
        return jsonify({"message": status, "status": "success"}), 201
    else:
        return jsonify({"message": "Something went wrong! Please come back later"}), 500
