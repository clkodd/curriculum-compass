# Performance Tuning

## Fake Data Modeling

**Guessstimations**:
- The median volunteer probably registers for about 3 events each, with the average events registered for slightly under 3
  - num_sched_rows = math.ceil(num_vol_rows * 2.7)

- There is probably 1 event for every 25 or so volunteers, with the average being slightly under
  - num_event_rows = math.ceil(num_vol_rows / 25.9)

- The median organization probably hosts around 4 events, with the average events per organization being a bit under 4
  - num_org_rows = math.ceil(num_event_rows / 4.3)

- The median organization probably has about 2 supervisors on the site, with the average being slightly above 2 supervisors per org
  - num_sup_rows = math.ceil(num_org_rows * 2.2)

From there, I played around with the number of volunteers to equal a million rows. 

Volunteers: 265500 rows

Volunteer schedule events: 716850 rows

Events: 10251 rows

Organizations: 2384 rows

Supervisors: 5245 rows

**Total**: 1000230 rows

[Python file used](https://github.com/clkodd/volunteer-verse/blob/main/populate_posts.py)


## Endpoint Testing Results

| Endpoint                                             | Time (ms) |
| :--------------------------------------------------- | :-------- |
| /volunteers                                          |    8.04   |
| /volunteers/{volunteer_id}/update                    |  126.55   |
| /volunteers/events/{event_id}                        |  164.68   |
| /volunteers/{volunteer_id}/display_registered_events |  601.07   |
| /volunteers/{volunteer_id}/remove                    |  171.26   |
| /volunteers/{volunteer_id}/events                    |  108.88   |
| /events/                                             |  641.16   |
| /planner/{event_organizer_id}/create                 |  403.99   |
| /planner/{event_id}/                                 |  146.51   |
| /organization/                                       |  169.35   |
| /organization/{organization_id}/edit                 |   53.11   |
| /organization/{org_id}/supervisor                    |   21.47   |
| /organization/supervisor/{supervisor_id}/edit        |   24.77   |
| /admin/reset                                         |   86.97   |
| /admin/organization_info/                            |   76.98   |


The slowest endpoints were the event search (`/events`, 641.16 ms), displaying the events a given volunteer registered for (`/volunteers/{volunteer_id}/display_registered_events`, 601.07 ms), and creating a new event (`/planner/{event_organizer_id}/create`, 403.99 ms).

## Performance Tuning
![Display Registered Events]([https://example.com/images/example.png](https://imgur.com/a/FKyMm7w)https://imgur.com/a/FKyMm7w)
The explain results reveal there is an inefficiency in the query, indicating areas for optimization. The absence of an index on the volunteer_id column suggests that the database engine might perform a full table scan, leading to the slowness. The initial time was over 600 milliseconds which is incredibly slow. Let's optimize it by creating an index on volunteer_schedule(volunteer_id). Through this indexing, we can see that runtime is now much faster at the total time is 1 ms. Now after indexing the entire endpoint runs in 59.77s which is significant improvement from 600+ ms.
