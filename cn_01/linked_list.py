import math


class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, element):
        if self.head:
            pointer = self.head
            while pointer.next:
                pointer = pointer.next
            pointer.next = Node(element)
        else:
            self.head = Node(element)
        self._size = self._size + 1

    def __len__(self):
        return self._size

    def getTurbine(self):
        return self.head

    def __getitem__(self, index):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError('out of range')
        if pointer:
            return pointer.data

        raise IndexError('out of range')

    def __setitem__(self, index, element):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError('out of range')
        if pointer:
            pointer.data = element
        else:
            raise IndexError('out of range')

    def index(self, element):
        pointer = self.head
        i = 0
        while pointer:
            if pointer.data == element:
                return i
            pointer = pointer.next
            i = i + 1
        raise ValueError(f'{element} is not in the list')


class Links:

    def __init__(self, link=0):
        self.__custos = {1: 50.69836784, 2: 71.62465884, 3: 99.20682306, 4: 126.3675203, 5: 154.8583709, 6: 183.369654,
                         7: 217.0648069, 8: 255.9438294, 9: 300.0067216, 10: 349.2534835}
        self.link = link
        self.cost = self.verify(self.link)

    def multiplication(self):
        return self.cost * self.link

    def verify(self, num_links):
        return 0 if num_links == 0 else self.verify_number_links(num_links)

    def verify_number_links(self, num_links):
        return 0 if num_links > 10 else self.__custos[num_links]

    def distance_meters_between_points(self, station, elem1, elem2):
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

    def closer(self, station, elem1):
        list = []
        for i in range(len(station)):
            if elem1 != i:
                dist = self.distance_meters_between_points(station, elem1, i)
                list.append(dist)
        minpos = list.index(min(list))
        if minpos >= elem1:
            return minpos + 1
        if minpos < elem1:
            return minpos
