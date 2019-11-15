# Computational Practicum



## 1. 	Analytical solution

$$
\begin{cases}
y' = \frac{y^2-y}x \\
y(1) = 0.5
\end{cases}
$$

Let us proceed with the analytical solution of FO ODE first

Turning ODE into separable equation:
$$
y'=\frac{y^2-y}x \rightarrow \frac{\frac{dy}{dx}}{y^2-y} = \frac1x \rightarrow \frac{dy}{y^2-y}=\frac{dx}{x}
$$

$$
\int\frac{dy}{y^2-y}=\int\frac1x \rightarrow ln\frac{1-y}y=lnx+C
$$

$$
\frac{1-y}y = C_1x \rightarrow y=\frac1{C_1x+1}
$$

Solving IVP problem:
$$
\begin{cases}
y=\frac1{C_1x+1} \\
y(1) = 0.5
\end{cases} \rightarrow
0.5 = \frac1{C_1+1} \rightarrow C_1 = 1
$$

$$
y = \frac1{x+1}
$$



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

![Untitled Diagram](/Users/nikitasmirnov/Untitled Diagram.png)

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

![image-20191115140628208](/Users/nikitasmirnov/Library/Application Support/typora-user-images/image-20191115140628208.png)

