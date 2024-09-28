### Creating Data file
## Step1: generate_documents.py
# This file is used to generate 100 documents that are migrated to mysql

This will generate 100 documents like the sample json document provided

Then I used MySQL to build the database. Run teh following in MYSQL database query window

```sql
-- clustersclusters-- Create the database
CREATE DATABASE IF NOT EXISTS documents_db;
USE documents_db;

-- Create Clusters table
CREATE TABLE Clusters (
    clusterId VARCHAR(50) PRIMARY KEY
);

-- Create Users table
CREATE TABLE Users (
    id INT PRIMARY KEY,
    userId VARCHAR(9) UNIQUE NOT NULL,
    originationTime INT NOT NULL,
    clusterId VARCHAR(50),
    FOREIGN KEY (clusterId) REFERENCES Clusters(clusterId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Create Phones table
CREATE TABLE Phones (
    phoneId INT AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(20) UNIQUE NOT NULL,
    phoneModel VARCHAR(50),
    purchaseDate DATE
);

-- Create Voicemails table
CREATE TABLE Voicemails (
    vmId INT AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(20) UNIQUE NOT NULL,
    setupDate DATE,
    storageCapacity INT
);

-- Create User_Phones table
CREATE TABLE User_Phones (
    userId INT,
    phoneId INT,
    PRIMARY KEY (userId, phoneId),
    FOREIGN KEY (userId) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (phoneId) REFERENCES Phones(phoneId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create User_Voicemails table
CREATE TABLE User_Voicemails (
    userId INT,
    vmId INT,
    PRIMARY KEY (userId, vmId),
    FOREIGN KEY (userId) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (vmId) REFERENCES Voicemails(vmId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

# Entities and Relationships

# Clusters

Represents different server domains.
Attributes: clusterId.

# Users

Represents individual users.
Attributes: Unique _id, userId, originationTime, and associated clusterId.

# Phones

Represents phone devices.
Attributes: Unique identifier and specific phone-related attributes.

# Voicemails

Represents voicemail devices.
Attributes: Unique identifier and specific voicemail-related attributes.

# User_Phones

#Junction table to handle the many-to-many relationship between Users and Phones.

# User_Voicemails

Junction table to handle the many-to-many relationship between Users and Voicemails.
```
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
```

## Step2: Then I built FastAPI backend application with the following features:

1. 🔑 **OAuth2 Authentication:** Secure API endpoints using JWT (JSON Web Tokens).
2. 🔄 **CORS Support:** Allow cross-origin requests from your frontend.
3. 🗄️ **MySQL Integration:** Store and manage data using a MySQL database.
4. 🌐 **RESTful API Endpoints:** Provide endpoints to retrieve records by phone number, voicemail, user ID, and cluster ID within a specified date range.
5. 📝 **Logging:** Implement robust logging for monitoring and debugging.
6. 📂 **Data Migration:** Migrate data from a JSON file (`documents.json`) to the MySQL database.


To run this application:

You can clone it:
```bash
git clone https://github.com/safakhan413/fast-react-app.git
#cd into the folder

# Create the environment (Windows)
python -m venv env
# Activate your environment
path\to\your\fast-react-app\env\Scripts\activate

# Then install all the relevant packages
pip install -r requirements.txt

```

Now you are ready to migrate your database using app/migrate.py file

Remember to change line 140 in migrate.py to point to the actual location of documents.json

```python

      json_path = os.path.join(os.path.dirname(__file__), '..', 'documents.json')

```

____________________________________________________________________________________________________________
Databases
_________________________________________________________________



