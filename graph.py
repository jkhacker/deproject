import abc

class Graph(abc.ABC):
    def __init__(self, x0=1, X=9, n=10):
        self.__x0 = x0
        self.__X = X
        self.__n = n

        self.__xgrid = []
        self.__ygrid = []
        self.__grid_step = (X - x0)/n
        while x0 < X:
            self.__xgrid.append(x0)
            x0 += self.__grid_step
        self.__calc()

    @abc.abstractmethod
    def __calc(self):
        raise NotImplementedError

    def recalculate(self, x0, X, n):
        self.__x0 = x0
        self.__X = X
        self.__n = n

        self.__xgrid.clear()
        self.__ygrid.clear()
        self.__grid_step = (X - x0)/n
        while x0 < X:
            self.__xgrid.append(x0)
            x0 += self.__grid_step
        self.__calc()

    def get_xgrid(self):
        return self.__xgrid

    def get_ygrid(self):
        return self.__ygrid

class GraphApprox(Graph):

    def __init__(self, x0=1, y0=0.5, X=9, n=10):
        self.__y0 = y0
        Graph.__init__(x0, X, n)

    def recalculate(self, x0, y0, X, n):
        self.__y0 = y0
        super.recalculate(x0, X, n)

    @abc.abstractmethod
    def __calc(self):
        raise NotImplementedError