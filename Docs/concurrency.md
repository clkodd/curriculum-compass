# Concurrency Control

## Case 1: Non-Repeatable Read When Regstering for Events

In this case, when a user runs `GET /events/`, a list of all the events with at least 1 spot left are displayed. When registering for a specific event, it checks if the event has at least 1 spot left, and then adds the event to the user's schedule and updates the spots left.

1. User 1 runs `GET /events/`. Event 66 has 1 spot left.
2. User 2 calls `POST /schedules/2/events/66` and registers for Event 66. Event 66 now has 0 spots left.
3. User 1 calls `POST /schedules/1/events/66` and registers for Event 66. Event 66 now has -1 spots left.

In our code, we control for this by checking again when registering for an event if there is at least 1 spot left. So, in our code, if User 1 attempts to register for Event 66, the code would reject User 1's registration when it found that there were no spots left for Event 66. 

## Case 2: Phantom Read When Searching for Events

In this case, when a user runs `GET /search/`, a list of all the events that match the provided search criteria are displayed. 

1. User 1 calls `GET /search/`, filtering for all events taking place in San Luis Obispo, which displays 7 matching rows.
2. User 2 calls `PUT /planner/2/create` and creates a new event located in San Luis Obispo.
3. User 1 forgot the event ID of their desired event and calls `GET /search/` again to find it, using the same filtering for all events taking place in San Luis Obispo, but now the query returns 8 matching rows.

This can be controlled for by changing the isolation level of the transaction, from the default `READ COMMITTED` to `SERIALIZABLE`. This is appropriate because it's the only transaction isolation level that prevents phantom reads. 

## Case 3: 

Write up three cases where your service would encounter phenomenon if it had no concurrency control protection in place. 
Make a sequence diagram for each case.
What will you do in your code to ensure isolation of your transactions, and why is that the appropriate case? 

If you believe your transactions don't have any such cases, 
your transactions either aren't complex enough and you need to build something more interesting 
or you aren't understanding what issues are occurring. 

Note, this can be both how a particular transaction definition interacts with other transaction definitions, 
but also how a transaction definition interacts with other concurrent instances of itself. 
