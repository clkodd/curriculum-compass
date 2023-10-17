# API Specification

## 1. Volunteer Registering

The API calls are made in this sequence when registering for events:
1. `Get Events`
2. `New Schedule`
3. `Add Event to Schedule` (Can be called multiple times)
4. `Register for Events`

An event can be removed from a schedule with the following API call:

5. `Remove Event from Schedule`

### 1.1. Get Events - `/events/` (GET)

Retreives the list of available events. 

**Returns**:

```json
[
    {
        "event_id": "integer",
        "name": "string", 
        "spots_left": "integer",
        "minimum_age": "integer",
        "activity_level": "integer", /* Between 1 and 3, 3 being the highest */
        "location": "string", /* A city name */
        "start_time": "datetime",
        "end_time": "datetime",
        "description": "string"
    }
]
```

### 1.2. New Schedule - `/schedules/` (POST)

Creates a new schedule for a specific volunteer.

**Request**: 

```json
{
    "volunteer": "string"
}
```

**Returns**: 

```json
{
    "schedule_id": "integer" /* Used in future calls to add events and register */
}
```

### 1.3. Add Event to Schedule - `/schedules/{schedule_id}/events/{event_id}` (PUT)

Adds a specific event to a schedule.

**Returns**: 

```json
{
    "success": "boolean" /* Checks for time conflicts */
}
```

### 1.4. Register for Events - `/schedules/{schedule_id}/register` (POST)

Handles the registration process for a specific schedule.

**Request**:

```json
{
    "confirm": "boolean"
}
```

**Returns**:

```json
{
    "total_events_registered": "integer",
    "total_hours": "integer"
}
```

### 1.5. Remove Event from Schedule - `/schedules/{schedule_id}/remove` (PUT)

Removes an event from a volunteer's schedule.

 **Request**:

 ```json
{
    "event_id": "integer"
}
```

**Returns**:

```json
{
    "schedule_id": "integer"
}
```

## 2. Event Creating

The API calls are made in this sequence when creating events:
1. `New Event`
2. `Get Event Plan`
3. `Post Events`

An event can be deleted with the following API calls:

4. `Delete Event`

### 2.1. New Event - `/event-planner/create` (POST)

Creates a new event. 

**Returns**:

```json
{
    "event_id": "integer" /* Used in future calls to modify the event */
}
```

### 2.2. Get Event Plan - `/event-planner/{event_id}` (PUT)

Adds event traits to the specified event, using the event's ID.

**Request**:

```json
[
    "name": "string", 
    "spots": "integer",
    "minimum_age": "integer",
    "activity_level": "integer", /* Between 1 and 3, 3 being the highest */
    "location": "string", /* A city name */
    "start_time": "datetime",
    "end_time": "datetime",
    "description": "string"
]
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 2.3. Post Events - `/event-planner/{event_id}/schedule` (POST)

Posts the list of specified events.

**Request**:

```json
{
    [
        "event_id": "integer"
    ]
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 2.4. Delete Event - `/event-planner/{event_id}/delete` (POST)

Removes an event from a volunteer's schedule.

 **Request**:

 ```json
{
    "event_id": "integer"
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

## 3. Admin Functions

### 3.1. Reset Site - `/admin/reset` (POST)

Deletes all events and schedules. 

### 3.2. Organizations Info - `/admin/organizations` (GET)

Returns a list of all verified volunteer organizations with active events scheduled.

**Returns**: 

```json
[
    {
        "organization": "string"
    }
]
```
