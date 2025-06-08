from flask import jsonify, request, Blueprint
from services.event_service import get_attendees

get_attendee = Blueprint('get_attendee', __name__)


@get_attendee.route('/<event_id>/attendee', methods=['GET'])
def create(event_id):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    status = get_attendees(event_id, page, limit)
    print(status)
    if status:
        return jsonify({"message": "Attendees :", "sections": status}), 200
    else:
        return jsonify({"message": "Something went wrong! Please come back later"}), 404