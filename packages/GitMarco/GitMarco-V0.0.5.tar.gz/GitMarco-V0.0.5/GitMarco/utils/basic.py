def assertion_test(x, dtype, name: str = ''):
    assert isinstance(x, dtype), \
        f'Wrong data type for {name}. Required : {dtype} - Actual: {type(x)}'
