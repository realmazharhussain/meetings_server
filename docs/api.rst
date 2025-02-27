Meeting Room Booking API Documentation
====================================

Overview
--------
This API provides endpoints for managing meeting room bookings. It allows users to view available rooms, create bookings, and manage existing bookings.

Base URL
--------
All endpoints are relative to the base URL of your server.

Authentication
-------------
The API uses cookie-based authentication. A secure HTTP-only cookie named ``session_token`` is set upon successful login.
All endpoints (except /login) require this cookie to be present and valid.

**Error Responses**:

* ``401``: Authentication required (missing or invalid token)
* ``403``: Access denied (attempting to access/modify other users' data)

Authentication Endpoints
----------------------

POST /login
~~~~~~~~~~
Authenticate or register a user. If the email exists, it will attempt to login; if not, it will create a new user.
On success, sets a secure HTTP-only cookie with the session token.

**Request Body**::

    {
      "email": "user@example.com",
      "password": "password123"
    }

**Response**::

    {
      "message": "Login successful"
    }

**Cookies Set**:

* ``session_token``: Secure, HTTP-only session token

**Status Codes**:

* ``200``: Success (both for login and registration)
* ``400``: Invalid request format
* ``401``: Invalid password for existing email

Room Endpoints
-------------

GET /rooms
~~~~~~~~~
Get a list of all available rooms.

**Response**::

    [
      {
        "id": "1",
        "name": "Brainstorm Room",
        "capacity": 4,
        "amenities": ["Whiteboard", "TV", "HDMI Cable"],
        "image": "https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=500&h=300&auto=format&fit=crop&q=80"
      }
    ]

**Status Codes**:

* ``200``: Success

GET /rooms/{id}
~~~~~~~~~~~~~~
Get details of a specific room.

**Parameters**:

* ``id``: Room ID (string)

**Response**::

    {
      "id": "1",
      "name": "Brainstorm Room",
      "capacity": 4,
      "amenities": ["Whiteboard", "TV", "HDMI Cable"],
      "image": "https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=500&h=300&auto=format&fit=crop&q=80"
    }

**Status Codes**:

* ``200``: Success
* ``404``: Room not found

Booking Endpoints
----------------

GET /bookings
~~~~~~~~~~~~
Get a list of bookings with optional filters.

**Query Parameters**:

* ``roomId`` (optional): Filter bookings by room ID
* ``date`` (optional): Filter bookings by date (YYYY-MM-DD format)
* ``mine`` (optional): When set to "true", only returns bookings for the authenticated user

**Response**::

    [
      {
        "id": "1",
        "roomId": "1",
        "date": "2024-03-20",
        "timeSlot": "09:00-10:00",
        "userName": "John Doe",
        "purpose": "Team Meeting"
      }
    ]

**Status Codes**:

* ``200``: Success
* ``401``: Authentication required

POST /bookings
~~~~~~~~~~~~~
Create one or multiple bookings.

**Request Body**

Single booking::

    {
      "roomId": "1",
      "date": "2024-03-20",
      "timeSlot": "09:00-10:00",
      "userName": "John Doe",
      "purpose": "Team Meeting"
    }

Multiple bookings::

    [
      {
        "roomId": "1",
        "date": "2024-03-20",
        "timeSlot": "09:00-10:00",
        "userName": "John Doe",
        "purpose": "Team Meeting"
      },
      {
        "roomId": "2",
        "date": "2024-03-20",
        "timeSlot": "10:00-11:00",
        "userName": "Jane Smith",
        "purpose": "Client Call"
      }
    ]

**Response**

Single booking success::

    {
      "id": "1",
      "roomId": "1",
      "date": "2024-03-20",
      "timeSlot": "09:00-10:00",
      "userName": "John Doe",
      "purpose": "Team Meeting"
    }

Multiple bookings success::

    [
      {
        "id": "1",
        "roomId": "1",
        "date": "2024-03-20",
        "timeSlot": "09:00-10:00",
        "userName": "John Doe",
        "purpose": "Team Meeting"
      },
      {
        "id": "2",
        "roomId": "2",
        "date": "2024-03-20",
        "timeSlot": "10:00-11:00",
        "userName": "Jane Smith",
        "purpose": "Client Call"
      }
    ]

Error response::

    {
      "error": "Some bookings could not be created",
      "details": [
        {
          "booking": {
            "roomId": "1",
            "date": "2024-03-20",
            "timeSlot": "09:00-10:00",
            "userName": "John Doe",
            "purpose": "Team Meeting"
          },
          "error": "Time slot already booked"
        }
      ]
    }

**Status Codes**:

* ``201``: Booking(s) created successfully
* ``400``: Invalid request format or validation error
* ``404``: Room not found
* ``409``: Time slot already booked

GET /bookings/{id}
~~~~~~~~~~~~~~~~~
Get details of a specific booking.

**Parameters**:

* ``id``: Booking ID (string)

**Response**::

    {
      "id": "1",
      "roomId": "1",
      "date": "2024-03-20",
      "timeSlot": "09:00-10:00",
      "userName": "John Doe",
      "purpose": "Team Meeting"
    }

**Status Codes**:

* ``200``: Success
* ``404``: Booking not found

DELETE /bookings/{id}
~~~~~~~~~~~~~~~~~~~~
Delete a specific booking.

**Parameters**:

* ``id``: Booking ID (string)

**Response**: Empty response body

**Status Codes**:

* ``204``: Booking successfully deleted
* ``404``: Booking not found

Data Formats
-----------

Date Format
~~~~~~~~~~
Dates should be provided in ``YYYY-MM-DD`` format (e.g., "2024-03-20")

Time Slot Format
~~~~~~~~~~~~~~
Time slots should be provided in ``HH:MM-HH:MM`` format (e.g., "09:00-10:00")

Room ID Format
~~~~~~~~~~~~~
Room IDs are strings containing numeric values (e.g., "1", "2")

Booking ID Format
~~~~~~~~~~~~~~~
Booking IDs are strings containing numeric values (e.g., "1", "2")

Error Responses
--------------
All error responses follow this format::

    {
      "error": "Error message here"
    }

Common error status codes:

* ``400``: Bad Request - Invalid input or validation error
* ``401``: Unauthorized - Authentication required
* ``404``: Not Found - Resource doesn't exist
* ``409``: Conflict - Resource conflict (e.g., double booking)
* ``500``: Internal Server Error - Server-side error 