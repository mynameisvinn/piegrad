# piegrad
a simple python implementation of autograd. it automatically differentiates any arbitrary function (written in python)

## example
suppose we have function `func` and want to find its gradient `grad`. 
```python
def func(x):
	return 2*(x**2) + 1

# the correct gradient is
def grad(x):
	return 4*x
```
## how dey do dat?
using a specific set of rules (eg decrement exponent by 1 and multiply coefficent by exponent), piegrad converts `func`'s' ast to an ast corresponding to `grad`.