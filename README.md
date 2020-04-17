# PieGrad
a python implementation of autograd. it automatically differentiates arbitrary functions written in python.

## example
suppose we have function `f` and want to find its gradient `f_prime`. 
```python
from PieGrad import grad

def f(x):
	return 2*(x**3) + 1

f_prime = grad(f)  # return gradient of 6 * x ** 2
f_prime(2)  # prints 24
```
## how dey do dat?
piegrad does something called "source code transformation". by applying a specific set of rules (eg decrement exponent by 1 and multiply coefficent by exponent), piegrad converts `f`'s' ast to an ast corresponding to its gradient. 

starting from root, we recursively traverse the ast with a dfs. 

any node that is not a leaf is a binary operation (`ast.binop`). every `ast.binop` can be described with `(left, op, right)`, where `left` refers to the left node, `op` refers to operation (eg `ast.Add` or `ast.Pow`), and `right` refers to the right child). each child can be a leaf or another `ast.binop`.

we traverse until we hit a leaf (ie not a `ast.BinOp`). how a leaf is evaluated depends on two factors: what is its type (eg is it a `ast.Num`? or is it `ast.Name`?) and what is its parent's type (eg is its parent node a `ast.Pow`?).