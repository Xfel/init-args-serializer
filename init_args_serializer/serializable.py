from inspect import Parameter, signature

from .function_arg_capture import capture_args


def _serializable_load(cls, args, kwargs, state):
    """
    Create the new instance using args and kwargs, then apply the additional state. This is used by the __reduce__
    implementation.

    :param cls: class to create an insance of
    :param args: positional arguments
    :param kwargs: keyword arguments
    :param state: additional stored state
    :return: function call result
    """
    obj = cls(*args, **kwargs)
    obj._set_state(state)
    return obj


class Serializable:
    """
    Enables improved pickling support. Instead of storing the entire __dict__, the parameters passed to __init__ are
    captured. During unpickling, the captured parameters are used to create a new object instance.

    This behaviour is implemented using the __reduce__ hook. It is strongly discouraged to override the __reduce__
    method. If you need to pickle variables beyond the constructor parameters, you should use the regular __getstate__
    and __setstate__ methods.

    The type also features a cloning mechanism, where some constructor keywords can be replaced with others.
    """

    def _init(self, _locals, **kwargs):
        """
        Capture __init__ parameters from the given locals.

        This function is expected to be called at the start of the init function.
        It uses capture_args(self.__init__, _locals, **kwargs) to do so.

        :param _locals: locals() dict from the __init__ function
        :param kwargs: additional kwargs to pass to capture_args
        """
        # Make sure we only initialize once
        if getattr(self, "_serializable_initialized", False):
            return
        setattr(self, "_serializable_initialized", True)
        self.__args, self.__kwargs = capture_args(self.__init__, _locals, **kwargs)

    def __reduce__(self):
        # Build reduce tuple. Use a list while building to allow extension
        # Create the deserialized object using the constructor and the stored arguments
        # Since reduce only allows positional args, I use a helper function

        # Grab additional state
        state = dict()
        self._get_state(state)

        # Return reduce tuple
        return _serializable_load, (type(self), self.__args, self.__kwargs, state)

    def _get_state(self, state_dict):
        """
        Override to save any persistent state into state_dict.
        :param state_dict: dict to fill with state entries
        """
        pass

    def _set_state(self, state_dict, copying=False):
        """
        Override to restore persistent state from state_dict.

        Care must be taken if this method is called during a copy operation. Since the init parameters might be
        different, the stored state might not be appropriate any more. The copying parameter is set to true in
        that case.

        :param state_dict: dict filled with state entries
        :param copying: true if called by copy
        """
        pass

    def copy(self, **overrides):
        """
        Create a copy of this object, optionally replacing argument values.
        :param kwargs: replacements for argument values, keyed by parameter name set in the init function
        :return: the copyied instance
        """
        new_args = self.__args
        new_kwargs = self.__kwargs
        # Process overrides
        if overrides:
            if len(new_args) == 0:
                # No positional args, so simply add all overrides to kwargs
                new_kwargs = dict(new_kwargs, **overrides)
            else:
                # Must update positional args
                # Modify a copy of args and kwargs
                new_args = list(new_args)
                new_kwargs = dict(new_kwargs)

                sig = signature(self.__init__, follow_wrapped=False)
                # Look at overrides for positional parameters
                for i, param in enumerate(sig.parameters):
                    if param.kind == Parameter.VAR_POSITIONAL:
                        # Last positional parameter
                        if param.name in overrides:
                            # Override for var positional param. Remove old and add new
                            del new_args[i:]
                            new_args.extend(overrides[param.name])
                        # All remaining parameters are keyword only
                        break
                    elif param.name in overrides:
                        # Store overridden value
                        new_args[i] = overrides.pop(param.name)
                # All positional parameters were removed from overrides, so add the rest to kwargs
                new_kwargs.update(overrides)
        # Create copied instance
        copied_obj = type(self)(*new_args, **new_kwargs)

        # Copy state
        state = dict()
        self._get_state(state)
        copied_obj._set_state(state, copying=True)

        return copied_obj
