import types
import warnings

from logipy.logic.rules import apply_method_rules
from logipy.logic.properties import LogipyPropertyException
import logipy.logic.properties as logipy_properties


def _is_callable(obj):
    """Returns true if given object is a callable.

    Provides support for wrapped objects.
    """
    if isinstance(obj, LogipyPrimitive):
        return callable(obj.get_logipy_value())
    return callable(obj)


def logipy_value(obj):
    if isinstance(obj, LogipyPrimitive):
        return obj.get_logipy_value()
    return obj


def error(message):
    raise Exception(message)


__logipy_past_warnings = set()


def logipy_warning(logipy_warning_message):
    if logipy_warning_message in __logipy_past_warnings:
        return
    __logipy_past_warnings.add(logipy_warning_message)
    warnings.warn(logipy_warning_message)


def logipy_call(method, *args, **kwargs):
    """Call a callable object inside a LogipyMethod wrapper.

    :param method: The callable object to be wrapped and called.
    :param args: Arguments to be passed to the callable object.
    :param kwargs: Keyword arguments to be passed to the callable object.

    # TODO: Bettern return comment.
    :return: Upon successful verification, returns the value returned
    by the callable.
    """
    if isinstance(method, LogipyMethod):
        return method(*args, **kwargs)
    return LogipyMethod(method)(*args, **kwargs)


class LogipyMethod:
    """Wrapper for every callable object that should be monitored."""

    def __init__(self, method, parent_object=None):
        # Prohibit double wrapping of a callable.
        if isinstance(method, LogipyMethod):
            exception_text = "LogipyMethod cannot call an instance of itself. "
            exception_text += "Consider using logipy_call function instead."
            raise Exception(exception_text)

        self.__parent_object = parent_object
        self.__method = method  # Wrapped callable object.
        self.__doc__ = method.__doc__
        if hasattr(method, "__name__"):
            self.__name__ = method.__name__
        if hasattr(method, "__module__"):
            self.__module__ = method.__module__

    def __call__(self, *args, **kwargs):
        """Wrapper method for monitoring the calls on a callable object."""
        properties = logipy_properties.empty_properties()
        # apply_method_rules(self.__method.__name__, unbound_variable, "call", args, kwargs)

        # Monitor "call" predicate.
        if self.__parent_object is not None:
            if isinstance(self.__parent_object, LogipyPrimitive):
                logipy_properties.combine(properties, self.__parent_object.get_logipy_properties())
                apply_method_rules(self.__method.__name__, self.__parent_object,
                                   "call", args, kwargs)

        # Monitor "called by" predicate.
        for arg in args:
            if isinstance(arg, LogipyPrimitive):
                logipy_properties.combine(properties, arg.get_logipy_properties())
                apply_method_rules(self.__method.__name__, arg, "called by", args, kwargs)
        for arg in kwargs.values():
            if isinstance(arg, LogipyPrimitive):
                logipy_properties.combine(properties, arg.get_logipy_properties())
                apply_method_rules(self.__method.__name__, arg, "called by", args, kwargs)

        # Monitor "returned by" predicate.
        # TODO: FIND THE BEST WAY TO DO THE FOLLOWING
        try:
            ret = self.__method(*args, **kwargs)
        except Exception as err:
            if not isinstance(err, LogipyPropertyException):
                args = [arg.get_logipy_value() if isinstance(arg, LogipyPrimitive) else arg for arg
                        in args]
                kwargs = {key: arg.get_logipy_value() if isinstance(arg, LogipyPrimitive) else arg
                          for key, arg in kwargs.items()}
                ret = self.__method(*args, **kwargs)
                logipy_warning(
                    "A method " + method_name +
                    " was called a second time at least once by casting away LogipyPrimitive " +
                    "due to invoking the error: " + str(err))
            else:
                raise err
        # ret = self.__method(*args, **kwargs)
        ret = LogipyPrimitive(ret, properties)
        apply_method_rules(self.__method.__name__, ret, "returned by", args, kwargs)
        # print(self.__method.__name__)

        return ret

    def __get__(self, instance, cls):
        return types.MethodType(self, instance) if instance else self


class LogipyPrimitive:
    __logipy_id_count = 0  # Counter for each instantiated LogipyPrimitive so far.

    def __init__(self, value, properties=None):
        # Convert a single property string, to a proper iterable.
        if properties is not None and isinstance(properties, str):
            properties = [properties]

        if isinstance(value, LogipyPrimitive):
            # If given value is already a LogipyPrimitive, copy its properties.
            self.__logipy_value = value.__logipy_value
            self.__logipy_properties = logipy_properties.empty_properties()
            logipy_properties.combine(self.__logipy_properties, value.__logipy_properties)
        else:
            # If given value is not a LogipyPrimitive, instantiate a new set of properties.
            self.__logipy_value = value
            self.__logipy_properties = logipy_properties.empty_properties()

        if properties is not None:
            logipy_properties.combine(self.__logipy_properties, properties)

        self.__logipy_id = str(LogipyPrimitive.__logipy_id_count)
        LogipyPrimitive.__logipy_id_count += 1  # TODO: Make it thread safe.

    def get_logipy_id(self):
        return self.__logipy_id

    def get_logipy_properties(self):
        return self.__logipy_properties

    def get_logipy_value(self):
        return self.__logipy_value

    def __getattr__(self, method_name):
        # TODO: Rewrite function with a single exit point.
        # Delegate attribute lookup from wrapper to the wrapped object.
        if hasattr(self.__logipy_value, method_name):
            if _is_callable(getattr(self.__logipy_value, method_name)):
                # Wrap callable attributes into a LogipyMethod wrapper.
                return LogipyMethod(getattr(self.__logipy_value, method_name), self)
            else:
                # Wrap non-callables into a LogipyPremitive wrapper.
                value = getattr(self.__logipy_value, method_name)
                if isinstance(value, LogipyPrimitive):
                    return value
                return LogipyPrimitive(value, self.__logipy_properties)
        else:
            raise AttributeError()

        # def method(self, *args, **kw):
        #     return LogipyPrimitive(getattr(self.__logipy_value, method_name)(*args, **kw))
        # return method
        # return object.__getattribute__(self, method_name)

    # def __setattr__(self, key, value):
    # self.__dict__["_LogipyPrimitive__logipy_value"].__dict__[key] = value
    # self.__dict__[key] = value

    def __nonzero__(self):
        return bool(self.value())  # TODO: value() method?????

    # def __hash__(self):
    #     return hash(self.__logipy_value)

    def __repr__(self):
        return repr(self.__logipy_value) + " (" + ", ".join(self.__logipy_properties) + ")"


_special_names = [
    '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
    '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
    '__eq__', '__floordiv__', '__ge__', '__getitem__',
    '__getslice__', '__gt__', '__hex__', '__iadd__', '__iand__',
    '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
    '__imul__', '__invert__', '__ior__', '__ipow__', '__irshift__',
    '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__',
    '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
    '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__len__',
    '__radd__',  # comment to not create string errors
    '__float__', '__int__', '__bool__', '__hash__', '__str__',
    '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
    '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
    '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
    '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
    '__truediv__', '__xor__', '__next__',  # '__repr__',
]

_primitive_converters = set(['__float__', '__int__', '__bool__', '__str__', '__hash__', '__len__'])


def _make_primitive_method(method_name):
    def method(self, *args, **kwargs):
        if method_name in _primitive_converters:
            return getattr(self.get_logipy_value(), method_name)(*args, **kwargs)
        return LogipyMethod(getattr(self.get_logipy_value(), method_name), self)(*args, **kwargs)

        # _apply_method_rules(method_name, self, call_rules, *args, **kwargs)
        # for arg in args:
        #     graph_logic = graph_logic.union(_properties(arg))
        #     _apply_method_rules(method_name, arg, call_rules, *args, **kwargs)
        # for arg in kwargs.values():
        #     graph_logic = graph_logic.union(_properties(arg))
        #     _apply_method_rules(method_name, arg, call_rules, *args, **kwargs)
        # ret = LogipyPrimitive(getattr(self.logipy_value(), method_name)(*args, **kwargs), graph_logic)
        # _apply_method_rules(method_name, ret, return_rules, *args, **kwargs)
        # return ret

    return method


for method_name in _special_names:
    setattr(LogipyPrimitive, method_name, _make_primitive_method(method_name))

# unbound_variable = LogipyPrimitive(None)