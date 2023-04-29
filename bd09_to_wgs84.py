import os
import json
from coord_convert.transform import bd2wgs

def convert_bd_to_wgs84(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        data = json.load(f)
        
    for feature in data['features']:
        if feature['geometry']['type'] == 'Point':
            lng, lat = feature['geometry']['coordinates']
            lng84, lat84 = bd2wgs(lng, lat)
            feature['geometry']['coordinates'] = [lng84, lat84]
        elif feature['geometry']['type'] == 'LineString' or feature['geometry']['type'] == 'Polygon':
            for coordinates in feature['geometry']['coordinates']:
                for i, coordinate in enumerate(coordinates):
                    lng, lat = coordinate
                    lng84, lat84 = bd2wgs(lng, lat)
                    coordinates[i] = [lng84, lat84]

    with open(output_filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    input_files = [f for f in os.listdir() if f.endswith('_百度坐标系.geojson')]

    for input_file in input_files:
        output_file = input_file.replace('_百度坐标系.geojson', '_84坐标系.geojson')
        convert_bd_to_wgs84(input_file, output_file)
        print(f'已将 {input_file} 转换为 {output_file}')

if __name__ == "__main__":
    main()
