# piegrad
a python implementation of autograd. it automatically differentiates arbitrary functions written in python.

piegrad does something called "source code transformation". by using a specific set of rules (eg decrement exponent by 1 and multiply coefficent by exponent), piegrad converts `func`'s' ast to an ast corresponding to `grad`. by working at the ast level, we leverage cpython's parser.

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
starting from root, we recursively traverse down the abstract syntax tree with a depth first search. 

any node that is not a leaf is a binary operation (binop) that can be described with `(left, op, right)`, where `left` refers to the left node, `op` refers to operation (eg `ast.Add` or `ast.Pow`), and `right` refers to the right child).

we keep traversing until we hit a leaf node (by definition it is not a `ast.BinOp`). when we hit a leaf, we evalute it according to its type (eg is this leaf node a `ast.Num`?) and its parent's type (eg is its parent node a `ast.Pow`?). 