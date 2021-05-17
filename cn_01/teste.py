import math

from cn_01.linked_list import LinkedList
import random

from cn_01.station import Station

station = Station()


def distance_meters_between_points(station, elem1, elem2):
    station_df = station.station_components()

    lon1 = station_df.iloc[elem1]['lon']
    lat1 = station_df.iloc[elem1]['lat']

    lon2 = station_df.iloc[elem2]['lon']
    lat2 = station_df.iloc[elem2]['lat']

    R = 6378.137  # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters


def closer(station, elem1):
    list = []
    for i in range(len(station)):
        if elem1 != i:
            dist = distance_meters_between_points(station, elem1, i)
            list.append(dist)
    minpos = list.index(min(list))
    if minpos >= elem1:
        return minpos + 1
    if minpos < elem1:
        return minpos


def random_chromo(chrome, station):
    linkedList = LinkedList()
    for i in range(0, chrome):  # 'i' will have values from 0 to 49 (chrome length 50)
        rand = None
        if random.random() < 0.6:
            rand = closer(station, i + 2)
        else:
            rand = random.randint(0, chrome + 1)
        linkedList.append(rand)  # add numbers between 0 and 51 (0, 1 substation/ 2-51 turbines)
    return linkedList


l = random_chromo(50, station)

for i in range(50):
    print(l[i])
