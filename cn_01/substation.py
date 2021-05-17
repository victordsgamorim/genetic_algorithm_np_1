from cn_01.station_data_frame import StationDataFrame


class Substation(StationDataFrame):

    def type(self):
        return 'substation'

    def file_name(self):
        return 'altodacoutada-ss'
