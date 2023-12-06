# Concurrency Control

## Case 1: Dirty Read When Viewing Events

1. Supervisor 1 calls `PUT /planner/1/create` and inserts a new event, Event 66.
2. Before the `create_event` function is finished executing, Volunteer 2 calls `GET /events/` to see the available events. Event 66 appears on the list.
3. Supervisor 1 ends up rolling back the `create_event` transaction.
4. Volunteer 2 calls `POST /schedules/2/events/66` and attempts to register for Event 66, and is denied because Event 66 no longer exists.

![Case1Diagram](https://gcdnb.pbrd.co/images/60p2Jc6ETkN7.png?o=1)

In our code, we control for this by using the default Postgres isolation level, `READ COMMITTED`. This prevents dirty reads from being performed. 

## Case 2: Dirty Read When Renaming Organization

1. Supervisor 2 calls `POST /organization/3/edit` and changes their organization's name to something different.
2. Before the `edit_organization` function is finished executing, Admin 1 calls `GET /admin/organization_info/`, which displays all the organizations including the one with its updated name.
3. Supervisor 2 was mistaken about the new name and rolls back the `edit_organization` transaction, returning the name of the organization to its original name.

![Case2Diagram](https://gcdnb.pbrd.co/images/ciFJUsHvkgve.png?o=1)

In our code, we control for this by using the default Postgres isolation level, `READ COMMITTED`. This prevents dirty reads from being performed. 

## Case 3: Dirty Read When Registering for Events

1. Volunteer 1 is tired of being discriminated against because of their age (8) and calls `POST /volunteers/1/update` on their laptop to change their birthday to 7 years later.
2. At the same time, on their cell phone , Volunteer 1 then registers for an event, calling `POST /volunteers/events/3`, which checks Volunteer 1's age and, seeing they meet the minimum age requirement, adds the event to their schedule.
3. Before the call to `update_volunteer_info` completes, Volunteer 1 has a near-instantaneous change of conscience about trying to scam a volunteer site and rolls back the transaction on their laptop.
4. Volunteer 1 is now registered for an event that is above their current age.

![Case3Diagram](https://gcdnb.pbrd.co/images/QAcIXgNZC7kq.png?o=1)

In our code, we control for this by using the default Postgres isolation level, `READ COMMITTED`. This prevents dirty reads from being performed. 
