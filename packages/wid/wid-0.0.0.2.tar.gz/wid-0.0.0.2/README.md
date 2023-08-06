# wid

WID - [wee double_u id] - short UUIDs [lossless]

i love the utility of UUIDs.

i do no love the length of UUIDs i.e.: 36 characters.

22 characters is 14 characters shorter and therefore better.

22 characters that maintain all the information of the original 36 characters and can be converted back to the original UUID is awesome !

## install

```
pip install wid
```


## import

```
from wid import wid, wid_to_uuid
```

## examples

```
In [1]: from wid import wid, wid_to_uuid

In [2]: w = wid()

In [3]: w
Out[3]: 'QTXQVNL_kGG8WlMAxSjOnw'

In [4]: wid_to_uuid(w)
Out[4]: UUID('93f2cd55-05d3-4061-bc5a-5300c528ce9f')
```

## django

```
from wid import wid
from django.db import models

class Example(models.Model):
    id = models.TextField(primary_key=True, default=wid)
    .... more fields ....
```
