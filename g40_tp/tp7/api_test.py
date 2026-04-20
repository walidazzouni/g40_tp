import requests

url = "https://api.github.com"

response = requests.get(url)

data = response.json()

print("Statut :", response.status_code)
print("URL API :", data["current_user_url"])
print("Repos URL :", data["repository_url"])