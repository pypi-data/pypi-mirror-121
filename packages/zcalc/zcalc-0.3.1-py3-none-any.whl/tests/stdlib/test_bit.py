import pytest

from zcalc.env import Env
from zcalc.stdlib import math

@pytest.mark.parametrize('line', [
    '0x88 ; 0xf0 ; and ; hex ; 0x80',
    '0x88 ; 0xf0 ; or  ; hex ; 0xf8',
    '0x0f ; 0xff ; xor ; hex ; 0xf0',
    '0x80 ;    3 ; shr ; hex ; 0x10',
    '0x10 ;    3 ; shl ; hex ; 0x80',

    '0x88 ; 0xf0 ;  & ; hex ; 0x80',
    '0x88 ; 0xf0 ;  | ; hex ; 0xf8',
    '0x0f ; 0xff ;  ^ ; hex ; 0xf0',
    '0x80 ;    3 ; >> ; hex ; 0x10',
    '0x10 ;    3 ; << ; hex ; 0x80',

    '420 ; oct ; 0o644',
    '0xf ; bin ; 0b1111',
])
def test_bit(line):
    z = Env(prelude=False)
    z.use('bit')
    z.do(line)
    assert z.pop() == z.pop()
