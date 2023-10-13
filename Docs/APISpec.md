# API Specification
## 1. Volunteer Registering

The API calls are made in this sequence when registering for events:
1. `Get Events`
2. `New Schedule`
3. `Add Event to Schedule` (Can be called multiple times)
4. `Register for Events`

### 1.1 Get Events - `/events/` (GET)

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

### 1.2 New Schedule - `/schedules/` (POST)

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

### 1.3 Add Event to Schedule - `/schedules/{schedule_id}/events/{event_id}` (PUT)

Adds a specific event to a schedule.

**Request**: 

```json
{
    
}
```

**Returns**: 

```json
{
    "success": "boolean" /* Checks for time conflicts */
}
```

### 1.4 Register for Events - `/schedules/{schedule_id}/register` (POST)

Handles the registration process for a specific schedule.





## 2. Event Creating

The API calls are made in this sequence when creating events:
1. `Get Events`
2. `New Schedule`
3. `Add Event to Schedule` (Can be called multiple times)
4. `Register for Events`

### 2.1 Get - `//` (GET)




## 3. Admin Functions

The API calls are made in this sequence when creating events:
1. `Get Events`
2. `New Schedule`
3. `Add Event to Schedule` (Can be called multiple times)
4. `Register for Events`

### 1.1 Get Events - `/events/` (GET)
