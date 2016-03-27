import collections
import numbers


class DunderProvider:

    @staticmethod
    def operator_factory(symbol):
        oper_expr = 'Operator("{s}", lambda x, y: x {s} y)'.format(s=symbol)
        return eval(oper_expr)

    def __add__(self, other):
        oper = DunderProvider.operator_factory('+')
        return Expression((self, oper, other))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        oper = DunderProvider.operator_factory('-')
        return Expression((self, oper, other))

    def __rsub__(self, other):
        oper = DunderProvider.operator_factory('-')
        return Expression((other, oper, self))

    def __mul__(self, other):
        oper = DunderProvider.operator_factory('*')
        return Expression((self, oper, other))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        oper = DunderProvider.operator_factory('/')
        return Expression((self, oper, other))

    def __rtruediv__(self, other):
        oper = DunderProvider.operator_factory('/')
        return Expression((other, oper, self))

    def __floordiv__(self, other):
        oper = DunderProvider.operator_factory('//')
        return Expression((self, oper, other))

    def __rfloordiv__(self, other):
        oper = DunderProvider.operator_factory('//')
        return Expression((other, oper, self))

    def __mod__(self, other):
        oper = DunderProvider.operator_factory('%')
        return Expression((self, oper, other))

    def __rmod__(self, other):
        oper = DunderProvider.operator_factory('%')
        return Expression((other, oper, self))


class Constant(DunderProvider):

    '''
    def customize(self):
        dunders = ['__add__', '__mul__', '__sub__', '__truediv__',
                   '__floordiv__', '__mod__', '__divmod__', '__pow__']
        operators = ['+', '*', '-', '/', '//', '%', 'divmod', '**']

        for d, o in zip(dunders, operators):
            Constant.__dict__[d] = Expression((constant.operator_factory(o)))
    '''
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self):
        raise AttributeError('''Can't set new value
        for {} object'''.format(type(self).__name__))

    def __str__(self):
        return str(self.value)

    def evaluate(self, **variables):
        return self.value


class Variable(DunderProvider):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, **variables):
        return variables[self.name]


class Operator:

    objects = set()

    def __new__(cls, *args, **kwargs):
        for ind, obj in enumerate(cls.objects):
            if all(arg in obj.__dict__.values() for arg in args):
                return obj
        new_obj = super().__new__(cls)
        return new_obj

    def __init__(self, symbol, func):
        self.symbol, self.func = symbol, func
        self.objects.add(self)

    def __str__(self):
        return self.symbol

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Expression(DunderProvider):

    def __init__(self, expression):
        self.expression = list(expression)
        self._variable_names = set()

    def stringify(self, expression):
        for ind, exp in enumerate(expression):
            if isinstance(exp, collections.Sequence):
                expression[ind] = list(exp)
                self.stringify(expression[ind])
            else:
                expression[ind] = str(expression[ind])

    def __str__(self):
        str_ver = self.expression[:]
        self.stringify(str_ver)
        final_ver = str(str_ver)
        while "'" in final_ver:
            final_ver = final_ver.replace("'", '')
        while "," in final_ver:
            final_ver = final_ver.replace(",", '')
        while "[" in final_ver:
            final_ver = final_ver.replace("[", '(')
        while "]" in final_ver:
            final_ver = final_ver.replace("]", ')')
        return final_ver

    def get_variable_names(self, expression):
        for exp in expression:
            if isinstance(exp, Variable):
                self._variable_names.add(exp.name)
            elif isinstance(exp, collections.Sequence):
                self.get_variable_names(exp)

    @property
    def variable_names(self):
        self.get_variable_names(self.expression)
        return tuple(self._variable_names)

    def simplify(self, expr, **variables):
        operands = []
        for el in expr:
            if isinstance(el, Operator):
                oper = el
            elif isinstance(el, Variable):
                operands.append(variables[el.name])
            elif isinstance(el, Constant):
                operands.append(el.value)
            elif isinstance(el, numbers.Number):
                operands.append(el)
            elif isinstance(el, Expression):
                operands.append(self.evaluate_v2(el.expression, **variables))
        return oper(*operands)

    def evaluate_v2(self, expression, **variables):
        if any(hasattr(x, '__iter__') for x in expression):
            for ind, expr in enumerate(expression):
                if hasattr(expr, '__iter__'):
                    expression[ind] = list(expr)
                    res = self.evaluate_v2(expression[ind], **variables)
                    expression[ind] = res
        else:
            res = self.simplify(expression, **variables)

        return self.simplify(expression, **variables)

    def evaluate(self, **variables):
        return self.evaluate_v2(self.expression,  **variables)


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)



plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
minus = create_operator('-', lambda l, r: l - r)
times = create_operator('*', lambda le, ri: le * ri)
x = create_variable('x')
y = create_variable('y')
six = create_constant(6)
nine = create_constant(9)
#expression = create_expression((six, plus, nine))
#print(expression.evaluate())
expression = create_expression((six, times, ((x, minus, y), plus, nine)))
print(expression.evaluate(x=5, y=2))
twelve = create_constant(12)
print(expression.expression)
expression = create_expression((x, plus, (y, times, twelve)))
#print(expression.evaluate(x=5, y=2))
print(expression.expression)
