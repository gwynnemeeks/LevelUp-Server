"""Module for generating events by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection

def userevent_list(request):
    """Function to build an HTML report of events"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all events, with related user info
            db_cursor.execute("""
                SELECT
                    e.id event_id
                    e.day
                    e.time
                    e.location
                    e.game_id 
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
            """)