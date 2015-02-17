from _pytest.assertion.rewrite import rewrite_asserts
import ast, astunparse, sys

with open(sys.argv[1], 'r') as open_file:
    ast_tree = ast.parse(open_file.read())
rewrite_asserts(ast_tree)
print astunparse.unparse(ast_tree)
