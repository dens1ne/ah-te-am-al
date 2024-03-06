from requests import get, post

# Empty request
print(post('http://localhost:5000/api/jobs', json={}).json())

# Bad request
print(post('http://localhost:5000/api/jobs', json={'team_leader_id': 'some id'}).json())

# Correct request
print(post('http://localhost:5000/api/jobs',
           json={'team_leader_id': 1,
                 'job': 'Recovery of modules 5 and 6',
                 'work_size': 30,
                 'start_date': '2024-01-01 00:00:00.000000',
                 'end_date': '2024-02-01 00:00:00.000000',
                 'is_finished': True,
                 'collaborators': '2,3,4'}).json())
