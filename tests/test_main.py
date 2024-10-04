import sys
import os
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.main import app, get_db
from app.database import Base
from app import models
from app.auth import get_current_user

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Mock the current user for authentication
def override_get_current_user():
    return {"username": "testuser"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# Load test data from documents.json
def load_test_data(db):
    with open('documents.json', 'r') as f:
        data = json.load(f)
        for item in data:
            # Create or get the cluster
            cluster_id = item.get('clusterId')
            if cluster_id:
                cluster = db.query(models.Cluster).filter_by(clusterId=cluster_id).first()
                if not cluster:
                    cluster = models.Cluster(clusterId=cluster_id)
                    db.add(cluster)
                    db.commit()
                    db.refresh(cluster)
            else:
                cluster = None

            # Create the user
            user = models.User(
                id=item['_id'],
                userId=item['userId'],
                originationTime=item['originationTime'],
                clusterId=cluster.clusterId if cluster else None
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            # Add phones
            for phone_identifier in item['devices'].get('phone', []):
                phone = db.query(models.Phone).filter_by(identifier=phone_identifier).first()
                if not phone:
                    phone = models.Phone(identifier=phone_identifier)
                    db.add(phone)
                    db.commit()
                    db.refresh(phone)
                # Create association
                if phone not in user.phones:
                    user.phones.append(phone)
                    db.commit()

            # Add voicemails
            for voicemail_identifier in item['devices'].get('voicemail', []):
                voicemail = db.query(models.Voicemail).filter_by(identifier=voicemail_identifier).first()
                if not voicemail:
                    voicemail = models.Voicemail(identifier=voicemail_identifier)
                    db.add(voicemail)
                    db.commit()
                    db.refresh(voicemail)
                # Create association
                if voicemail not in user.voicemails:
                    user.voicemails.append(voicemail)
                    db.commit()

@pytest.fixture(scope="module")
def test_client():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Load test data
    load_test_data(db)
    db.close()
    yield client
    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)

def test_get_users_order_by_user_id(test_client):
    response = test_client.get("/users/", params={
        "start_time": 0,
        "end_time": 9999999999,
        "parameter": "user_id"
    })
    assert response.status_code == 200
    data = response.json()
    user_ids = [user['userId'] for user in data]
    assert user_ids == sorted(user_ids)

def test_get_users_order_by_phone(test_client):
    response = test_client.get("/users/", params={
        "start_time": 0,
        "end_time": 9999999999,
        "parameter": "phone"
    })
    assert response.status_code == 200
    data = response.json()
    min_phone_identifiers = []
    for user in data:
        phones = user.get('phones', [])
        if phones:
            identifiers = [phone['identifier'] for phone in phones]
            assert identifiers == sorted(identifiers)  # Verify phones are sorted
            min_identifier = min(identifiers)
            min_phone_identifiers.append(min_identifier)
        else:
            min_phone_identifiers.append(None)
    # Remove None values
    min_phone_identifiers_filtered = [i for i in min_phone_identifiers if i is not None]
    assert min_phone_identifiers_filtered == sorted(min_phone_identifiers_filtered)

def test_get_users_order_by_voicemail(test_client):
    response = test_client.get("/users/", params={
        "start_time": 0,
        "end_time": 9999999999,
        "parameter": "voicemail"
    })
    assert response.status_code == 200
    data = response.json()
    min_voicemail_identifiers = []
    for user in data:
        voicemails = user.get('voicemails', [])
        if voicemails:
            identifiers = [vm['identifier'] for vm in voicemails]
            assert identifiers == sorted(identifiers)  # Verify voicemails are sorted
            min_identifier = min(identifiers)
            min_voicemail_identifiers.append(min_identifier)
        else:
            min_voicemail_identifiers.append(None)
    # Remove None values
    min_voicemail_identifiers_filtered = [i for i in min_voicemail_identifiers if i is not None]
    assert min_voicemail_identifiers_filtered == sorted(min_voicemail_identifiers_filtered)

def test_get_users_order_by_cluster(test_client):
    response = test_client.get("/users/", params={
        "start_time": 0,
        "end_time": 9999999999,
        "parameter": "cluster"
    })
    assert response.status_code == 200
    data = response.json()
    cluster_ids = [user['clusterId'] for user in data]
    cluster_ids_filtered = [cid for cid in cluster_ids if cid is not None]
    assert cluster_ids_filtered == sorted(cluster_ids_filtered)
