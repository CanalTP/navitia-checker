import math

def distance_wgs84(point1, point2):
    LatA = float(point1['lat']) * math.pi / 180  # deg2rad
    LngA = float(point1['lon']) * math.pi / 180  # deg2rad
    LatB = float(point2['lat']) * math.pi / 180  # deg2rad
    LngB = float(point2['lon']) * math.pi / 180  # deg2rad
    distance = 6378 * math.acos(math.cos(LatA) * math.cos(LatB) * math.cos(LngB - LngA) + math.sin(LatA) * math.sin(LatB))
    return  round(distance * 1000)
