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
### /volunteers/{volunteer_id}/display_registered_events
![Display Registered Events Explain](https://i.imgur.com/VOSaqdq.png)
The explain results reveal there is an inefficiency in the query, indicating areas for optimization. The absence of an index on the volunteer_id column suggests that the database engine might perform a full table scan, leading to the slowness. The initial time was over 600 milliseconds which is incredibly slow. Let's optimize it by creating an index on volunteer_schedule(volunteer_id). Through this indexing, we can see that runtime is now much faster at the total time is 1 ms. Now after indexing the entire endpoint runs in 59.77s which is significant improvement from 600+ ms.
![Rerunning Display Registered Events with Indexing](https://i.imgur.com/NAbhR5A.png)

### /events/

#### Query 1
![Events](https://i.imgur.com/ehX1Fbp.png)

The explain results indicate an inefficiency in the query, pinpointing areas that can be optimized. The absence of an ID for the event ID contributes to the sluggish performance, causing a delay of 500 milliseconds. Recognizing this bottleneck, we can enhance the query speed by introducing an index on the event_id column. After indexing, the entire endpoint now executes in 59.77 milliseconds, showcasing an improvement from the initial 600+ milliseconds.
![Events with Indexing](https://i.imgur.com/8D9VQ6F.png)

#### Query 2
![Events2](https://i.imgur.com/ehX1Fbp.png)

The explain results indicate that adding an index for the volunteer schedule event ID did not yield significant improvements, resulting in only a 20 milliseconds faster execution. Therefore, we decided not to implement this index. 

#### Query 3
![Events3](https://i.imgur.com/peK426T.png)
![Events3](https://i.imgur.com/peK426T.png)

We added a materialized view to enhance the efficienncy since the indexing didn't yield the efficiency we wanted. A materialized view caches the results each time and we make sure that users don't get stale data by updating the cache every time the reference data is updated.

### /planner/{event_organizer_id}/create
#### Query 1
![create1](https://i.imgur.com/CbYXSmS.png)

#### Query 2
![create2](https://i.imgur.com/1cnqH6r.png)

#### Query 3
![create3](https://i.imgur.com/iClKx6n.png)

The explain results indicate an inefficiency in the query execution, therefore there are areas for improvement. Let's increase efficiency by adding an index on events(name).

#### Indexing Added
![index_added](https://i.imgur.com/L4z3np2.png)

As a result of the indexing, we can cut planning time in half and removed almost 5 milliseconds off execution time.
