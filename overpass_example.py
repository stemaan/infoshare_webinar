import json
import overpy
import folium

with open('./route.json', encoding='utf-8') as geojson:
    loaded_data = json.load(geojson)
    geometry = loaded_data.get('geometry')

api = overpy.Overpass()
radius = 1000
tag = 'fuel'
query_template = '(node["amenity"="{tag}"](around:{radius},{lat},{lon}););out body;'

# get only latitude and longitude, no need for elevation
geometry = [(lat, long) for lat, long, alt in geometry]
middle_idx = len(geometry) // 2
middle_point = geometry[middle_idx]

my_map = folium.Map(location=middle_point, zoom_start=10)

folium.PolyLine(geometry).add_to(my_map)

for latitude, longitude in geometry[::250]:
    result = api.query(
        query_template.format(
            tag=tag, radius=radius, lat=latitude, lon=longitude
        )
    )

    for node in result.nodes:
        folium.map.Marker([node.lat, node.lon],
                          popup=node.tags.get('brand', tag)).add_to(my_map)

my_map.save('mapa3.html')
