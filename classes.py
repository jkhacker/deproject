from graph import Graph
import numpy as np

class ExactGraph(Graph):
    def __func(self, x, c):
        try:
            res =  1/(c*x+1)
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold) 
        res = np.ma.masked_greater(res, threshold)
        return res

    def _Graph__calc(self):
        c = 1/self._Graph__y0 - 1
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(self.__func(x_i, c))

class EulerGraph(Graph):
    def __func(self, x, y):
        try:
            res = (y**2 - y)/x
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold)
        res = np.ma.masked_greater(res, threshold)
        return res

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            y_i = y_i + self._Graph__grid_step*self.__func(x_i, y_i)

class EulerImGraph(Graph):
    def __func(self, x, y):
        try:
            res = (y**2 - y)/x
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold)
        res = np.ma.masked_greater(res, threshold)
        return res

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            y_i = y_i + (self._Graph__grid_step/2)*(
                self.__func(x_i, y_i) + self.__func(
                    x_i + self._Graph__grid_step, y_i +
                    self._Graph__grid_step*self.__func(x_i, y_i)
                )
            )

class RungeKuttaGraph(Graph):
    def __func(self, x, y):
        try:
            res = (y**2 - y)/x
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold)
        res = np.ma.masked_greater(res, threshold)
        return res

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            k1 = self.__func(x_i, y_i)
            k2 = self.__func(x_i + self._Graph__grid_step/2, y_i + k1*self._Graph__grid_step/2)
            k3 = self.__func(x_i + self._Graph__grid_step/2, y_i + k2*self._Graph__grid_step/2)
            k4 = self.__func(x_i + self._Graph__grid_step, y_i + k3*self._Graph__grid_step)
            y_i = y_i + self._Graph__grid_step*(k1 + 2*k2 + 2*k3 + k4)/6

class ErrorGraph:
    def __init__(self, exact_graph, approx_graph, name):

        self.__exact = exact_graph
        self.__approx = approx_graph
        self.__name = name
        self.__ygrid = [x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1], self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]
    
    def recalculate(self, *args):
        self.__ygrid = [x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1], self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]

    def get_grid(self):
        return self.__xgrid, self.__ygrid, self.__name
