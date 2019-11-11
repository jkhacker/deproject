from graph import Graph, GraphApprox

class ExactGraph(Graph):
    def __func(self, x):
        return 1/(x+1)

    def __calc(self):
        for x_i in self.__xgrid:
            self.__ygrid.append(self.__func(x_i))



class EulerGraph(GraphApprox):
    def __func(self, x, y):
        return (y**2 - y)/x

    def __calc(self):
        y_i = self.__y0
        for x_i in self.__xgrid:
            self.__ygrid.append(y_i)
            y_i = y_i + self.__grid_step*self.__func(x_i, y_i)

class EulerImGraph(GraphApprox):
    def __func(self, x, y):
        return (y**2 - y)/x

    def __calc(self):
        y_i = self.__y0
        for x_i in self.__xgrid:
            self.__ygrid.append(y_i)
            y_i = y_i + (self.__grid_step/2)*(
                self.__func(x_i, y_i) + self.__func(
                    x_i + self.__grid_step, y_i +
                    self.__grid_step*self.__func(x_i, y_i)
                )
            )

class RungeKuttaGraph(GraphApprox):
    def __func(self, x, y):
        return (y**2 - y)/x

    def __calc(self):
        y_i = self.__y0
        for x_i in self.__xgrid:
            self.__ygrid.append(y_i)
            k1 = self.__func(x_i, y_i)
            k2 = self.__func(x_i + self.__grid_step/2, y_i + k1*self.__grid_step/2)
            k3 = self.__func(x_i + self.__grid_step/2, y_i + k2*self.__grid_step/2)
            k4 = self.__func(x_i + self.__grid_step, y_i + k3*self.__grid_step)
            y_i = y_i + self.__grid_step*(k1 + 2*k2 + 2*k3 + k4)/6

