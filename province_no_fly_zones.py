import json
import urllib.request
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import unary_union
import numpy as np

# 读取各省边界_百度坐标系.geojson文件
geo_data = gpd.read_file('各省边界_百度坐标系.geojson')


def generate_circle_coordinates(lat, lng, radius, num_points=50):
    angles = np.linspace(0, 360, num_points)
    circle_points = []
    for angle in angles:
        angle_rad = np.radians(angle)
        dlat = radius * np.cos(angle_rad) / 111320  # Convert meters to degrees
        dlng = radius * np.sin(angle_rad) / (111320 * np.cos(np.radians(lat)))
        circle_points.append([lng + dlng, lat + dlat])
    return circle_points

def generate_china_points(step=3):
    china_west = 73  
    china_east = 136  
    china_north = 54  
    china_south = 18  

    for lng in np.arange(china_west, china_east, step):
        for lat in np.arange(china_south, china_north, step):
            yield (lng, lat)

def find_province_by_point(point, geo_data):
    for index, row in geo_data.iterrows():
        province_name = row['name']
        province_boundary = row['geometry']
        if not province_boundary.is_valid:
            province_boundary = province_boundary.buffer(0)
        if province_boundary.contains(point):
            return province_name
    return None

url_template = "https://www.dji.com/cn/api/geo/areas?lng=%s&lat=%s&country=CN&search_radius=250000&drone=spark&level=%s&zones_mode=total"

# 创建一个集合用于存储不重复的area
unique_areas = set()

# 创建一个映射字典，用于存储省份与其对应的区域
province_area_mapping = {}

# 初始化省份映射字典
for index, row in geo_data.iterrows():
    province_name = row['name']
    if province_name:
        province_area_mapping[province_name] = []

for lng, lat in generate_china_points():
    url = url_template % (lng, lat, "1%2C2%2C4%2C7%2C8")

    html = urllib.request.urlopen(url)
    # 获取数据
    data = html.read()

    # 转换成字典数据
    data_json = json.loads(data)

    if data_json['areas']:
        for area in data_json['areas']:
            area_lng = area['lng']
            area_lat = area['lat']
            area_point = Point(area_lng, area_lat)

            # 判断区域的经纬度是否在某个省份的边界内
            area_province = find_province_by_point(area_point, geo_data)

            if area_province:
                # 将area转换为JSON字符串，确保不重复地添加到集合中
                area_json = json.dumps(area, ensure_ascii=False)
                if area_json not in unique_areas:
                    unique_areas.add(area_json)
                    province_area_mapping[area_province].append(area)

def parse_data_to_geojson(data):
    features = []
    for area in data:
        if area['sub_areas'] is not None:
            for sub_area in area['sub_areas']:
                shape = sub_area['shape']
                if shape == 1:  # Polygon
                    coords = sub_area['polygon_points'][0]
                else:  # Circle
                    coords = generate_circle_coordinates(sub_area['lat'], sub_area['lng'], sub_area['radius'])
                polygon = Polygon(coords)
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": area['name'],
                        "type": area['type'],
                        "height": sub_area['height'],
                        "level": sub_area['level']
                    },
                    "geometry": polygon.__geo_interface__
                })

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson_data

# 遍历每个省份的禁飞区列表
for province_name, areas in province_area_mapping.items():
    # 将数据转换为 Polygon 对象列表
    geojson_data = parse_data_to_geojson(areas)
    # 保存 GeoJSON 数据到文件
    with open(f'{province_name}禁飞区_百度坐标系.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)