from requests import delete, get, post

# Correct request
print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())

response = post('http://localhost:5000/api/v2/users',
           json={"surname": "surname",
                 "name": "name",
                 "age": 14,
                 "position": "position",
                 "speciality": "speciality",
                 "email": "email",
                 "password": "password",
                 "address": "address",
                 "city_from": "city"})
print(response.json())

print(delete(f'http://localhost:5000/api/v2/users/{response.json().get("user_id")}').json())

# Wrong input
print(get('http://localhost:5000/api/v2/users/100000').json())
print(delete('http://localhost:5000/api/v2/users/-1').json())
print(post('http://localhost:5000/api/v2', json={}))
