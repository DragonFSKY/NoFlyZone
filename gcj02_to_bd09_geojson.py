import geopandas as gpd
from coord_convert.transform import wgs2gcj, gcj2bd
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, shape


def transform_coord(coord, transformer):
    return tuple(transformer(*coord))


def transform_geometry(geom, transformer):
    if geom.type == 'Point':
        return Point(transform_coord(geom.coords[0], transformer))
    elif geom.type == 'LineString':
        return LineString([transform_coord(coord, transformer) for coord in geom.coords])
    elif geom.type == 'Polygon':
        return Polygon([transform_coord(coord, transformer) for coord in geom.exterior.coords])
    elif geom.type == 'MultiPolygon':
        return MultiPolygon([transform_geometry(polygon, transformer) for polygon in geom.geoms])
    else:
        raise ValueError(f'Unsupported geometry type: {geom.type}')


def gcj_to_bd(geometry):
    return transform_geometry(geometry, gcj2bd)


input_file = '各省边界_高德坐标系.geojson'
output_file = '各省边界_百度坐标系.geojson'

gdf = gpd.read_file(input_file)
gdf.crs = None
gdf['geometry'] = gdf['geometry'].apply(gcj_to_bd)
gdf.to_file(output_file, driver='GeoJSON')
