import requests
import pandas as pd
from datetime import datetime, timedelta

#api kulcs
API_KEY = '76ff5f36df09e6c0671225f86317afab'

#cache tomb
cache = {}

#koordináták lekérése
def getCoordinates(city):
    if city in cache:
        print("Az adatok a gyorsítótárból vannak!")
        return cache[city]
    else:
        coordinates = fetchCoordinates(city)
        if coordinates is not None:
            cache[city] = coordinates
            return coordinates
        else:
            print("Helytelen városnév.")
            return None
#koordináták lekérése -> API CALL
def fetchCoordinates(city):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and len(response.json()) > 0:
        coordinates = response.json()[0]
        #print("--> sikeresen lefutott az api keres")
        return coordinates
    else:
        return None
#időjárás lekérése
def getWeather(city):
    coordinates = getCoordinates(city)
    if coordinates is not None:
        data = fetchWeather(coordinates['lat'], coordinates['lon'])
        if data is not None:
            return data
        else:
            print("Sikertelen művelet! #getWeather")
            return None
    else:
        return None
#időjárás lekérése -> API CALL
def fetchWeather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, " breakpoint")
        return None
#adatok mentése csv fájlba.
def saveData(data, city):
    filename = f"{city}_weather.csv"
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Sikeres mentés, fájlnév: {filename}")


def showMenu():
    print("1 - Csapadék előrejelzés lekérése")
    print("2 - Adatok mentése CSV-fájlba")
    print("0 - Kilépés")

def main():
    while True:
        showMenu()
        choice = input("Kérem válasszon menüpontot: ")
        
        if choice == '1':
            city = input("Kérem a város nevét: ")
            coordinates = getCoordinates(city)
            if coordinates is not None:
                lat = coordinates['lat']
                lon = coordinates['lon']
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    precipitation = data.get('rain', {}).get('1h', 0)
                    if precipitation != 0:
                        print(f"Az egy órára várható csapadék mennyisége: {precipitation} mm")
                    else:
                        print("Az egy órára várható csapadék mennyisége: Nincs adat")
                else:
                    print("Hiba: Az időjárás adatok lekérése sikertelen.")
            
        elif choice == '2':
            city = input("Kérem a város nevét: ")
            data = getWeather(city)
            if data is not None:
                saveData(data, city)
            
        elif choice == '0':
            break
            
        else:
            print("Hibás választás. Kérem válasszon egy érvényes menüpontot.")

if __name__ == '__main__':
    main()