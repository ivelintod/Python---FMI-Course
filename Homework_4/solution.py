import ast
import inspect
from collections import defaultdict


MESSAGES = {
    'line_length': 'line too long ({} > {})',
    'forbid_semicolons': 'multiple expressions on the same line',
    'max_nesting': 'nesting too deep ({} > {})',
    'indentation_size': 'indentation is {} instead of {}',
    'methods_per_class': 'too many methods in class({} > {})',
    'max_arity': 'too many arguments({} > {})',
    'forbid_trailing_whitespace': 'trailing whitespace',
    'max_lines_per_function': 'method with too many lines ({} > {})'
}


DEFAULTS = {
    'line_length': 79,
    'forbid_semicolons': True,
    'max_nesting': None,
    'indentation_size': 4,
    'methods_per_class': None,
    'max_arity': None,
    'forbid_trailing_whitespace': True,
    'max_lines_per_function': None
}


ERRORS = defaultdict(set)


def check_line_len(code, limit):
    current_len = 0
    current_line = 1
    print(len(code))
    for ind, char in enumerate(code):
        if char != '\n':
            current_len += 1
        elif current_len >= limit:
            ERRORS[current_line].add(MESSAGES['line_length']
            .format(current_line, DEFAULTS['line_length']))
            current_len = 0
        else:
            current_line += 1
        if ind == len(code) - 1 and current_len >= limit:
            ERRORS[current_line].add(MESSAGES['line_length']
                          .format(current_len, DEFAULTS['line_length']))
            current_len = 0
            current_line += 1
    #return ERRORS


def check_for_semicolons(code, forbidden):
    current_line = 1
    OFF = False
    for ind in code:
        if ind == '"' or ind == "'":
            True if not OFF else False
        elif not OFF:
            if ind == ';':
                ERRORS[current_line].add(MESSAGES['forbid_semicolons'])
            if ind == '\n':
                current_line += 1
    #return ERRORS



def critic(code, **rules):
    DEFAULTS.update(rules)
    check_line_len(code, DEFAULTS['line_length'])
    check_for_semicolons(code, DEFAULTS['forbid_semicolons'])
    return ERRORS


'''def foo(a):
    b = 2 + 2
    a = []
    for i in range(11):
        a.append(i)

print(inspect.getsource(foo))
example_ast = ast.parse(inspect.getsource(foo))
print(ast.dump(example_ast))

ast.NodeVisitor().visit(example_ast)'''


if __name__ == '__main__':
    code = ("def some_func():\n"
                "    a_variable = 'some text';"
                " another_variable = 'some more text';"
                " even_moar_variables = 'just for to pass the time'")
    print(critic(code))
