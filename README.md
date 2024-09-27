### Creating Data file
generate_documents.py is used to generate 100 documents that are migrated to mysql

We'll build a FastAPI backend application with the following features:

OAuth2 Authentication: Secure API endpoints using JWT (JSON Web Tokens).
CORS Support: Allow cross-origin requests from your frontend.
MySQL Integration: Store and manage data using a MySQL database.
RESTful API Endpoints: Provide endpoints to retrieve records by phone number, voicemail, user ID, and cluster ID within a specified date range.
Logging: Implement robust logging for monitoring and debugging.
Data Migration: Migrate data from a JSON file (documents.json) to the MySQL database.

Some observations:

Separate Voicemail Table: Voicemails should be a distinct entity, not just another type of device.
Many-to-Many Relationships:
Users ↔ Devices: A user can have multiple devices, and a device can be associated with multiple users.
Users ↔ Voicemails: Similarly, a user can have multiple voicemails, and a voicemail can be associated with multiple users.
Additional Fields:
Cluster IDs: Each user is associated with a specific cluster.
Other Metadata: Fields like _id and originationTime provide additional context.