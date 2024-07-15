import json 
import random
from datetime import datetime

# Constants
GROUP_SIZE = 4
MAX_RECOMMENDED_USERS = 10

# Simulating Firestore database
db = {}

def generate_study_groups(profile_collection):
    # Check if admin settings exist, if not create them
    if not check_admin_settings_exist():
        create_admin_settings()

    # Extract user data from profiles
    users = [
        {
            'uid': doc.id,
            'summary': doc.data['summary'],
            'firstName': doc.data['firstName'],
            'lastName': doc.data['lastName']
        }
        for doc in profile_collection
    ]

    # Randomize user order
    random.shuffle(users)

    # Divide users into groups
    groups = [users[i:i+GROUP_SIZE] for i in range(0, len(users), GROUP_SIZE)]

    # Redistribute the smallest group if necessary
    if len(groups[-1]) < GROUP_SIZE and len(groups[-1]) <= len(groups) - 1:
        for i, user in enumerate(groups[-1]):
            groups[i].append(user)
        groups.pop()

    # Create groups in the database
    collection_count = len(db.get('groups', []))
    for group in groups:
        collection_count += 1
        group_id = f"group_{collection_count}"
        
        # Add members to group
        uids = []
        for profile in group:
            db.setdefault(f"groups/{group_id}/members", {})[profile['uid']] = profile
            uids.append(profile['uid'])

        # Set group details
        db.setdefault('groups', {})[group_id] = {
            'id': group_id,
            'groupNumber': collection_count,
            'memberUserIds': uids,
            'attendingUserIds': [],
            'createdAt': datetime.now()
        }

def generate_recommendations(profile_collection, profile_ref):
    # Get already matched users
    matched_uids = set(db.get(f"profiles/{profile_ref}/match.complete", {}).keys())

    # Filter and prepare potential recommendations
    potential_recommendations = [
        {
            'uid': doc.id,
            'summary': doc.data['summary'],
            'bio': doc.data['bio'],
            'firstName': doc.data['firstName'],
            'lastName': doc.data['lastName'],
            'graduationYear': doc.data['graduationYear'],
            'degree': doc.data['degree'],
            'major': doc.data['major'],
            'interests': doc.data['interests'],
            'subjects': doc.data['subjects']
        }
        for doc in profile_collection
        if doc.id not in matched_uids and doc.id != profile_ref
    ]

    # Randomly select recommendations
    recommended_users = random.sample(potential_recommendations, min(MAX_RECOMMENDED_USERS, len(potential_recommendations)))

    # Update recommendations in the database
    db[f"profiles/{profile_ref}/recommendations"] = {user['uid']: user for user in recommended_users}


# Executing function
def main():
    profile_collection = db.get('profiles', {})
    generate_study_groups(profile_collection)

    for profile_ref in profile_collection:
        generate_recommendations(profile_collection, profile_ref)

if __name__ == "__main__":
    main()
