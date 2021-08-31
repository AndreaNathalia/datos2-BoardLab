import requests
import json

#API auth
clientID = "QxqUbiHLBkFZQGBGh5c6cr8a4s_Mt3z7w9apnT1tFAo"

# Buscar fotos - API 
url = "https://api.unsplash.com/search/photos/"

def searchPhotos(query):
    data = requests.get(url, params={"client_id": clientID,
                                     "query": query, 
                                     "per_page":30,
                                     "page" : 1}).json()
    tags = []
    for i in data["results"]:
        tags.append(i["urls"]["full"])
    return tags