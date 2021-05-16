# Python init-args based Serializer
[![PyPI version](https://badge.fury.io/py/init-args-serializer.svg)](https://badge.fury.io/py/init-args-serializer)
[![codecov](https://codecov.io/gh/famura/init-args-serializer/branch/master/graph/badge.svg?token=7NIHSH9VKD)](https://codecov.io/gh/famura/init-args-serializer)

This package provides improved pickling support. Instead of storing the entire state dict `__dict__`, the parameters passed to the initializer `__init__()` are captured. 
During unpickling, the captured parameters are used to create a new object instance.

This behaviour is implemented using the `__reduce__()` hook. 
Thus, it is strongly discouraged to override the `__reduce__()` method. 
If you need to pickle variables beyond the constructor parameters, you should use the regular `__getstate__()` and `__setstate__()` methods.

## Installation
```
pip install init-args-serializer
```

## Usage
```
class MyCustomClass(OptionalBaseClass, Serializable):
    
    def __init__(self, *args, **kwargs):
        # Recommended to call this first
        Serializable._init(self, locals())

```
