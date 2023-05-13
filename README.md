# NoFlyZone

## 在大佬基础上添加以下文件：
- `各省边界_高德坐标系.geojson`：从高德开放平台下载的各省边界文件(推荐这里下载 https://datav.aliyun.com/portal/school/atlas/area_selector)，坐标系为高德坐标系。
- `gcj02_to_bd09_geojson.py`：将高德坐标系的各省边界文件转换为百度坐标系的文件。
- `province_no_fly_zones.py`：根据百度坐标系的各省边界文件获得各省禁飞区。如果需要获取临时禁飞区、警戒区，需要根据大疆geo平台接口修改传参level。
- `city_no_fly_zones.py`：根据百度坐标系的各省边界文件获得各市区禁飞区。如果需要获取临时禁飞区、警戒区，需要根据大疆geo平台接口修改传参level。
- `bd09_to_wgs84.py`：将当前目录下 _百度坐标系结尾的geojson 转换成 wgs84坐标系对应的文件。


## 首先运行下载禁飞区脚本
```python
down.py
```
生成data.txt,数据文件

## 然后运行
```python
parse.py
```
生成polygon.shp

