from thelittlehackers.constant.entity import EntityStatusfrom thelittlehackers.constant.data_type import DataTypefrom datetime import datetime

# The Little Hackers Python GetEnv Library
Python utility library for accessing and managing environment variables.

This library utilizes [`python-dotenv`](https://github.com/theskumar/python-dotenv) to load key-value pairs from a `.env` file, supporting the development of applications in alignment with the 12-factor principles.

This library offers a helper function to convert environment variable values to their expected data types.

For examples:

```python
from thelittlehackers.utils.env import loadenv
from thelittlehackers.utils.env import getenv
from thelittlehackers.constant.data_type import DataType
from thelittlehackers.constant.entity import EntityStatus


loadenv()

consumer_key = getenv('CONSUMER_KEY', is_required=True)
consumer_secret = getenv('CONSUMER_SECRET', is_required=False)

last_sync_timestamp = getenv(
    'LAST_SYNC_TIME',
    date_type=DataType.TIMESTAMP, 
    is_required=False
)

sync_status = getenv(
    'SYNC_STATUS',
    data_type=DataType.ENUMERATION, 
    enumeration=EntityStatus,
    is_required=True,
    default_value=EntityStatus.ENABLED
)
```