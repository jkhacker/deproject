import numpy as np
class Solution:
    
    def __init__(self, n=1, x0=1, y0=0.5, X=9):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n

        self.x_grid = []
        self.grid_step = (X - x0)/self.n
        while x0 < X:
            self.x_grid.append(x0)
            x0 += self.grid_step
        
        self.y_grid_e = []
        self.y_grid_exact = []
        self.y_grid_eim = []
        self.y_grid_rk = []

        self.exact()
        self.euler()
        self.eulerim()
        self.rungekutta()


    def set_accuracy(self, n, x0=1, y0=0.5, X=9):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n

        self.x_grid = []
        self.grid_step = (X - x0)/self.n
        while x0 < X:
            self.x_grid.append(x0)
            x0 += self.grid_step

        self.y_grid_e = []
        self.y_grid_exact = []
        self.y_grid_eim = []
        self.y_grid_rk = []

        self.exact()
        self.euler()
        self.eulerim()
        self.rungekutta()

    def get_x_grid(self):
        return self.x_grid
    
    def get_y_grid_exact(self):
        return self.y_grid_exact
    
    def get_y_grid_e(self):
        return self.y_grid_e

    def get_y_grid_eim(self):
        return self.y_grid_eim

    def get_y_grid_rk(self):
        return self.y_grid_rk

    def func(self, x, y):
        return (y**2 - y)/x

    def exact(self):
        self.y_grid_exact.clear()
        for x_i in self.x_grid:
            if x_i == 0.0:
                self.y_grid_exact.append(np.nan)
                print('sas')
                continue
            self.y_grid_exact.append(1/(x_i+1))

    def euler(self):
        self.y_grid_e.clear()
        y_i = self.y0
        for x_i in self.x_grid:
            self.y_grid_e.append(y_i)
            y_i = y_i + self.grid_step*self.func(x_i, y_i)

    def eulerim(self):
        self.y_grid_eim.clear()
        y_i = self.y0
        for x_i in self.x_grid:
            self.y_grid_eim.append(y_i)
            y_i = y_i + (self.grid_step/2)*(
                                        self.func(x_i, y_i) + self.func(
                                            x_i + self.grid_step, y_i + self.grid_step*self.func(x_i, y_i)
                                            )
                                        )

    def rungekutta(self):
        self.y_grid_rk
        y_i = self.y0
        for x_i in self.x_grid:
            self.y_grid_rk.append(y_i)
            k1 = self.func(x_i, y_i)
            k2 = self.func(x_i + self.grid_step/2, y_i + k1*self.grid_step/2)
            k3 = self.func(x_i + self.grid_step/2, y_i + k2*self.grid_step/2)
            k4 = self.func(x_i + self.grid_step, y_i + k3*self.grid_step)
            y_i = y_i + self.grid_step*(k1 + 2*k2 + 2*k3 + k4)/6

