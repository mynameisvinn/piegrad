import ast
import astor
import inspect

class grad(object):
    
    def __init__(self, function):        
        
        # we will trace our way through asts
        self.binop_stack = []
        self.data_stack = []
        
        # convert string source code to ast
        tree = ast.parse(inspect.getsource(function), mode='exec')
        
        # start from root, modify root
        root = tree.body[0].body[0].value
        self.down(root)
        
        # modified
        self.curr = tree.body[0]  
        source = astor.to_source(self.curr)
        print(source) 
        
        # https://stackoverflow.com/questions/48759838/how-to-create-a-function-object-from-an-ast-functiondef-node
        code = compile(tree, 'hello.py', 'exec')
        self.namespace = {}
        exec(code, self.namespace)  # put function code object into namespace dictionary
        
    def __call__(self, x):
        return self.namespace["f"](x)


    def down(self, node):
        """
        using depth first search, add to stack ("binop_stack") if node is a 
        binop. otherwise evaluate leaf nodes by calling evaluate.
        """

        # scenario 1 - it is a binop, which means it is not a leaf
        if isinstance(node, ast.BinOp):
            print("adding", node.op, "to binop stack")
            self.binop_stack.append(node)

            # a binop always has a left and right child
            self.down(node.left)
            self.down(node.right)

            # once we've explore left and right children, remove binop from stack
            self.binop_stack.pop()  

        # scenario 2 - it is a leaf, so evaluate according to a specific set of rules
        else:
            self.evaluate(node)

    def evaluate(self, z):
        """evaluate a leaf node.

        how a leaf is evaluated depends on its type (eg it is a ast.Name) 
        and parent's type (eg its parent is ast.Pow).
        """
        print('eval', z)
        parent = self.binop_stack[-1].op

        # scenario 1: node is a Name node
        if isinstance(z, ast.Name):
            if isinstance(parent, ast.Pow):
                exp = self.binop_stack[-1].right.n
                self.binop_stack[-1].right.n -= 1
                self.data_stack[-1].n = self.data_stack[-1].n * exp
                self.data_stack.pop()

        # scenario 2: node is a Num
        if isinstance(z, ast.Num):
            if isinstance(parent, ast.Mult):
                print("adding", z.n, "to data stack")
                self.data_stack.append(z)
            if isinstance(parent, ast.Add):
                print("stop")
                z.n = 0  # since any constants have zero derivative
            if isinstance(parent, ast.Pow):
                pass