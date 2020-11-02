from abc import ABC, abstractmethod
import numpy as np
from utils import *

class Graph(ABC):
    def __init__(self, name, x0=1, y0=0.5, X=9, n=10):
        self.__x0 = x0
        self.__X = X
        self.__n = n
        self.__y0 = y0
        self.__name = name

        self.__xgrid = []
        self.__ygrid = []
        self.__grid_step = (X - x0)/n
        while x0 < X:
            self.__xgrid.append(x0)
            x0 += self.__grid_step
        self.__calc()
        super().__init__()

    @abstractmethod
    def __calc(self):
        pass

    def __func(self, x, y):
        try:
            res = gen_func(x, y)
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold)
        res = np.ma.masked_greater(res, threshold)
        return res

    def recalculate(self, x0, y0, X, n):
        self.__x0 = x0
        self.__X = X
        self.__n = n
        self.__y0 = y0

        self.__xgrid.clear()
        self.__ygrid.clear()
        self.__grid_step = (X - x0)/n
        while x0 < X:
            self.__xgrid.append(x0)
            x0 += self.__grid_step
        self.__calc()

    def get_grid(self):
        return self.__xgrid, self.__ygrid, self.__name