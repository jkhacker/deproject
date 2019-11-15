from abc import ABC, abstractmethod

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