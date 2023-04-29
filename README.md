# NoFlyZone

## 在大佬的基础上添加
各省边界_高德坐标系.geojson 下载自高德开放平台
gcj02_to_bd09_geojson.py 将 各省边界_高德坐标系.geojson 转换为 各省边界_百度坐标系.geojson
province_no_fly_zones.py 根据 各省边界_百度坐标系.geojson 获得 各省禁飞区_百度坐标系.geojson 如果需要获取临时禁飞区、警戒区 需根据大疆geo平台接口修改传参level
bd09_to_WG84.py  将当前目录下 xxx_百度坐标系.geojson 转换为 xxx_84坐标系.geojson
==================================================
下载大疆无人机禁飞区，生成shp文件


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

