from cn_01.substation import Substation
from cn_01.turbine import Turbine


class Station:

    def __init__(self):
        self.__turbines = Turbine()
        self.__substation = Substation()

    def station_components(self):
        return self.__substation.df.append(self.__turbines.df)

    def __len__(self):
        return len(self.station_components())

    @property
    def turbines(self):
        return self.__turbines

    @property
    def substation(self):
        return self.__substation
