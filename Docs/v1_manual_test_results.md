# Example workflow - Volunteer Registering for an Event
Roxanne is a high school student and she is in desperate need of more volunteering hours to graduate high school.
- starts by calling `GET /events/` to see the list of posted volunteer events she can register for. She sees one she likes with an event_id of 2, and will use that event_id to sign up for it later.
- then creates a new volunteer object by calling `POST /volunteers/` and receives the volunteer ID 1.
- Roxanne then calls `PUT /volunteers/events/2` to register for the event she saw earlier. This will return a success if she is able to add this to her schedule.
- Roxanne repeats the previous step to register for as many events as she wants.
- She confirms that she is going to add the current event to her schedule and finalizes the registering process by calling `POST /schedule/1/register`, which returns the total events and their total hours that she has decided to sign up for.
  
Roxanne has successfully registered for volunteer opportunities. 

# Testing results
1. Calling `GET /events/`

```html
curl -X 'GET' \
  'https://volunteer-verse.onrender.com/events/' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac'
```

2. Response

```json
[
  {
    "event_id": 1,
    "name": "Soup kitchen",
    "spots_left": 30,
    "minimum_age": 15,
    "activity_level": 1,
    "location": "Long Beach",
    "start_time": "2023-11-10T19:00:00+00:00",
    "end_time": "2023-11-10T22:00:00+00:00",
    "description": "Hand out meals to the hungry."
  },
  {
    "event_id": 2,
    "name": "Beach cleanup",
    "spots_left": 15,
    "minimum_age": 10,
    "activity_level": 2,
    "location": "Los Angeles",
    "start_time": "2023-11-13T12:00:00+00:00",
    "end_time": "2020-11-13T15:00:00+00:00",
    "description": "Come and collect trash from the beach!"
  }
]
```

3. Calling `POST /volunteers/`

```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/volunteers/' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -H 'Content-Type: application/json' \
  -d '{
  "volunteer_name": "Roxanne",
  "city": "Anaheim",
  "age": "17",
  "email": "roxanne@anaheimhigh.edu"
}'
```

4. Response

```json
{
  "volunteer_id": 1
}
```

5. Calling `PUT /volunteers/events/2`

```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/volunteers/events/2?volunteer_id=1' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -d ''
```

6. Response

```json
"OK"
```

7. Calling `POST /volunteers/1/register`
```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/volunteers/1/register' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -d ''
```

8. Response

```json
{
  "total_events_registered": 1,
  "total_hours": 3
}
```
