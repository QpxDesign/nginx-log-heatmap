![example heatmap](https://github.com/qpxdesign/nginx-log-heatmap/blob/main/images/example.png?raw=true)

### NGINX Log Heatmap Generator

This is a python script that takes in NGINX logs and geolocates IPs, outputting them to JSON and counting unique ip occurrences. It can also output as GeoJSON, to a pre-configured HTML/Mapbox-based Heatmap of User Traffic.

#### Running It

1. install the requirements : `pip install -r requirements.txt`
2. Get a [Mapbox Access Token](https://docs.mapbox.com/help/getting-started/access-tokens/), and place it in the .env file, where it says 'MAPBOX_ACCESS_TOKEN='.
3. Run the following command to generate the JSON/GeoJSON (it may take a while based on how big your log file is).
   `python3 geolocate.py <log_path> <regex_to_match_log_lines>`

Once that finishes, you should be able to open the map.html in your browser by either dragging it or going to its path. There, you should be able to see your heatmap!

#### Contributing

Feel free to make contributions to this! Create a pull request with bug fixes or new features, and I'll review and add them!

#### License (MIT)

MIT License

Copyright (c) [2023] [Quinn Patwardhan]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
