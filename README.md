# Full Stack Application with FastAPI and React

This project is a full-stack web application that includes a FastAPI backend and a React frontend. The backend uses MySQL as the database and implements token-based authentication with JWT. The frontend is built using React with Material-UI and communicates with the FastAPI backend to fetch, display, and export data.

## Project Overview

This application allows users to log in, query data from the backend, and export the results to a CSV file. The backend is built with FastAPI and uses JWT-based authentication. The frontend uses React for UI, with Material-UI components for styling.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, MySQL, JWT, Pydantic
- **Frontend**: React, Material-UI, Axios, react-csv
- **Database**: MySQL
- **Other**: Python 3.9+, Node.js 14+

## Creating Data File

### Step 1: `generate_documents.py`
This file is used to generate 100 documents that will be migrated to MySQL. These documents follow the format of the provided sample JSON document.

Next, use MySQL to build the database. Run the following in the MySQL query window:

```sql
-- Create the database
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

## Entities and Relationships

### Clusters
Represents different server domains.  
**Attributes**: `clusterId`.

### Users
Represents individual users.  
**Attributes**: `id`, `userId`, `originationTime`, and associated `clusterId`.

### Phones
Represents phone devices.  
**Attributes**: `phoneId`, `identifier`, `phoneModel`, `purchaseDate`.

### Voicemails
Represents voicemail devices.  
**Attributes**: `vmId`, `identifier`, `setupDate`, `storageCapacity`.

### User_Phones
Junction table to handle the many-to-many relationship between `Users` and `Phones`.

### User_Voicemails
Junction table to handle the many-to-many relationship between `Users` and `Voicemails`.

```plaintext
+-----------+          +-----------+          +----------+          +------------+
|  Clusters |          |   Users   |          |  Phones  |          | Voicemails |
+-----------+          +-----------+          +----------+          +------------+
| clusterId |<-------->|    id     |          | phoneId  |          | vmId       |
|  (PK)     |          | userId    |          | identifier|         | identifier |
+-----------+          | origTime  |          | ...      |          | ...        |
                       | clusterId |<-------->| (FK)     |          | (FK)       |
                       +-----------+          +----------+          +------------+
                             |                     |                      |
                             v                     v                      v
                      +--------------+     +----------------+     +------------------+
                      | User_Phones  |     | User_Voicemails|     | ...              |
                      +--------------+     +----------------+     +------------------+
                      | userId (FK)  |     | userId (FK)    |     |                  |
                      | phoneId (FK) |     | vmId (FK)      |     |                  |
                      +--------------+     +----------------+     +------------------+
```

## Step 2: FastAPI Backend Features

1. 🔑 **OAuth2 Authentication**: Secure API endpoints using JWT (JSON Web Tokens).
2. 🔄 **CORS Support**: Allow cross-origin requests from your frontend.
3. 🗄️ **MySQL Integration**: Store and manage data using a MySQL database.
4. 🌐 **RESTful API Endpoints**: Provide endpoints to retrieve records by phone number, voicemail, user ID, and cluster ID within a specified date range.
5. 📝 **Logging**: Implement robust logging for monitoring and debugging.
6. 📂 **Data Migration**: Migrate data from a JSON file (`documents.json`) to the MySQL database.

## How to Run This Application

Clone the repository:

```bash
git clone https://github.com/safakhan413/fast-react-app.git
cd fast-react-app
```

### Setting up the Backend

1. **Create the virtual environment** (Windows):
    ```bash
    python -m venv env
    ```

2. **Activate your environment**:
    ```bash
    path\to\your\fast-react-app\env\Scripts\activate
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Update the `SQLALCHEMY_DATABASE_URL` in the `database.py` file** with your own credentials:
    ```python
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://<user>:<password>@<host>/<database>"
    ```

    Example:
    ```plaintext
    usname: admin
    pwd: eE9OnSygIreDzQO
    ```

5. **Generate a hashed password** for your `.env` file:
    ```bash
    python hash_password.py
    ```

6. **Update your `.env` file** with the hashed password:
    ```plaintext
    ADMIN_USERNAME=admin
    ADMIN_PASSWORD_HASH=$2b$12...
    ```

7. **Migrate the database** using `app/migrate.py`. Make sure to update line 140 to point to the correct location of `documents.json`:
    ```python
    json_path = os.path.join(os.path.dirname(__file__), '..', 'documents.json')
    ```

    Run the migration:
    ```bash
    cd app
    python migrate.py
    ```

8. **Run the FastAPI application**:
    ```bash
    python run.py
    ```

    The application will be available at:
    ```plaintext
    http://127.0.0.1:8000
    ```

## API Endpoints

### Authentication

- **POST** `/token`: User login, returns a JWT token.  
  Request body: `username`, `password`.  
  Response: `{ access_token: <token>, token_type: "bearer" }`

### Data Retrieval

- **GET** `/users/`: Fetches user data based on filters.  
  Query parameters: `start_time`, `end_time`, `parameter`.  
  Authorization: Requires Bearer token.

---

## Frontend Setup

### 1. Navigate to the Frontend Directory

```bash
cd frontend
```

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Run the Frontend Server

```bash
npm start
```

The frontend will be available at:

```plaintext
http://localhost:3000
```

---

## Usage

1. **Login**:  
   Navigate to [http://localhost:3000/login](http://localhost:3000/login), enter your credentials, and submit to authenticate.

2. **Search and Export Data**:  
   After logging in, use the search page to query records based on parameters such as phone number, voicemail, user ID, or cluster ID, and export results to CSV.

---

## API Documentation

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)



## Screenshots

Here are some screenshots of the application in action:

### Login Page
```markdown
```

![Login Page](https://github.com/safakhan413/fast-react-app/blob/main/loginpage.png "Login Page")

### Data Viewer Page

![Data Viewer Page](https://github.com/safakhan413/fast-react-app/blob/main/datapage.png "Data Viewer Page")

```