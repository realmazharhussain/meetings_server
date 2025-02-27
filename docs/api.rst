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
Currently, the API uses token-based authentication. Include the token in the ``Authorization`` header::

    Authorization: Bearer <token>

Authentication Endpoints
----------------------

POST /login
~~~~~~~~~~
Authenticate or register a user and get a token. If the email exists, it will attempt to login; if not, it will create a new user.

**Request Body**::

    {
      "email": "user@example.com",
      "password": "password123"
    }

**Response**::

    {
      "userID": "token_string_here"
    }

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
        "image": "/placeholder.svg?height=300&width=500",
        "bookings": [
          {
            "id": "1",
            "date": "2024-03-20",
            "timeSlot": "09:00-10:00",
            "userName": "John Doe",
            "purpose": "Team Meeting"
          }
        ]
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
      "image": "/placeholder.svg?height=300&width=500",
      "bookings": [
        {
          "id": "1",
          "date": "2024-03-20",
          "timeSlot": "09:00-10:00",
          "userName": "John Doe",
          "purpose": "Team Meeting"
        }
      ]
    }

**Status Codes**:

* ``200``: Success
* ``404``: Room not found

Static Assets
------------

GET /placeholder.svg
~~~~~~~~~~~~~~~~~~~
Get a placeholder SVG image.

**Query Parameters**:

* ``width`` (optional): Image width in pixels (default: 500)
* ``height`` (optional): Image height in pixels (default: 300)

**Response**:
An SVG image with the specified dimensions.

**Example URLs**:

* ``/placeholder.svg`` - Default size (500x300)
* ``/placeholder.svg?width=800&height=600`` - Custom size

**Status Codes**:

* ``200``: Success
* ``400``: Invalid dimensions

Booking Endpoints
----------------

GET /bookings
~~~~~~~~~~~~
Get a list of all bookings with optional filters.

**Query Parameters**:

* ``roomId`` (optional): Filter bookings by room ID
* ``date`` (optional): Filter bookings by date (YYYY-MM-DD format)

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