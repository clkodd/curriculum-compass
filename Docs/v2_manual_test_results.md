# Example workflow - Volunteer Site Event Coordinator Event Posting

Ronnie comes to our volunteer website because she is in desperate need of volunteers for serving meals at the Midnight Mission. She intends to create an event for volunteers to sign up. Ronnie wants to input her event details/requirements for the volunteer event. Ronnie is an established supervisor.

- starts by calling `POST /planner/1/create` with her supervisor ID, 1, and passes in:
  - Name: "Midnight Mission Mania"
  - Spots: 50
  - Minimum age: 15
  - Activity level: 1
  - Location: "Los Angeles"
  - Start time: "2023-11-04T20:00:00Z"
  - End time: "2023-11-04T23:59:59Z"
  - Description: “Serve food to the homeless at the Midnight Mission to help those in need.”
  She receives an event ID of 1 from this endpoint.
- the database updates to say that there is a new event on November 4th with all her inputted information on it.

Ronnie gets her volunteers and the homeless are served meals.

# Testing results
1. Calling `/event-planner/1/schedule`

```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/planner/1/create' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Midnight Mission Mania",
  "total_spots": 50,
  "minimum_age": 15,
  "activity_level": 1,
  "location": "Los Angeles",
  "start_time": "2023-11-04T20:00:00Z",
  "end_time": "2023-11-04T23:59:59Z",
  "description": "Serve food to the homeless at the Midnight Mission to help those in need."
}'
```

2. Response

```json
{
  "event_id": 1
}
```

# Example workflow - Supervisor Deleting an Event

Ronnie had previously created an event for people to serve meals at Midnight Mission. She posted her volunteer opportunity to take place on November 4th, and it went great! It is now November 6th. She plans to delete the volunteer request from the website. 

- from her unique event she created, using its event_id (1), she calls `POST /planner/1/`.

Ronnie has successfully deleted her volunteer Post.

# Testing results
1. Calling `/planner/1/`

```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/planner/1' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -d ''
```

2. Response

```json
"OK"
```

# Example workflow - Admin Resetting the Site

Binglethorpe is a site admin for Volunteer Verse. Due to a recent cybersecurity attack on the event planners' accounts that changed all the event locations to "Add me on Genshin Impact," it has become necessary to delete all the active events on the site. He intends to wipe the site by removing all the events and deleting the volunteers' schedules.

- starts by calling `GET /admin/organizations` to see all the different organization with active events, so he can notify them later.
- then Binglethorpe calls `POST /admin/reset`. All the schedules are reset, and every active event is deleted from the list.
- Finally, he calls `GET /admin/organizations` to ensure the reset worked as intended. No organizations show up, so Binglethorpe is confident in his reset.

The events and schedules are cleared. Binglethorpe is moritifed and enrolls in CSC 321 to prevent future attacks.

# Testing results
1. Calling `GET /admin/organizations`

```html
curl -X 'GET' \
  'https://volunteer-verse.onrender.com/admin/organization_info/' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac'
```

2. Response

```json
[
  {
    "organization": "Midnight Mission"
  },
  {
    "organization": "Generic Helper Nonprofit"
  }
]
```

3. Calling `POST /admin/reset`

```html
curl -X 'POST' \
  'https://volunteer-verse.onrender.com/admin/reset' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac' \
  -d ''
```

4. Response

```json
"OK"
```

5. Calling `GET /admin/organizations`

```html
curl -X 'GET' \
  'https://volunteer-verse.onrender.com/admin/organization_info/' \
  -H 'accept: application/json' \
  -H 'access_token: ab026eac22f97725fd6fc88a5fe3deac'
```

6. Response

```json
[]
```
