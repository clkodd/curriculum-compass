# Example Flows

## Flow 1 - Volunteer Site Event Coordinator Event Posting

Ronnie comes to our volunteer website because she is in desperate need of volunteers for serving meals at the Midnight Mission. She intends to create an event for volunteers to sign up. To do so she: First, Ronnie makes an account that generates an unique organizer ID by calling POST /event-organizer. Ronnie then wants to input her event details/requirements for the volunteer event. 

- starts by calling `POST /event-organizer` to get a new schedule with ID 9001.
- then Ronnie calls `POST /event-organizer/9001/plan` and passes in:
  - Name: "Midnight Mission Mania"
  - Spots: 50
  - Minimum age: 15
  - Activity level: 1
  - Location: "Los Angeles"
  - Start time: 2023-10-16T20:00:00Z
  - End time: 2023-10-16T23:59:59Z
  - Description: “Serve food to the homeless at the Midnight Mission to help those in need.”
- Finally, she calls `POST /event-organizer/9001/schedule` to finish scheduling her event. The updates the database to say that there is a new event on October 16th with all her inputted information on it.

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
