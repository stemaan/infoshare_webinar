import json
import overpy
import folium

with open('./route.json') as geojson:
    loaded_data = json.load(geojson)
    coordinates = loaded_data.get('geometry')

coordinates = [coordinate[:2] for coordinate in coordinates]
middle = coordinates[len(coordinates) // 2]
my_map = folium.Map(location=(middle), zoom_start=10)

folium.PolyLine(coordinates).add_to(my_map)

api = overpy.Overpass()
radius = 1000
tag = 'fuel'
latitude = 49.7173
longitude = 18.8007
query_fmt = '(node["amenity"="{tag}"](around:{radius},{lat},{lon}););out body;'

for coordinate in coordinates[::250]:
    latitude, longitude = coordinate
    result = api.query(
        query_fmt.format(
            tag=tag, radius=radius, lat=latitude, lon=longitude
        )
    )

    for node in result.nodes:
        folium.map.Marker([node.lat, node.lon],
                          popup=node.tags.get('brand', 'Stacja paliw')).add_to(
            my_map)

my_map.save('overpass2.html')
