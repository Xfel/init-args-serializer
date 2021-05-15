from collections import OrderedDict
from collections.abc import Iterable
from inspect import unwrap, signature, Parameter


def capture_args(function, _locals, omit_defaulted_params: bool = False):
    """
    Extract the function's arguments from the local variable dict.

    Ideally, we would replicate the original arguments exactly. Unfortunately, there is no way to tell whether a parameter
    was passed as positional or keyword argument, or if a keyword parameter was passed at all.

    As far as possible, arguments are stored by their name in the keyword argument dict. If that is not possible,
    they are stored as positional arguments. This is only necessary for positional arguments before a var
    positional argument.

    If a parameter has not been specified, it might be desireable to omit it from serialization, so that future changes
    to the default value are possible. However, there is no way to tell whether a parameter was not passed, or if it was
    explicitly specified to have the default value. Thus, this functionality is turned off by default. You can specify
    omit_defaulted_params=True to remove default values for all parameters, or pass a list of parameter names whose default
    values should be removed.

    .. code-block:: python

        def foo(a1,a2=None,*va, kw1=2, **kw):
            # Get passed arguments
            args, kwargs = capture_args(foo, locals(), omit_defaulted_params=['kw1'])
            # ...

    :param function: The function whose arguments to extract.
    :param _locals: Local variable dict as retured by builtin locals()
    :param omit_defaulted_params: Whether to omit keyword arguments whose value is their default. This may be True
                                  to do so for all keyword arguments, or a container to do so for the listed arguments.
    :return: tuple (args, kwargs)
    """
    # Since we should be called by the function definition, we do not want to see any modified signature added by delegates.
    function = unwrap(function)
    # Use inspect.Signature to determine parameter names.
    sig = signature(function)

    # Collect parameter values
    pos_args = []
    kw_args = OrderedDict()
    for p in sig.parameters.values():
        if p.kind == Parameter.POSITIONAL_ONLY:
            # Always use positional arguments here
            pos_args.append(_locals[p.name])
        elif (
            p.kind == Parameter.POSITIONAL_OR_KEYWORD
            or p.kind == Parameter.POSITIONAL_ONLY
            or p.kind == Parameter.KEYWORD_ONLY
        ):
            # Add as keyword argument for now.
            kw_args[p.name] = _locals[p.name]
        elif p.kind == Parameter.VAR_POSITIONAL:
            varargs = _locals[p.name]
            if len(varargs) == 0:
                # The special treatment is not required if the parameter is defined, but empty, since that means that
                # no varargs were passed.
                continue
            # If we have a var positional param, all pos_or_kw params coming before must be passed as positional params.
            pos_args.extend(kw_args.values())
            kw_args.clear()
            # Now append varargs
            pos_args.extend(varargs)
        elif p.kind == Parameter.VAR_KEYWORD:
            # Add var keywords to kw dict
            kw_args.update(_locals[p.name])

    # Omit parameters that have their default values if requested
    if omit_defaulted_params is True:
        # Do for all
        for p in sig.parameters.values():
            if p.name in kw_args and kw_args[p.name] == p.default:
                del kw_args[p.name]

    elif isinstance(omit_defaulted_params, Iterable):
        # Do for listed
        for name in omit_defaulted_params:
            if name in kw_args and kw_args[name] == sig.parameters[name].default:
                del kw_args[p.name]

    # Return positional args as tuple and kwargs as dict
    return tuple(pos_args), dict(kw_args)
