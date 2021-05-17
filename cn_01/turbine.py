from cn_01.station_data_frame import StationDataFrame

class Turbine(StationDataFrame):

    def type(self):
        return 'turbine'

    def file_name(self):
        return 'altodacoutada'
