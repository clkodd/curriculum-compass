# Example Flows

## Flow 1 - Volunteer Site Event Coordinator Event Posting

Ronnie comes to our volunteer website because she is in desperate need of volunteers for serving meals at the Midnight Mission. She intends to create an event for volunteers to sign up. Ronnie wants to input her event details/requirements for the volunteer event. To do so she:

- starts by calling `POST /event-planner` to get a new event with ID 9001.
- then Ronnie calls `POST /event-planner/9001` and passes in:
  - Name: "Midnight Mission Mania"
  - Spots: 50
  - Minimum age: 15
  - Activity level: 1
  - Location: "Los Angeles"
  - Start time: 2023-10-16T20:00:00Z
  - End time: 2023-10-16T23:59:59Z
  - Description: “Serve food to the homeless at the Midnight Mission to help those in need.”
- Finally, she calls `POST /event-planner/9001/schedule` to finish scheduling her event. The updates the database to say that there is a new event on October 16th with all her inputted information on it.

Ronnie gets her volunteers and the homeless are served meals.

## Flow 2 - Volunteer Deleting an Event

Ronnie had previously created an event for people to serve meals at Midnight Mission. She posted her volunteer opportunity to take place on October 16th, and it went great! It is now October 17th. She plans to delete the volunteer request from the website. 

- from her unique event she created, using its event_id, she calls `POST /event-organizer/{event_id}/delete`.
  
Ronnie has successfully deleted her volunteer Post.

## Flow 3 - Admin Resetting the Site

Binglethorpe is a site admin for Volunteer Verse. Due to a recent cybersecurity attack on the event planners' accounts that changed all the event locations to "Add me on Genshin Impact," it has become necessary to delete all the active events on the site. He intends to wipe the site by removing all the events and deleting the volunteers' schedules.

- starts by calling `GET /admin/organizations` to see all the different organization with active events, so he can notify them later.
- then Binglethorpe calls `POST /admin/reset`. All the schedules are reset, and every active event is deleted from the list.
- Finally, he calls `GET /admin/organizations` to ensure the reset worked as intended. No organizations show up, so Binglethorpe is confident in his reset.

The events and schedules are cleared. Binglethorpe is moritifed and enrolls in CSC 321 to prevent future attacks.

## Flow 4 - Volunteer Registering for an Event

Roxanne is a high school student and she is in desperate need of more volunteering hours to graduate high school. First, Roxanne must create a schedule by calling 
- starts by calling `GET /events/` to see the list of posted volunteer events she can register for. She sees one she likes with an event_id of 300, and will use that event_id to sign up for it later.
- then creates a new schedule object by calling `POST /events/schedules` and receives the schedule ID 707.
- Roxanne then calls `PUT /schedules/707/events/300` to register for the event she saw earlier. This will return a success if she is able to add this to her schedule.
- Roxanne repeats the previous step to register for as many events as she wants.
- She confirms that she is going to add the current event to her schedule and finalizes the registering process by calling `POST /schedule/707/register`, which returns the total events and their total hours that she has decided to sign up for.
  
Roxanne has successfully registered for volunteer opportunities. 

