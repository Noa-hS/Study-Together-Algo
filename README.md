# Study Group Generation Algorithm

This Python algorithm reads a JSON file containing student data and generates an array of study groups for each subject the students are taking. The algorithm prioritizes creating groups of 5 users but allows for exceptions when the remainder of users cannot be grouped efficiently into 5s. The logic ensures that all users are assigned to a group, even if the group size exceeds the preferred limit of 5.

## Input Data

The JSON file should contain the following data for each student:

- `uid`: A string of integers representing the student/user ID.
- `opt`: A boolean value (1 or 0) indicating whether the user has opted in for the study groups.
- `subjects`: A list of 4 subjects taken by each student.

## Algorithm Overview

1. **Read Subjects for Opted-In Users**: The algorithm only processes users who have opted in. It generates a dictionary of all subjects the opted-in students are taking. If a student is taking a subject, their ID is appended to a dictionary.

2. **Calculate Group Size for Each Subject**: For each subject, the algorithm calculates the number of possible full 5-user groups and the number of remaining users. 

3. **Generate Study Groups**: Using the group calculations and the user IDs in each subject, the algorithm generates study groups. The creation date (in the format dd/mm/yyyy) is included in the output.

## Output Format

The output format is as follows:

```json
{
  "creation date": {
    "subject 1": {
      "group 1": ["user1", "user2", "user3"],
      "group 2": ["user1", "user2"]
    },
    "subject 2": {
      "group 1": ["user1", "user2", "user3", "user4"],
      "group 2": ["user1", "user2", "user3"]
    }
  }
}
```

The creation date is in the format dd/mm/yyyy. Each group is an array of user IDs. The users allocated into the groups are random, so every time the algorithm is run, there should be different user IDs in the study groups. 

## Note

This algorithm is designed to ensure that all users are assigned to a group, even if the group size exceeds the preferred limit of 5. The users allocated into the groups are random, so every time the algorithm is run, there should be different user IDs in the study groups. 

This algorithm is unoptimized and is only a prototype. Any group size other than 5 should not be used yet. 
