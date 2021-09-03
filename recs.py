# Recomendaciones 
import requests

#API auth
clientID = "QxqUbiHLBkFZQGBGh5c6cr8a4s_Mt3z7w9apnT1tFAo"

url = "https://api.unsplash.com/photos/random"

def homeRecs():

    recs = requests.get(url, params={"client_id": clientID, "count": 30}).json()

    linkRecs = []
    for i in recs:
        print(i["urls"]["full"])
        print("")
        linkRecs.append(i["urls"]["full"])
    
    # linkRecs.append() # --------- SEARCH FOR MORE

    return linkRecs

