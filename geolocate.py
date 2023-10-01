import sys
import json
import requests
import time
import math
from tqdm import tqdm
import re
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__': 
    with open(f'./{sys.argv[1]}', 'r') as f:
        contents = f.read()
        lines = contents.split("\n")
        results = []
        for line in lines:
            regex = r''+str(sys.argv[2])
            if len(sys.argv) <= 2 or re.search(regex,string=line) is not None:
                if len(line.split(" - - ")) != 0:
                    ip = line.split(" - - ")[0]
                    if len(ip) > 5:   # make sure ip is valid    
                        results.append({
                            "ip_address": ip, 
                            "count": 1,
                            "date": (line.split(' - - ')[1].split(" ")[0]).replace("[","")
                        })
        print(f"TOTAL REQUESTS SENT: {len(results)}")
        ip_occurrences = []
        for ip in tqdm(results):
            a = list(filter(lambda x: x != None and x["ip_address"] == ip["ip_address"], results))
            b = list(filter(lambda x: x != None and x["ip_address"] == ip["ip_address"], ip_occurrences))
            if len(a) == 0:
                ip_occurrences.append(ip)
            elif len(b) == 0:
                sum_count = 0
                for ip in a:
                    sum_count += ip['count']
                ip_occurrences.append({
                    "ip_address":ip['ip_address'],
                    "count": sum_count,
                    "last_date": ip['date']
                })
        
        ip_occurrences.sort(key=lambda x:x != None and x.get("count"),reverse=True)
        print(f"TOTAL UNIQUE IPS: {len(ip_occurrences)}")
        print(f"ESTIMATED {math.floor(len(ip_occurrences)/45)}min TOTAL RUNTIME")
        index = 0
        start_time = time.time()

        for ip_entry in tqdm(ip_occurrences):
            index += 1
            request_worked = False
            while not request_worked:
                try:
                    time.sleep(1.5)
                    res = requests.get(f'http://ip-api.com/json/{ip_entry["ip_address"]}?fields=66842623&lang=en')
                    response = json.loads(res.text)
                    ip_entry.update(response)
                    request_worked = True
                    runtime_min = math.floor((time.time()-start_time)/60)
                except:
                    print("FAILED TO CONNECT TO IP GEOLOCATION API - RETRYING")

        ip_occurrences_geojson = {
        "type": "FeatureCollection",
        "crs": {
        "type": "name",
        "properties": {
        "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        },
        },
         "features": []
        }
        final_f = []
        print(len(ip_occurrences))
        for d in ip_occurrences:
            final_f = []
            obj = {
                "type":"Feature",
                "properties": {
                    "id":d["ip_address"],
                    "mag":d["count"],
                },
                'geometry': {
                    'type':"Point",
                    'coordinates': [
                        d['lon'],d["lat"]
                    ]
                }
            }
            final_f.append(obj)
        print(len(final_f))
        ip_occurrences_geojson["features"] = final_f

        MAP_HTML = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>NGINX Log Heatmap</title>
    <meta
      name="viewport"
      content="initial-scale=1,maximum-scale=1,user-scalable=no"
    />
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css"
      rel="stylesheet"
    />
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.js"></script>
    <style>
      body {
        margin: 0;
        padding: 0;
      }
      #map {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      const data_geojson = <PLACE_HOLDER_1>
      mapboxgl.accessToken = "<PLACE_HOLDER_2>";
      const map = new mapboxgl.Map({
        container: "map",
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: "mapbox://styles/mapbox/dark-v11",
        center: [-120, 50],
        zoom: 2,
      });

      map.on("load", () => {
        map.addSource("user_connections", {
          type: "geojson",
          data: data_geojson,
        });
        map.addLayer(
          {
            id: "user_connections-heat",
            type: "heatmap",
            source: "user_connections",
            maxzoom: 9,
            paint: {
              // Increase the heatmap weight based on frequency and property magnitude
              "heatmap-weight": [
                "interpolate",
                ["linear"],
                ["get", "mag"],
                0,
                0,
                6,
                1,
              ],
              // Increase the heatmap color weight weight by zoom level
              // heatmap-intensity is a multiplier on top of heatmap-weight
              "heatmap-intensity": [
                "interpolate",
                ["linear"],
                ["zoom"],
                0,
                1,
                9,
                3,
              ],
              // Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
              // Begin color ramp at 0-stop with a 0-transparancy color
              // to create a blur-like effect.
              "heatmap-color": [
                "interpolate",
                ["linear"],
                ["heatmap-density"],
                0,
                "rgba(33,102,172,0)",
                0.2,
                "rgb(103,169,207)",
                0.4,
                "rgb(209,229,240)",
                0.6,
                "rgb(253,219,199)",
                0.8,
                "rgb(239,138,98)",
                1,
                "rgb(178,24,43)",
              ],
              // Adjust the heatmap radius by zoom level
              "heatmap-radius": [
                "interpolate",
                ["linear"],
                ["zoom"],
                0,
                2,
                9,
                20,
              ],
              // Transition from heatmap to circle layer by zoom level
              "heatmap-opacity": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                1,
                9,
                0,
              ],
            },
          },
          "waterway-label"
        );

        map.addLayer(
          {
            id: "user_connections-point",
            type: "circle",
            source: "user_connections",
            minzoom: 7,
            paint: {
              // Size circle radius by earthquake magnitude and zoom level
              "circle-radius": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                ["interpolate", ["linear"], ["get", "mag"], 1, 1, 6, 4],
                16,
                ["interpolate", ["linear"], ["get", "mag"], 1, 5, 6, 50],
              ],
              // Color circle by earthquake magnitude
              "circle-color": [
                "interpolate",
                ["linear"],
                ["get", "mag"],
                1,
                "rgba(33,102,172,0)",
                2,
                "rgb(103,169,207)",
                3,
                "rgb(209,229,240)",
                4,
                "rgb(253,219,199)",
                5,
                "rgb(239,138,98)",
                6,
                "rgb(178,24,43)",
              ],
              "circle-stroke-color": "white",
              "circle-stroke-width": 1,
              // Transition from heatmap to circle layer by zoom level
              "circle-opacity": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                0,
                8,
                1,
              ],
            },
          },
          "waterway-label"
        );
      });
    </script>
  </body>
</html>
"""
        MAP_HTML = MAP_HTML.replace("<PLACE_HOLDER_1>",json.dumps(ip_occurrences_geojson,separators=(',', ':')))
        MAP_HTML = MAP_HTML.replace("<PLACE_HOLDER_2>",os.getenv("MAPBOX_ACCESS_TOKEN"))
        with open(f"./map.html", 'w') as f2:
            f2.write(MAP_HTML)
            