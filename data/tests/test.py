from requests import delete, get

# Correct request
print(get(url='http://localhost:5000/api/jobs').json())
print(delete('http://localhost:5000/api/jobs/4').json())
print(get(url='http://localhost:5000/api/jobs').json())

# Wrong request
print(delete('http://localhost:5000/api/jobs/9000').json())

# Wrong type of parameter
print(delete('http://localhost:5000/api/jobs/five').json())
