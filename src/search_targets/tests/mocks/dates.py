"""
Date mocking has some specificities.

- `datetime.datetime.now()` and `datetime.datetime.today()` can't be overriden 
with a Mock object easily as they are implemented in C and builtin 
- To solve this, we could then mock the class `datetime.datetime` and target 
the methods. It works well but has side effects related to calls like 
`isinstance(date, datetime.datetime)` : since we've mocked the class with a 
`Mock()` (an instance), the call becomes erroneous
- To solve this, the mock library makes available a `spec` attribute, which 
is supposed to help us pass this hurdle
(see https://docs.python.org/3/library/unittest.mock.html#the-mock-class)
- However, I couldn't manage to make it work. After more digging, I found the
post quoted below that proposes the current solution. It's based on overriding
the `__instancecheck__` for our mocked datetime classes. For more info, see 
this nice post : https://blog.xelnor.net/python-mocking-datetime/
"""

from typing import Any, Type
import datetime


def _get_custom_inst_check_subclass(real_class: Type[Any]):
    """
    Return a class with custom instance check, to compare
    with given class
    """
    class _CustomInstanceCheckSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_class)
    return _CustomInstanceCheckSubclassMeta


def get_datetime_mocker(mocked_date: datetime.datetime) -> Type[datetime.datetime]:
    """ 
    Return a datetime.datetime class with `datetime.datetime.now()` and
    `datetime.datetime.utcnow()` mocked at given date
    """
    class BaseMockedDatetime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return mocked_date.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return mocked_date

    custom_instance_check_class = _get_custom_inst_check_subclass(datetime.datetime)
    mocked_datetime_class = custom_instance_check_class(
        "datetime", (BaseMockedDatetime,), {}
    )
    return mocked_datetime_class


def get_date_mocker(mocked_date: datetime.datetime) -> Type[datetime.date]:
    """ 
    Return a datetime.date class with `datetime.datetime.today()` mocked at 
    given date
    """
    class BaseMockedDate(datetime.date):
        @classmethod
        def today(cls, tz=None):
            return mocked_date.replace(tzinfo=tz)

    custom_instance_check_class = _get_custom_inst_check_subclass(datetime.date)
    mocked_date_class = custom_instance_check_class(
        "date", (BaseMockedDate,), {}
    )
    return mocked_date_class
