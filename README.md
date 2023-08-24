**Overview:**

 Implemented REST api with all CRUD operations on User-Events scenario. A new user can be created and add/update/delete associated events.
Each event contains Title and Description. 

Each user can potentially have multiple events associated with them.
Each event should have two main attributes: a "Title" to briefly describe the event and a "Description"
to provide more detailed information about the event.

A popular open-source relational database, PostgreSQL to store and manage your data. PostgreSQL provides robust support for structured data storage.

JWT is being used for authentication. When a user logs in, they receive a JWT, which they then include in the headers of their API requests. 
The server can then validate this token to identify the user and permit or deny access to specific resources.

All Operations - CRUD calls
1. Create a new User: POST localhost:8080/register
2. Login User with credentials: POST localhost:8080/login
3. Add a new Event: POST localhost:8080/event
4. Get User specific events: GET localhost:8080/user/events
5. Get all events and filter option with title and description: GET localhost:8080/events?title=event1&description=test_event
6. Update an Event by using Event ID: PUT localhost:8080/event/2
7. Delete an Event by using Event ID: DELETE localhost:8080/event/2

**Setup:**

1. Set up Postgres database and update SQLALCHEMY_CONFIG_URI as per your configuration.
2. To view database contents, you can use PGAdmin
3. Run command pip install -r requirements.txt
4. Run "flask init" to create Database models in Database tables.
5. Run Flask app, it will start run in Debug mode on 8080 port.
6. Once application successfully started, you can refer to Postman collection and run/test all operations.






