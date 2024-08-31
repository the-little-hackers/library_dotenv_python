# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from os import PathLike
from typing import Any

import dotenv
from thelittlehackers.constant.data_type import DataType
from thelittlehackers.utils.string_utils import DATA_TYPE_CONVERTERS


def __cast_value(
        value: Any,
        data_type: DataType = DataType.STRING,
        **kwargs) -> Any:
    """
    Convert a value, more likely a string, to the specified data type


    :param value: The string to be converted to the specified data type.

    :param data_type: An item of `DataType` that indicates the data type
        to cast the value to.

    :param enumeration: A Python class inheriting from `Enum`.  The value
        passed to this function MUST be an item or a string representation
        of an item of this enumeration.

    :param item_data_type: An item of `DataType` that specifies the desired
        data type of every item of the value (a list).  The argument
        `data_type` MUST be `DataType.list`.

    :param object_class: A Python class used to instantiate a new object
        from the value (a JSON string representation). The argument
        `data_type` MUST be `object`.  This Python class MUST implement a
        static method `from_json` that returns an instance of this class
        providing a JSON expression.

        If this argument `object_class` is not defined, while the argument
        `data_type` is `object`, the function uses the class `Object` to
        instantiate a new object from the JSON string representation.


    :return: The value converted to the desired data type.


    :raise ValueError: If the argument ``data_type`` is 
        ``DataType.enumeration`` but the argument ``enumeration`` has not
        been passed to this function.

    :raise TypeError: If the argument `value` is not a valid string
        representation of the desired data type.
    """
    if data_type not in DataType:
        raise ValueError("The argument 'data_type' MUST be an item of the enumeration 'DataType'")

    converter = DATA_TYPE_CONVERTERS.get(data_type)
    if converter is None:
        raise NotImplementedError(f"No converter for data type \"{data_type}\"")

    value = converter(value, **kwargs)

    return value


def getenv(
        name: str,
        data_type: DataType = DataType.STRING,
        default_value: Any = None,
        is_required: bool = True,
        **kwargs
) -> Any:
    """
    Return the value of an environment variable.


    :param name: Name of an environment variable.

    :param data_type: An item of `DataType` that indicates the data type
        to cast the value to.

    :param default_value: Default value to return when the environment
        variable doesn't exist.

    :param is_required: Indicate whether the environment variable MUST
        exist.  If the environment variable doesn't exist, while the
        argument `is_required` is `True` and the argument `default_value`
        is not passed, the function raises an exception.

    :param enumeration: A Python class inheriting from `Enum`.  The value
        passed to this function MUST be a member or a string representation
        of a member of this enumeration.

    :param item_data_type: A member of ``DataType`` that specifies the
        desired data type of every item of the value (a list).  The
        argument ``data_type`` MUST be ``DataType.LIST``.

    :param object_class: A Python class used to instantiate a new object
        from the value (a JSON string representation). The argument
        ``data_type`` MUST be ``DataType.OBJECT`.  This Python class
        MUST implement a static method `from_json` that returns an
        instance of this class providing a JSON expression.

If this argument ``object_class`` is not defined, while the argument
`data_type` is `object`, the function uses the class `Object` to
instantiate a new object from the JSON string representation.


    :return: The value of the environment variable converted to the
        desired data type.


    :raise Error: If the environment variable doesn't exist.
    """
    value = os.getenv(name)

    if value:
        value = __cast_value(value, data_type=data_type, **kwargs)
    elif default_value is not None:
        value = __cast_value(default_value, data_type=data_type, **kwargs)
    elif is_required:
        raise Exception(f"The environment variable \"{name}\" is not defined")

    return value


def loadenv(env_path_file_name: str or PathLike) -> bool:
    """
    Load environment variables from the local file `.env`.


    :param env_path_file_name: Absolute or relative path to .env file.
    """
    return dotenv.load_dotenv(env_path_file_name or '.env')


def setenv(name: str, value: Any) -> None:
    """
    Set an environment variable.


    :param name: The name of the environment variable to set.

    :param value: The value of the environment variable.
    """
    os.environ[name] = str(value)
