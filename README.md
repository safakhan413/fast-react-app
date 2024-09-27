### Creating Data file
generate_documents.py is used to generate 100 documents that are migrated to mysql

We'll build a FastAPI backend application with the following features:

OAuth2 Authentication: Secure API endpoints using JWT (JSON Web Tokens).
CORS Support: Allow cross-origin requests from your frontend.
MySQL Integration: Store and manage data using a MySQL database.
RESTful API Endpoints: Provide endpoints to retrieve records by phone number, voicemail, user ID, and cluster ID within a specified date range.
Logging: Implement robust logging for monitoring and debugging.
Data Migration: Migrate data from a JSON file (documents.json) to the MySQL database.

____________________________________________________________________________________________________________
Databases
_________________________________________________________________


Entities and Relationships
Clusters

Represents different server domains.
Attributes: clusterId.
Users

Represents individual users.
Attributes: Unique _id, userId, originationTime, and associated clusterId.
Phones

Represents phone devices.
Attributes: Unique identifier and specific phone-related attributes.
Voicemails

Represents voicemail devices.
Attributes: Unique identifier and specific voicemail-related attributes.
User_Phones

Junction table to handle the many-to-many relationship between Users and Phones.
User_Voicemails

Junction table to handle the many-to-many relationship between Users and Voicemails.

+-----------+          +-----------+          +----------+          +------------+
|  Clusters |          |   Users   |          |  Phones  |          | Voicemails |
+-----------+          +-----------+          +----------+          +------------+
| clusterId |<-------->|    id     |          | phoneId  |          | vmId       |
|  (PK)     |          | userId    |          | identifier|         | identifier |
+-----------+          | origTime  |          | ...      |          | ...        |
                       | clusterId |<-------->| (FK)     |          | (FK)       |
                       +-----------+          +----------+          +------------+
                             |                     |                      |
                             |                     |                      |
                             |                     |                      |
                             v                     v                      v
                      +--------------+     +----------------+     +------------------+
                      | User_Phones  |     | User_Voicemails|     | ...              |
                      +--------------+     +----------------+     +------------------+
                      | userId (FK)  |     | userId (FK)    |     |                  |
                      | phoneId (FK) |     | vmId (FK)      |     |                  |
                      +--------------+     +----------------+     +------------------+
