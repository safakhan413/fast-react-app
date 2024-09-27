# migrate.py

import json
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base  # Import Base from database.py
from models import Cluster, User, Phone, Voicemail, UserPhones, UserVoicemails
from sqlalchemy.exc import IntegrityError

def load_json(file_path):
    """
    Loads JSON data from the specified file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def migrate_data(data, session: Session):
    """
    Migrates data from JSON to MySQL database.
    """
    # Step 1: Populate Clusters
    cluster_ids = set(record['clusterId'] for record in data)

    existing_clusters = session.query(Cluster).filter(Cluster.clusterId.in_(cluster_ids)).all()
    existing_cluster_ids = {cluster.clusterId for cluster in existing_clusters}

    new_clusters = [Cluster(clusterId=cid) for cid in cluster_ids if cid not in existing_cluster_ids]
    session.add_all(new_clusters)
    session.commit()
    print(f"Inserted {len(new_clusters)} new clusters.")

    # Step 2: Populate Phones and Voicemails
    phone_identifiers = set()
    voicemail_identifiers = set()
    for record in data:
        devices = record.get('devices', {})
        phone_identifiers.update(devices.get('phone', []))
        voicemail_identifiers.update(devices.get('voicemail', []))

    # Insert Phones
    existing_phones = session.query(Phone).filter(Phone.identifier.in_(phone_identifiers)).all()
    existing_phone_ids = {phone.identifier: phone.phoneId for phone in existing_phones}
    new_phones = [Phone(identifier=pid) for pid in phone_identifiers if pid not in existing_phone_ids]
    session.add_all(new_phones)
    session.commit()
    print(f"Inserted {len(new_phones)} new phones.")

    # Insert Voicemails
    existing_voicemails = session.query(Voicemail).filter(Voicemail.identifier.in_(voicemail_identifiers)).all()
    existing_vm_ids = {vm.identifier: vm.vmId for vm in existing_voicemails}
    new_voicemails = [Voicemail(identifier=vid) for vid in voicemail_identifiers if vid not in existing_vm_ids]
    session.add_all(new_voicemails)
    session.commit()
    print(f"Inserted {len(new_voicemails)} new voicemails.")

    # Refresh phone and voicemail mappings
    all_phones = session.query(Phone).filter(Phone.identifier.in_(phone_identifiers)).all()
    phone_mapping = {phone.identifier: phone.phoneId for phone in all_phones}

    all_voicemails = session.query(Voicemail).filter(Voicemail.identifier.in_(voicemail_identifiers)).all()
    voicemail_mapping = {vm.identifier: vm.vmId for vm in all_voicemails}

    # Step 3: Populate Users and Relationships
    users_added = 0
    user_phone_relations = []
    user_voicemail_relations = []

    for record in data:
        user_id = record['_id']
        userId = record['userId']
        originationTime = record['originationTime']
        clusterId = record['clusterId']

        # Check if user already exists
        existing_user = session.query(User).filter(User.id == user_id).first()
        if existing_user:
            print(f"User with id {user_id} already exists. Skipping.")
            continue

        # Create User
        user = User(
            id=user_id,
            userId=userId,
            originationTime=originationTime,
            clusterId=clusterId
        )
        session.add(user)
        users_added += 1
        session.flush()  # Flush to assign relationships

        # Associate Phones
        phones = record.get('devices', {}).get('phone', [])
        for phone in phones:
            phoneId = phone_mapping.get(phone)
            if phoneId:
                relation = UserPhones(userId=user_id, phoneId=phoneId)
                user_phone_relations.append(relation)

        # Associate Voicemails
        voicemails = record.get('devices', {}).get('voicemail', [])
        for vm in voicemails:
            vmId = voicemail_mapping.get(vm)
            if vmId:
                relation = UserVoicemails(userId=user_id, vmId=vmId)
                user_voicemail_relations.append(relation)

    # Bulk Insert Relationships
    if user_phone_relations:
        session.bulk_save_objects(user_phone_relations)
        print(f"Associated {len(user_phone_relations)} phone relationships.")

    if user_voicemail_relations:
        session.bulk_save_objects(user_voicemail_relations)
        print(f"Associated {len(user_voicemail_relations)} voicemail relationships.")

    # Commit all changes
    try:
        session.commit()
        print(f"Inserted {users_added} new users.")
    except IntegrityError as e:
        session.rollback()
        print(f"IntegrityError occurred: {e.orig}")
    except Exception as e:
        session.rollback()
        print(f"An unexpected error occurred: {str(e)}")

def main():
    """
    Main function to perform migration.
    """
    # Create all tables (if not already created)
    from models import Cluster, User, Phone, Voicemail, UserPhones, UserVoicemails
    Base.metadata.create_all(bind=engine)

    # Create a new database session
    session = SessionLocal()

    try:
        import os
        json_path = os.path.join(os.path.dirname(__file__), '..', 'documents.json')
        json_path = os.path.abspath(json_path)
        data = load_json(json_path)


        # data = load_json('../documents.json')
        migrate_data(data, session)
        print("Data migration completed successfully.")
    except Exception as e:
        session.rollback()
        print("An error occurred during migration:", e)
    finally:
        session.close()

if __name__ == '__main__':
    main()
