# Computational Practicum

Nikita Smirnov,
IU BS18-04 student

November 2019

[github.com/pakrentos/deproject](github.com/pakrentos/deproject)



## 1. 	Analytical solution

<img src="https://latex.codecogs.com/gif.latex?\begin{cases}&space;y'&space;=&space;\frac{y^2-y}x&space;\\&space;y(1)&space;=&space;0.5&space;\end{cases}" title="\begin{cases} y' = \frac{y^2-y}x \\ y(1) = 0.5 \end{cases}" />

Let us proceed with the analytical solution of FO ODE first

Turning ODE into separable equation:
<img src="https://latex.codecogs.com/gif.latex?y'=\frac{y^2-y}x&space;\rightarrow&space;\frac{\frac{dy}{dx}}{y^2-y}&space;=&space;\frac1x&space;\rightarrow&space;\frac{dy}{y^2-y}=\frac{dx}{x}" title="y'=\frac{y^2-y}x \rightarrow \frac{\frac{dy}{dx}}{y^2-y} = \frac1x \rightarrow \frac{dy}{y^2-y}=\frac{dx}{x}" />

<img src="https://latex.codecogs.com/gif.latex?\int\frac{dy}{y^2-y}=\int\frac1x&space;\rightarrow&space;ln\frac{1-y}y=lnx&plus;C" title="\int\frac{dy}{y^2-y}=\int\frac1x \rightarrow ln\frac{1-y}y=lnx+C" />

<img src="https://latex.codecogs.com/gif.latex?\frac{1-y}y&space;=&space;C_1x&space;\rightarrow&space;y=\frac1{C_1x&plus;1}" title="\frac{1-y}y = C_1x \rightarrow y=\frac1{C_1x+1}" />

Solving IVP problem:
<img src="https://latex.codecogs.com/gif.latex?\begin{cases}&space;y=\frac1{C_1x&plus;1}&space;\\&space;y(1)&space;=&space;0.5&space;\end{cases}&space;\rightarrow&space;0.5&space;=&space;\frac1{C_1&plus;1}&space;\rightarrow&space;C_1&space;=&space;1" title="\begin{cases} y=\frac1{C_1x+1} \\ y(1) = 0.5 \end{cases} \rightarrow 0.5 = \frac1{C_1+1} \rightarrow C_1 = 1" />

<img src="https://latex.codecogs.com/gif.latex?y&space;=&space;\frac1{x&plus;1}" title="y = \frac1{x+1}" />



## 2.	Program description

Simple matplotlib-based plotter for solving IVP for concrete equation. I decided to use python and such libraries as PyQt5 and matplotlib due to their functionality and using ease. 

Program consists of 3 parts: graphs OOP implementation, plotting widget, and main window.

* The most difficult part was implementing pure OOP in Python due to the lack of native support for abstract classes and encapsulation. The hierarchy of self-written graph classes is simple. The main class is the Graph class; it is also abstract. His heirs are analytical and approximating (Euler's method, Euler's improved method and Runge-Kutta method) graphs. Two helper classes are used to calculate local and total errors.

* The matplotlib part is a widget built into the PyQt window. Its main graphic part is processed using the PyQt library, the rest is implemented as an abstract canvas and its parameters
* PyQt part consists only of widgets interconnected using a simplified MVC model, namely, signals and slots



## 3.	Code Parts



#### Abstract Graph implementation:

```python
import ABC, abstractmethod

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
```


#### Exact solution Graph class:

```python
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
```



#### Local errors Graph class:

```python
class ErrorGraph:
    def __init__(self, exact_graph, approx_graph, name):
        self.__exact = exact_graph
        self.__approx = approx_graph
        self.__name = name
        self.__ygrid = [
          x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1],
                                      self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]
    
    def recalculate(self, *args):
        self.__ygrid = [x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1], self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]

    def get_grid(self):
        return self.__xgrid, self.__ygrid, self.__name
```



#### Matplotlib Figure class:

```python
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_title('y\'=(y^2 - y)/x')

    def clr(self):
        self.ax.clear()
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_title('y\'=(y^2 - y)/x')
        self.draw()

    def plot(self, xgrid, ygrid, label, color):
        self.ax.plot(xgrid, ygrid, color, label=label)
        self.ax.legend(fontsize='small')
        self.draw()
```



#### UML Diagram:

<img src="https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Untitled%20Diagram.drawio#R7VxRb5s6FP41kdqHXgVI0vSxIdl277qrad3Vep8ilzjEm8GRMW2yX79jMCHEQGlFQja5ilR8fAD7fIePzyeQnuMGm%2FccrVef2ALTnt1fbHrOtGfbluXY8E9atqnlenSTGnxOFsopN9yTn1gZ%2B8oakwWOCo6CMSrIumj0WBhiTxRsiHP2XHRbMlo86xr5WDPce4jq1m9kIVbZvPr9vOMDJv5KnXo8VB2PyPvhcxaH6nw921kmf2l3gLJjKf9ohRbsec%2FkzHqOyxkT6VawcTGVsc3Clu73rqJ3N26OQ9Fkh4er2wd78u%2B37%2BLd5L9%2FUGx%2FnN5fZSg8IRrjbB7JaMU2ixBeQMBUk3GxYj4LEZ3l1kkSBSzP04dW7nPH2BqMFhi%2FYyG2Cn0UCwamlQio6k3PKU9UOTlliljMPVwzIzV%2BgbiPRY3faAcBpDZmARZ8C%2FtxTJEgT8VxIJVj%2Fs4vjzNsqFC%2FIuy2FvXk6tJCHz2TgKJQxnjJQpGhIEOGKPFD2PYgQpiD4QlzQSCvb1WHkLGfeCtCF3doy2IZjEhA0matyYpx8hMOizIYoJsLBZI9Knjcyz0VwBxH4PM5A8c6MH1Cm4LjHYqEMniMUrSOyONuGgHgRMIJE4IFyknFBqaDN%2FXpoMOndrBHKq%2Bf80t6dyGu9q7mHQ21DrFTcmFN5AhhireSqChDogdRth0rnbXs3db2PtR1hmknCUu6UIDT3khwrVfy8jwSeF139E1K59KBkqhk4If9B5kMWIokwzj7gV1GGaTsNGRpahNKD0xZdlO8FJW5Ha2RR0L%2FLvGZDnLLFwWwNDHYF6YkiXdFFgscJnwlkEBpEsoprBlELUmA4QQ%2BkBJu%2F69hbwgDd6Ft5W34SHcuXBbCXBBJ8hFDhj9jmeXNkreaE%2FSM3mYZ3SyhLXtwpIQevHynoCQBLwU5u5tab0I4AKySe4uC9GtyJ7myNNgdHXanBGKKHjH9zCIiCJPH56nvAfRdoWsNG%2FLV%2BEjgDivYaj4nIRHz%2BUVCHG5OD9WbELTLlAjCWJ74gCg4BpS9GO6y%2BKLZsTS%2BwmIu2ebicp9v3MJWMlxDQS0n6bhZkg7tI2XpSMvSWUwxN9qpVe3kKEizO8%2B4qZYaHEtLXf%2FRWiqlQZ3nthVuhtZeSWsVS72zUVZjo6yOhm7nyurmN1dWO9pxywxlHLiMQ08bwGUdIcpxX8g5FaZneK7lK6GhfBsfS75ZVrl%2B%2BzswCq5NBTcYnZ2Cs%2FSKp5FwhtoaU5tVkfFno%2BGssnqvEXEt4du5irPKqp9GxhkZ18W10LmO06vFX%2BLQxx9jIZCRcm1KudHN%2BUk5vQprpJyht%2Bb0Njx3KVdWbjZSriV8u5dyZeVWI%2BWMlOviWuhcyunl6dkGecKouFZU3PmotuxsRrUZ1fYmJrs5c9Vm618uGNXWGr6dq7YMTaPajGrrmOu6V20ZiZ72JQ0IGt8%2ByP0BAdX8Xx0uaUw3hda2IKBaeblDFR5ffLmjCsETvd0x7Bie67PHp0IvnwifURf4dBHmiuXnicKs19FmnDPzuG6r3xBYdvEbgmH3rz7ZVRU2tF5ztkm1icqCAwWDZfEhddivQxwu%2Fo62Zq1dmJo154lfR7g%2B9zVn2cOdZs3ZEr6drzmdqprZbs25z1FuTmpqRdd0kamt2KqWk3uODZeUhnPazsmu34Fy9DrXVwgkNdKqdWnljF6WVo51UmmV%2FdrGny6tSstqRli1RHLOq5%2BmLU3z4wkrxzxNe0R8y4RVKcBHE1bNn6atUVg1tfkWyvtGkP0WXFUmyEpz%2BQ2CDJr5zzMlfXu%2FgeXMfgE%3D" />

## 4.	Solution analysis 

As we can see from the graphs (provided in the end of the PDF-file) Runge- Kutta is indeed the most presice method among those 3. As we can see from the graph of local error, Euler method is indeed the least precise method. Runge- Kutta is the most precise method of all of them. We can also note from the total error graphs that Euler method total error is $O(h^2)$, Euler method total error is $O(h^3)$, Euler method total error is $O(h^4)$ 



## 5.	Solid principles 

The code is written on Python language that supports OOP. It does not contradict the solid OOP principles: 

#### 5.1 Open-closed principle 

The code is easy to extend without modifying it. For example, to implement the other solution method it is only necessary to extend from graph and implement 2-3 features. 

#### 5.2 Liskov Substitution principle 

Objects in my project can be substituted with their subtypes 

#### 5.3 Interface segregation principle 

PyQt and matplotlib does not contradict Interface segregation principle. 

#### 5.4 Dependency Inversion principle 

This code does not depend on details 



## 6.	Program screenshots:

![image-20191115140438504](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191115140438504.png)

![image-20191115140503918](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191115140503918.png)

![image-20191115140522291](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191115140522291.png)

![image-20191115140537020](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191115140537020.png)

![image-20191116114523544](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191116114523544.png)

![image-20191116114538912](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191116114538912.png)

![image-20191116114554710](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191116114554710.png)
