# Concurrency Control

## Case 1: Non-Repeatable Read When Regstering for Events

In this case, when a user runs `GET /events/`, a list of all the events with at least 1 spot left are displayed. When registering for a specific event, it checks if the event has at least 1 spot left, and then adds the event to the user's schedule and updates the spots left.

1. User 1 runs `GET /events/`. Event 66 has 1 spot left.
2. User 2 calls `POST /schedules/2/events/66` and registers for Event 66. Event 66 now has 0 spots left.
3. User 1 calls `POST /schedules/1/events/66` and registers for Event 66. Event 66 now has -1 spots left.

In our code, we control for this by checking again when registering for an event if there is at least 1 spot left. So, in our code, if User 1 attempts to register for Event 66, the code would reject User 1's registration when it found that there were no spots left for Event 66.

## Case 2:

## Case 3: 

Write up three cases where your service would encounter phenomenon if it had no concurrency control protection in place. 
Make a sequence diagram for each case.
What will you do in your code to ensure isolation of your transactions, and why is that the appropriate case? 

If you believe your transactions don't have any such cases, 
your transactions either aren't complex enough and you need to build something more interesting 
or you aren't understanding what issues are occurring. 

Note, this can be both how a particular transaction definition interacts with other transaction definitions, 
but also how a transaction definition interacts with other concurrent instances of itself. 

Please document all of this in a markdown file named: concurrency.md checked into your group's github.
