import typing
from cake import Number, Integer, Prime

def createInteger(x: typing.Any, check_value_attr: bool = True, *args, **kwargs):
    return Integer(
        x, check_value_attr,
        *args, **kwargs
    )

def createPrime(x: typing.Any, check_value_attr: bool = True, *args, **kwargs):
    return Prime(
        x, check_value_attr,
        *args, **kwargs
    )

MAPPING = {
    int: createInteger
}


def convert_type(result: typing.Any, check_value_attr: bool = True, *args, **kwargs) -> object:
    """
    Returns an object of the specified type

    Parameters
    ----------
    result: :class:`~typing.Any`
        The result/object to convert the type to
    """
    func = MAPPING.get(result.__class__)

    if not func:
        raise TypeError('Cannot find a specified class for this type')
    return func(result, check_value_attr, *args, **kwargs)
    
