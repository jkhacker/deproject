class Solution:
    
    def __init__(self, x0 = 1, y0 = 0.5, X = 9):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = 10
        self.x_grid = []
        self.grid_step = (X - x0)/self.n
        while x0 < X:
            self.x_grid.append(x0)
            x0 += self.grid_step

    def accuracy(self, n):
        self.n = n
        x0 = self.x0
        self.x_grid = []
        self.grid_step = (self.X - self.x0)/self.n
        while x0 < self.X:
            self.x_grid.append(x0)
            x0 += self.grid_step

    
    def xgrid(self):
        return self.x_grid

    def func(self, x, y):
        return (y**2 - y)/x

    def euler(self):
        data = []
        y_i = self.y0
        for x_i in self.x_grid:
            data.append(y_i)
            y_i = y_i + self.grid_step*self.func(x_i, y_i)     
        return data

    def eulerim(self):
        data = []
        y_i = self.y0
        for x_i in self.x_grid:
            data.append(y_i)
            y_i = y_i + (self.grid_step/2)*(
                                        self.func(x_i, y_i) + self.func(
                                            x_i + self.grid_step, y_i + self.grid_step*self.func(x_i, y_i)
                                            )
                                        )
        return data

    def rungekutta(self):
        data = []
        y_i = self.y0
        for x_i in self.x_grid:
            data.append(y_i)
            k1 = self.func(x_i, y_i)
            k2 = self.func(x_i + self.grid_step/2, y_i + k1*self.grid_step/2)
            k3 = self.func(x_i + self.grid_step/2, y_i + k2*self.grid_step/2)
            k4 = self.func(x_i + self.grid_step, y_i + k3*self.grid_step)
            y_i = y_i + self.grid_step*(k1 + 2*k2 + 2*k3 + k4)/6
        return data
