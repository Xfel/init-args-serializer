import init_args_serializer.function_arg_capture as uut


# Positional and keyword args land in the kwargs
def simple_capturing_function(arg1, arg2="default_arg2", arg3="default_arg3"):
    # Capture and return args
    return uut.capture_args(simple_capturing_function, locals())


def test_simple_nooptional():
    args, kwargs = simple_capturing_function("val_arg1")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "default_arg2", "arg3": "default_arg3"}


def test_simple_posoptional():
    args, kwargs = simple_capturing_function("val_arg1", "val_arg2")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "val_arg2", "arg3": "default_arg3"}


def test_simple_kwoptional():
    args, kwargs = simple_capturing_function("val_arg1", arg3="val_arg3")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "default_arg2", "arg3": "val_arg3"}


# Dealing with var positional args
def varposargs_capturing_function(arg1, arg2="default_arg2", *varposarg, kwonlyarg="default_kwonlyarg"):
    # Capture and return args
    return uut.capture_args(varposargs_capturing_function, locals())


def test_varposargs_nooptional():
    args, kwargs = varposargs_capturing_function("val_arg1")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "default_arg2", "kwonlyarg": "default_kwonlyarg"}


def test_varposargs_posoptional():
    args, kwargs = varposargs_capturing_function("val_arg1", "val_arg2")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "val_arg2", "kwonlyarg": "default_kwonlyarg"}


def test_varposargs_withva():
    args, kwargs = varposargs_capturing_function("val_arg1", "val_arg2", "varposarg1", "varposarg2")
    assert args == ("val_arg1", "val_arg2", "varposarg1", "varposarg2")
    assert kwargs == {"kwonlyarg": "default_kwonlyarg"}


def test_varposargs_withvakw():
    args, kwargs = varposargs_capturing_function(
        "val_arg1", "val_arg2", "varposarg1", "varposarg2", kwonlyarg="val_kwonlyarg"
    )
    assert args == ("val_arg1", "val_arg2", "varposarg1", "varposarg2")
    assert kwargs == {"kwonlyarg": "val_kwonlyarg"}


# Dealing with var keyword args
def varkwargs_capturing_function(arg1, arg2="default_arg2", **kwargs):
    # Capture and return args
    return uut.capture_args(varkwargs_capturing_function, locals())


def test_varkwargs_nooptional():
    args, kwargs = varkwargs_capturing_function("val_arg1")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "default_arg2"}


def test_varkwargs_posoptional():
    args, kwargs = varkwargs_capturing_function("val_arg1", "val_arg2")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "val_arg2"}


def test_varkwargs_varkw():
    args, kwargs = varkwargs_capturing_function("val_arg1", "val_arg2", varkw1="val_varkw1", varkw2="val_varkw2")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "val_arg2", "varkw1": "val_varkw1", "varkw2": "val_varkw2"}


# Omitting default values
def nodefval_capturing_function(arg1, arg2="default_arg2", arg3="default_arg3"):
    # Capture and return args
    return uut.capture_args(simple_capturing_function, locals(), omit_defaulted_params=True)


def test_nodefval_nooptional():
    args, kwargs = nodefval_capturing_function("val_arg1")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1"}


def test_nodefval_posoptional():
    args, kwargs = nodefval_capturing_function("val_arg1", "val_arg2")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg2": "val_arg2"}


def test_nodefval_kwoptional():
    args, kwargs = nodefval_capturing_function("val_arg1", arg3="val_arg3")
    assert args == ()
    assert kwargs == {"arg1": "val_arg1", "arg3": "val_arg3"}
