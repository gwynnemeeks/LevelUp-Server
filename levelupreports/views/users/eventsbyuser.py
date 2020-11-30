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
                    e.id,
                    e.day,
                    e.time,
                    e.location,
                    e.game_id,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_gamer gr on e.gamer_id = gr.id
                JOIN
                    auth_user u on gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "organizer_id": 1,
            #         "full_name": "Molly Ringwald",
            #         "events": [
            #             {
            #                 "id": 5,
            #                 "day": "2020-12-23",
            #                 "time": "19:00",
            #                 "location": "Chez Meeks"
            #                 "game_name": "Fortress America"
            #             }
            #         ]
            #     }
            # }

            events_by_user = {}

            for row in dataset:
                # Create an Event instance and set its properties
                event = Event()
                event.day = row['day']
                event.time = row['time']
                event.location = row['location']
                event.game_id = row['game_id'] # this row might give you problems

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary ...
                if uid in events_by_user:

                    #Add the current event to the `events` list for it
                    events_by_user[uid]['events'].append(event)

                else:
                    # otherwise, create the key and dictionary value
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row ["full_name"]
                    events_by_user[uid]["events"] = [event]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_events = events_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)