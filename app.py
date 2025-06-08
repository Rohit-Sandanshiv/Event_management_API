from flask import Flask
from blueprints.create_event_bp import create_event
from blueprints.get_event_bp import get_event
from blueprints.register_attendee_bp import register_attendee
from blueprints.get_attendee_bp import get_attendee

app = Flask(__name__)

app.register_blueprint(create_event, url_prefix='/events')
app.register_blueprint(get_event, url_prefix='/events')
app.register_blueprint(register_attendee, url_prefix='/events')
app.register_blueprint(get_attendee, url_prefix='/events')

if __name__ == '__main__':
    app.run(debug=True)
