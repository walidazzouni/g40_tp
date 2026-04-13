import requests

ville = input("Ville : ")

api_key = "66642f9689244d5d0e90c3f72d6af57f"

url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric"

response = requests.get(url)

data = response.json()

if response.status_code == 200:
    nom = data["name"]
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]

    print(f"\nRésultat pour {nom}")
    print(f"Température : {temperature} °C")
    print(f"Météo : {description}")

else:
    print("\nErreur lors de la requête API")
    print("Message :", data.get("message", "inconnu"))