# API Specification

## 1. Volunteer Registering

The API calls are made in this sequence when registering for events:
1. `Get Events`
2. `New Volunteer`
3. `Add an event to Volunteer's Schedule` (Can be called multiple times)
4. `Registered Events`

An event can be removed from a schedule with the following API call:

5. `Remove Event from Schedule`

### 1.1. search - `/events/` (GET)

Retrieves the list of available events. [COMPLEX Endpoint]

**Returns**:

```json
[
    {
        "event_id": "integer",
	"organization_name": "string",
        "name": "string",
	"supervisor_email": "string",
        "total_spots": "integer",
        "minimum_age": "integer",
        "activity_level": "integer", /* Between 0, 1, 2, 3, 4, 5 with 5 being the highest activity level */
        "location": "string", /* A city name */
        "start_date": "datetime",
        "end_time": "datetime",
        "description": "string"
    }
]
```

### 1.2. New Volunteer - `/volunteers/` (POST)

Creates a new volunteer. 

**Request**: 

```json
{
    	"volunteer_name": "string",
	"city": "string", 
	"birthday": "int",
	"email": "string",
}

```

**Returns**: 

```json
{
      "volunteer_id": "int"
}
```

### 1.3. Update Volunteer - `/volunteers/{volunteer_id}/update` (POST)

Creates a new volunteer. 

**Request**: 

```json
{
	"volunteer_id": "int",
    	"volunteer_name": "string",
	"city_name": "string", 
	"birthday": "int",
	"email": "string"
}

```

**Returns**: 

```json
{
      "OK"
}
```

### 1.4. Add Event to Schedule - `/volunteers/events/{event_id}` (POST)

Adds a specific event to a schedule. Checking for time, age conflicts, and duplicate events. [COMPLEX Endpoint]

**Returns**: 

```json
{
    "success": "boolean" /* Checks for time conflicts */
}
```

### 1.5. Display Registered Events - `/volunteers/{volunteer_id}/display_registered_events` (POST)

Takes the total sum of events and hours completed overall for a volunteer.

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


### 1.6. Get all Volunteer Events - `/volunteers/{volunteer_id}/events` (POST)

Gets all the events that a specific volunteer is registered for and gives info on each event.

 **Request**:

 ```json
{
    "volunteer_id": "int"
}
```

**Returns**:

```json
{
        "name": "string",
        "total_spots": "integer",
        "activity_level": "integer", /* Between 0, 1, 2, 3, 4, 5 with 5 being the highest activity level */
        "location": "string", /* A city name */
        "start_date": "datetime",
        "end_time": "datetime",
        "description": "string"
}
```

### 1.7. Remove Event from Schedule - `/volunteers/{event_id}/remove` (POST)

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
    "confirm": "boolean"
}
```

## 2. Event Creating

The API calls are made in this sequence when creating events:
1. `Create Event`

An event can be deleted with the following API calls:

2. `Delete Event`


### 2.1 Create Event - `/event-planner/{event_id}/{event_organizer_id}` (POST)

Create a volunteer event. [COMPLEX Endpoint]

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
    "event_id": "int"
}
```


### 2.2. Delete Event - `/event-planner/{event_id}/delete` (POST)

Removes an event from the events table. In turn also deletes all references to that event_id removing event from volunteer table.

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

Deletes all organizations and volunteers. 

### 3.2. Organizations Info - `/admin/organizations` (GET)

Returns a list of all volunteer organizations with active events scheduled.

**Returns**: 

```json
[
    {
        "organization": "string"
    }
]
```

## 4. Organization Functions

### 4.1. Create Organization `/organization/` (POST)

Creates a new organization.

**Request**: 

```json
{
    "name": "string",
	"city": "string", 
}

```

**Returns**: 

```json
{
      "org_id": "int"
}
```


### 4.2. Create Supervisor `/organization/{org_id}/supervisor` (POST)

Creates a new supervisor.

**Request**: 

```json
{
    	"sup_name": "string",
	"email": "string",
}

```

**Returns**: 

```json
{
      "sup_id": "int"
}
```

### 4.3. Edit Organization `/organization/{org_id}/edit` (POST)

Edits existing organization.

**Request**: 

```json
{
    	"org_id": "int",
	"name": "string",
	"city": "string"
}

```

**Returns**: 

```json
{
	"org_id": "int",
	"name": "string",
	"city": "string"
}
```


### 4.4. Edit Supervisor `/organization/supervisor/{org_id}/edit` (POST)

Edits existing supervisor.

**Request**: 

```json
{
    	"sup_id": "int",
	"org_id": "int",
	"name": "string",
	"email": "string"
}

```

**Returns**: 

```json
{
	"sup_id": "int",
	"org_id": "int",
	"name": "string",
	"email": "string"
}
```

