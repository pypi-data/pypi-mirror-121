import decimal
import operator
from zcalc.lib import CalcError, op, reduce

@op(aliases=['+', 'a'])
def add(z):
    z.op2(operator.add, z.pop_number)

@op(aliases=['/', 'd'])
def div(z):
    try:
        z.op2(operator.truediv, z.pop_number)
    except decimal.DivisionByZero:
        raise CalcError('division by zero')

@op()
def frac(z):
    def fn(d):
        (num, denom) = d.as_integer_ratio()
        return f'{num}/{denom}'
    z.op1(fn, z.pop_decimal)

@op(name='int')
def int_(z):
    z.op1(int, z.pop_number)

@op(aliases=['%'])
def mod(z):
    z.op2(operator.mod, z.pop_number)

@op(aliases=['*', 'm'])
def mul(z):
    z.op2(operator.mul, z.pop_number)

@op()
def neg(z):
    z.op1(operator.neg, z.pop_number)

@op()
def norm(z):
    z.op1(lambda d: d.normalize(), z.pop_decimal)

@op()
def prec(z):
    places = z.pop_int()
    decimal.getcontext().prec = places

@op(name='?prec')
def prec_q(z):
    z.info = f'{decimal.getcontext().prec} places'

@op(aliases=['r'])
def round(z):
    digits = z.pop_int()
    number = z.pop_decimal()
    amount = '.' + ('0' * (digits - 1)) + '1'
    z.push(number.quantize(decimal.Decimal(amount)))

@op(aliases=['-', 's'])
def sub(z):
    z.op2(operator.sub, z.pop_number)

@op()
def sum(z):
    reduce(z, ['add'])

