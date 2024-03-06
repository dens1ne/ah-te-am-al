from requests import delete

# Correct request
print(delete('http://localhost:5000/api/jobs/3').json())

# Wrong id
print(delete('http://localhost:5000/api/jobs/5000').json())

# Wrong type of parameter
print(delete('http://localhost:5000/api/jobs/wrongtype').json())
