from abc import ABC, abstractmethod

import pandas as pd


class StationDataFrame(ABC):

    def __init__(self):
        self.__TYPE = 'type'

        self.__FILE_PATH = f'{self.file_name()}.txt'
        self.__df = pd.read_table(self.__FILE_PATH,
                                  delim_whitespace=True,
                                  names=('lon', 'lat'))

        self.__add_new_column()
        self.__reorder_colum()

    # abstract method to child classes
    @abstractmethod
    def file_name(self):
        pass

    @abstractmethod
    def type(self):
        pass

    # size of dataframe
    def size(self):
        return len(self.__df)

    # get dataframe
    @property
    def df(self):
        return self.__df

    def append_new_dataframe(self, second_df):
        return self.__df.append(second_df, ignore_index=True)


    # dataframe logic
    def __row_type(self):
        return [f'{self.type()}_{i + 1}' for i in range(self.size())]

    def __add_new_column(self):
        self.__df[self.__TYPE] = self.__row_type()

    def __reorder_colum(self):
        cols = self.__df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        self.__df = self.__df[cols]
