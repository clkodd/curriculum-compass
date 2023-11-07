# Example workflow - Volunteer Site Event Coordinator Event Posting

Ronnie comes to our volunteer website because she is in desperate need of volunteers for serving meals at the Midnight Mission. She intends to create an event for volunteers to sign up. Ronnie wants to input her event details/requirements for the volunteer event. To do so she:

- starts by calling `POST /event-planner` to get a new event with ID 1.
- then Ronnie calls `POST /event-planner/1` and passes in:
  - Name: "Midnight Mission Mania"
  - Spots: 50
  - Minimum age: 15
  - Activity level: 1
  - Location: "Los Angeles"
  - Start time: "2023-11-04T20:00:00Z"
  - End time: "2023-11-04T23:59:59Z"
  - Description: “Serve food to the homeless at the Midnight Mission to help those in need.”
- Finally, she calls `POST /event-planner/1/schedule` to finish scheduling her event. The updates the database to say that there is a new event on November 4th with all her inputted information on it.

Ronnie gets her volunteers and the homeless are served meals.

# Testing results
1. Calling 

```html
```

2. Response

```json
```

3. Calling 

```html
```

4. Response

```json
```

5. Calling 

```html
```

6. Response

```json
```

7. Calling 

```html
```

8. Response

```json
```

# Example workflow - Volunteer Deleting an Event

Ronnie had previously created an event for people to serve meals at Midnight Mission. She posted her volunteer opportunity to take place on November 4th, and it went great! It is now November 6th. She plans to delete the volunteer request from the website. 

- from her unique event she created, using its event_id, she calls `POST /event-organizer/{event_id}/delete`.

Ronnie has successfully deleted her volunteer Post.

# Testing results
1. Calling 

```html
```

2. Response

```json
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
```

2. Response

```json
```

3. Calling `POST /admin/reset`

```html
```

4. Response

```json
```

5. Calling `GET /admin/organizations`

```html
```

6. Response

```json
```
