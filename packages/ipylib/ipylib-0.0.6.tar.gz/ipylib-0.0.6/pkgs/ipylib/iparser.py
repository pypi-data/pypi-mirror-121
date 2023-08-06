# -*- coding: utf-8 -*-
from idebug import *
from ipylib.inumber import *
from ipylib.idatetime import *


__all__ = [
    'ValueDtypeParser',
]

def ValueDtypeParser(v, dtype, ndigits=4):
    try:
        if dtype == 'int':
            return iNumber(v)
        elif dtype == 'int_abs':
            return abs(iNumber(v))
        elif dtype == 'float':
            return iNumber(v, prec=ndigits, sosujeom='.')
        elif dtype == 'pct':
            return Percent(v, prec=2, sosujeom='.').num
        elif dtype in ['date','time','dt','datetime']:
            return DatetimeParser(v)
        elif dtype == 'str':
            return v
        else:
            logger.exception(f"정의되지 않은 데이타-타입({dtype})을 입력했다. {locals()}")
    except Exception as e:
        logger.exception(f"파싱 에러가 발생하면, 입력된 값을 그대로 반환한다. {locals()}")
        return v
