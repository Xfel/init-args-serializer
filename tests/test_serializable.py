import init_args_serializer.serializable as uut
import pickle


# A simple serializable subclass used for tests
class SerTestBase(uut.Serializable):

    def __init__(self, arg1, arg2):
        # Capture args for serializable
        uut.Serializable._init(self, locals())

        # For testing, capture args separately
        self.initargs = (arg1, arg2)


def test_ser_deser():
    # test with init args only
    obj = SerTestBase('posarg1', 'posarg2')
    # Pickle/unpickle
    obj_loaded = pickle.loads(pickle.dumps(obj))
    # Check
    assert obj_loaded.initargs == obj.initargs


# A serializable subclass using getstate/setstate
class SerTestGetstate(uut.Serializable):

    def __init__(self, arg1, arg2="arg2def"):
        # Capture args for serializable
        uut.Serializable._init(self, locals())

        # For testing, capture args separately
        self.initargs = (arg1, arg2)

        # Add a state variable
        self.statevar = "initstate"

    def _get_state(self, state_dict):
        state_dict['statevar'] = self.statevar

    def _set_state(self, state_dict, copying=False):
        self.statevar = state_dict['statevar']


def test_ser_deser_getstate_unchanged():
    # Check that the getstate/setstate system works
    obj = SerTestGetstate('argval1')
    # Don't change state var

    # Pickle/unpickle
    obj_loaded = pickle.loads(pickle.dumps(obj))
    # Check init args
    assert obj_loaded.initargs == obj.initargs
    # Check state
    assert obj_loaded.statevar == "initstate"

def test_ser_deser_getstate_changed():
    # Check that the getstate/setstate system works
    obj = SerTestGetstate('argval1')
    # Change state var
    obj.statevar = "changedstate"

    # Pickle/unpickle
    obj_loaded = pickle.loads(pickle.dumps(obj))
    # Check init args
    assert obj_loaded.initargs == obj.initargs
    # Check state
    assert obj_loaded.statevar == "changedstate"


# Check inheritance
class SerTestInherited(SerTestBase):

    def __init__(self, arg1, arg2, arg3):
        # Capture args for serializable
        uut.Serializable._init(self, locals())

        # Call parent ctor
        super(SerTestInherited, self).__init__(arg1, arg2)

        # For testing, capture args separately
        self.sub_initargs = (arg3,)


def test_ser_deser_inherited():
    # test with init args only
    obj = SerTestInherited('posarg1', 'posarg2', 'posarg3')
    # Pickle/unpickle
    obj_loaded = pickle.loads(pickle.dumps(obj))
    # Check
    assert obj_loaded.initargs == ('posarg1', 'posarg2')
    assert obj_loaded.sub_initargs == ('posarg3', )


# Test copying
def test_copy():
    obj = SerTestBase('posarg1', 'posarg2')
    # Copy object
    obj_loaded = obj.copy()
    # Check
    assert obj_loaded.initargs == obj.initargs


def test_copy_getstate_unchanged():
    # Check that the getstate/setstate system works
    obj = SerTestGetstate('argval1')
    # Don't change state var

    # Copy object
    obj_loaded = obj.copy()
    # Check init args
    assert obj_loaded.initargs == obj.initargs
    # Check state
    assert obj_loaded.statevar == "initstate"


def test_copy_getstate_changed():
    # Check that the getstate/setstate system works
    obj = SerTestGetstate('argval1')
    # Change state var
    obj.statevar = "changedstate"

    # Copy object
    obj_loaded = obj.copy()
    # Check init args
    assert obj_loaded.initargs == obj.initargs
    # Check state
    assert obj_loaded.statevar == "changedstate"


def test_copy_inherited():
    obj = SerTestInherited('posarg1', 'posarg2', 'posarg3')
    # Copy object
    obj_loaded = obj.copy()
    # Check
    assert obj_loaded.initargs == ('posarg1', 'posarg2')
    assert obj_loaded.sub_initargs == ('posarg3',)


# test copy with arg override
def test_copy_arg_override():
    obj = SerTestInherited('posarg1', 'posarg2', 'posarg3')
    # Copy object
    obj_loaded = obj.copy(arg2='changed')
    # Check
    assert obj_loaded.initargs == ('posarg1', 'changed')
    assert obj_loaded.sub_initargs == ('posarg3',)