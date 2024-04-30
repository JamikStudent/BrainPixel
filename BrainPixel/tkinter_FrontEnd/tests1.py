import requests

url = ('http://localhost:8000/users/1/') # URL for requests
response = requests.post(url) # GET / POST requests
print(response.json()) # debug