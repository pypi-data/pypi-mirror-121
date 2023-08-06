import pytest

from zcalc.env import Env
from zcalc.stdlib import math

@pytest.mark.parametrize('line', [
    '6 ; 2 ; + ; 8',
    '6 ; 2 ; - ; 4',
    '6 ; 2 ; * ; 12',
    '6 ; 2 ; / ; 3',
    '3 ; 2 ; % ; 1',

    '6 ; 2 ; a ; 8',
    '6 ; 2 ; s ; 4',
    '6 ; 2 ; m ; 12',
    '6 ; 2 ; d ; 3',

    '[add 6 2 ; 8',
    '[sub 6 2 ; 4',
    '[mul 6 2 ; 12',
    '[div 6 2 ; 3',
    '[mod 3 2 ; 1',

    '[add 1.1 2.2 ; 3.3',  # ensure it is a decimal, not float
    '[frac 0.5 ; 1/2',
    '[int 2.99 ; 2',
    '[neg -5 ; 5',
    '[norm 1.40500e2 ; 140.5',
    '[sum 1 2 3 4 ; 10',

])
def test_math(line):
    z = Env(prelude=False)
    z.use('math')
    z.do(line)
    assert z.pop() == z.pop()

