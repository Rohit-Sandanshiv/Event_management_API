from flask import jsonify
import uuid
from models.db_connection import get_db_connection
from datetime import datetime
from utils.timezone import ist_to_utc, utc_to_ist


def insert_events(data):
    unique_id = str(uuid.uuid4())[:7]
    name = data.get("name")
    location = data.get("location")
    start_time = ist_to_utc(data.get("start_time"))
    end_time = ist_to_utc(data.get("end_time"))
    max_capacity = data.get("max_capacity")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """INSERT INTO events(id, name, location, start_time, end_time, max_capacity) 
            VALUES (?, ?, ?, ?, ?, ?)"""
            params = (unique_id, name, location, start_time, end_time, max_capacity)
            cursor.execute(query, params)
            conn.commit()
        return unique_id
    except Exception as e:
        print(f"Error inserting data: {e}")
        return 0


def get_events():
    now = datetime.now()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = f"""SELECT * FROM events where start_time > ? ORDER BY start_time"""
            events = cursor.execute(query, (now,)).fetchall()
            conn.commit()
        if len(events) == 0:
            return ['NO upcoming events found! Please try again']
        else:
            return [{"id": i[0],
                     "name": i[1],
                     "location": i[2],
                     "start_time": utc_to_ist(datetime.fromisoformat(i[3])).strftime("%Y-%m-%d %H:%M"),
                     "end_time": utc_to_ist(datetime.fromisoformat(i[4])).strftime("%Y-%m-%d %H:%M"),
                     "max_capacity": i[5]
                     } for i in events]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return 0


def insert_attendees(data, event_id):
    unique_id = str(uuid.uuid4())[:7]
    name = data.get("name")
    email = data.get("email")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            email_backend_query = """SELECT id from attendees where email = ? and event_id = ?"""
            results = cursor.execute(email_backend_query, (email, event_id)).fetchall()
            if not results:
                max_capacity_event_query = """select max_capacity from events where id = ?"""
                max_capacity = cursor.execute(max_capacity_event_query, (event_id,)).fetchall()[0][0]

                is_space_avl_query = """select count(*) from attendees where event_id = ?"""
                is_space_avl_count = cursor.execute(is_space_avl_query, (event_id,)).fetchall()[0][0]

                print(is_space_avl_count)
                print(max_capacity)

                if is_space_avl_count < max_capacity:
                    query = """INSERT INTO attendees(id, name, email, event_id) 
                        VALUES (?, ?, ?, ?)"""
                    params = (unique_id, name, email, event_id)
                    cursor.execute(query, params)
                    conn.commit()
                    return "Registration Successful"
                else:
                    return "Seats full! Come again for next show"
            else:
                return "only 1 registration per user"
    except Exception as e:
        print(e.__traceback__.tb_lineno)
        print(f"Error inserting data: {e}")
        return 0


def get_attendees(event_id, page=1, limit=10):
    offset = (page - 1) * limit
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = f"""SELECT * from attendees where event_id = ? LIMIT ? OFFSET ?"""
            events = cursor.execute(query, (event_id, limit, offset)).fetchall()
            conn.commit()
        if len(events) == 0:
            return ['No attendees for a event yet...']
        else:
            return [{"id": i[0], "name": i[1], "email": i[2], "event_id": i[3]} for i in events]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return 0
