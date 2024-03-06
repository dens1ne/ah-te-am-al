from requests import put

# Correct request
print(put('http://localhost:5000/api/jobs/2',
          json={'team_leader_id': 2,
                'collaborators': '3,4'}).json())

# Wrong parameter
print(put('http://localhost:5000/api/jobs/2000',
          json={'team_leader_id': 2,
                'collaborators': '3,4'}).json())
print(put('http://localhost:5000/api/jobs/qqq',
          json={'team_leader_id': 2,
                'collaborators': '3,4'}).json())

# Wrong data
print(put('http://localhost:5000/api/jobs/2',
          json={'team_leader_id': 2,
                'collaborators': '3,4',
                'useless parameter': 'abcdefg'}).json())
