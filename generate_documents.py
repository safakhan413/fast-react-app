import random
import time
import json
from collections import defaultdict

# ------------------------------
# 1. Define Sample Data
# ------------------------------

# Sample cluster IDs representing different servers or domains
cluster_ids = ['domainserver1', 'domainserver2', 'domainserver3', 'domainserver4']

# Generate 100 unique user IDs (as strings of 9 digits)
user_ids = [str(random.randint(100000000, 999999999)) for _ in range(100)]  # 100 users

# Prefixes for phone and voicemail identifiers to add variety
phone_prefixes = ['SEP', 'HP', 'SAMS', 'LG', 'APP']
voicemail_prefixes = ['VM', 'MSG', 'MAIL', 'VOICE']

# ------------------------------
# 2. Define Helper Functions
# ------------------------------

def generate_unique_id(start=10000):
    """
    Generates a unique integer identifier starting from a specified number.
    
    Args:
        start (int): The starting point for IDs.
    
    Returns:
        int: A unique integer ID.
    """
    # Use a generator to create unique IDs
    generate_unique_id.current += 1
    return generate_unique_id.current

# Initialize the generator's current ID
generate_unique_id.current = 10000  # Starting from 10000 as an example

def generate_origination_time():
    """
    Generates a random origination time within the last year.
    
    Returns:
        int: A Unix timestamp representing the origination time.
    """
    current_time = int(time.time())  # Current Unix timestamp
    one_year_seconds = 365 * 24 * 60 * 60  # Number of seconds in one year
    # Random timestamp within the last year
    return random.randint(current_time - one_year_seconds, current_time)

# ------------------------------
# 3. Create a Shared Pool of Devices
# ------------------------------

# Define the total number of unique devices
num_phones = 200       # Total unique phones
num_voicemails = 200   # Total unique voicemails

# Generate a pool of unique phone identifiers (3-letter prefix + 12 digits)
phones_pool = [f"{random.choice(phone_prefixes)}{random.randint(100000000000, 999999999999)}" for _ in range(num_phones)]

# Generate a pool of unique voicemail identifiers (prefix + 6 digits)
voicemails_pool = [f"{random.choice(voicemail_prefixes)}{random.randint(100000, 999999)}" for _ in range(num_voicemails)]

# ------------------------------
# 4. Assign Devices to Users
# ------------------------------

# Initialize separate mappings for phones and voicemails
device_users_phones = defaultdict(set)
device_users_voicemails = defaultdict(set)

# Initialize mapping between users and devices
user_devices = defaultdict(lambda: {'phones': set(), 'voicemails': set()})

# Assign devices to users
for user in user_ids:
    # Determine the number of phones and voicemails for each user
    num_user_phones = random.randint(1, 5)       # Each user has between 1 to 5 phones
    num_user_voicemails = random.randint(1, 3)   # Each user has between 1 to 3 voicemails

    # Randomly assign phones to the user, allowing for shared devices
    assigned_phones = random.sample(phones_pool, num_user_phones)
    user_devices[user]['phones'].update(assigned_phones)
    for phone in assigned_phones:
        device_users_phones[phone].add(user)

    # Randomly assign voicemails to the user, allowing for shared devices
    assigned_voicemails = random.sample(voicemails_pool, num_user_voicemails)
    user_devices[user]['voicemails'].update(assigned_voicemails)
    for vm in assigned_voicemails:
        device_users_voicemails[vm].add(user)

# ------------------------------
# 5. Generate JSON Documents
# ------------------------------

# List to hold all JSON documents
json_documents = []

# Iterate through each user to create their JSON document
for user in user_ids:
    document = {
        "_id": generate_unique_id(),                     # Unique integer ID
        "originationTime": generate_origination_time(),  # Random origination time
        "clusterId": random.choice(cluster_ids),         # Randomly assign a cluster
        "userId": user,                                  # User ID
        "devices": {
            "phone": list(user_devices[user]['phones']),        # List of assigned phones
            "voicemail": list(user_devices[user]['voicemails']) # List of assigned voicemails
        }
    }
    json_documents.append(document)  # Add the document to the list

# ------------------------------
# 6. Save to a JSON File
# ------------------------------

# Specify the output file name
output_file = 'documents.json'

# Open the file in write mode and dump the JSON documents with indentation for readability
with open(output_file, 'w') as f:
    json.dump(json_documents, f, indent=4)

print(f"Successfully generated {len(json_documents)} JSON documents and saved to '{output_file}'.")
