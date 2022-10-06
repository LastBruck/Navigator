import requests, json, folium, polyline
from geopy.distance import distance


location_from =  input("Введите первый адрес:")
location_to =  input("Введите второй адрес:")

addresses = [location_from, location_to]

def get_coordinates(addr=addresses):
    BASE_URL = 'https://nominatim.OpenStreetMap.org/search?format=json'
    locations = []
    for adres in addr:
        response = requests.get(f"{BASE_URL}&q={adres}")
        data = response.json()
        latitude = data[0].get('lat')
        longitude = data[0].get('lon')
        locations.append([longitude, latitude])
    return locations

def rout_coor():
    locations = get_coordinates()
    coor = ";".join(map(",".join, locations))
    route_url=f'http://router.project-osrm.org/route/v1/driving/{coor}?alternatives=true&geometries=polyline'
    r=requests.get(route_url)
    res=r.json()
    route = polyline.decode(res["routes"][0]["geometry"])
    return route

def drawing_the_route():
    locations = get_coordinates()
    route = rout_coor()
    location1 = locations[0][::-1]
    location2 = locations[-1][::-1]

    m = folium.Map(location=location1, width=2000, height=1100, zoom_start=15)
    folium.PolyLine(route, weight=8,color='blue',opacity=6).add_to(m)
    folium.Marker(location1, popup='Точка А', tooltip='Точка А').add_to(m)
    folium.Marker(location2, popup='Точка Б', tooltip='Точка Б').add_to(m)
    km = distance(location1, location2).kilometers
    
    m.save('MAP.html')

    print(f'{km:.2f} км')

drawing_the_route()