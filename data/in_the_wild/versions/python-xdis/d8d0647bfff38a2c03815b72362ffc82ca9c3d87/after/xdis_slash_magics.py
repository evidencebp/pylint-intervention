"""
Everything you ever wanted to know about Python versions and their
magic numbers. And a little bit more...
"""
import imp, struct, sys

def int2magic(magic):
    if (sys.version_info >= (3, 0)):
        return struct.pack('Hcc', magic, bytes('\r', 'utf-8'), bytes('\n', 'utf-8'))
    else:
        return struct.pack('Hcc', magic, '\r', '\n')

def magic2int(magic):
    return struct.unpack('Hcc', magic)[0]

# The magic integer for the current running Python interpreter
PYTHON_MAGIC_INT = magic2int(imp.get_magic())

by_magic = {}
by_version = {}

def __by_version(magics):
    for m, v in list(magics.items()):
        if m not in by_magic:
            by_magic[m] = set([v])
        else:
            by_magic[m].add(v)
        by_version[v] = m
    return by_version

versions = {
    # Magic word to reject .pyc files generated by other Python versions.
    # It should change for each incompatible change to the bytecode.
    #
    # The value of CR and LF is incorporated so if you ever read or write
    # a .pyc file in text mode the magic number will be wrong; also, the
    # Apple MPW compiler swaps their values, botching string constants.
    #
    # The magic numbers must be spaced apart at least 2 values, as the
    # -U interpeter flag will cause MAGIC+1 being used. They have been
    # odd numbers for some time now.
    #
    # There were a variety of old schemes for setting the magic number.
    # The current working scheme is to increment the previous value by
    # 10.
    #
    # Starting with the adoption of PEP 3147 in Python 3.2, every bump in magic
    # number also includes a new "magic tag", i.e. a human readable string used
    # to represent the magic number in __pycache__ directories.  When you change
    # the magic number, you must also set a new unique magic tag.  Generally this
    # can be named after the Python major version of the magic number bump, but
    # it can really be anything, as long as it's different than anything else
    # that's come before.  The tags are included in the following table, starting
    # with Python 3.2a0.

    # taken from from Python/import.c, importlib/_bootstrap.py and other sources
    # magic,          sample version number
    int2magic(11913): '1.3', #
    int2magic(5892):  '1.4', #
    int2magic(20121): '1.5', # 1.5, 1.5.1, 1.5.2
    int2magic(50428): '1.6', # 1.6
    int2magic(50823): '2.0', # 2.0, 2.0.1
    int2magic(60202): '2.1', # 2.1, 2.1.1, 2.1.2
    int2magic(60717): '2.2', # 2.2
    int2magic(62011): '2.3a0',
    int2magic(62021): '2.3a0', # ! Two magics one version
    int2magic(62041): '2.4a0',
    int2magic(62051): '2.4a3',
    int2magic(62061): '2.4b1',
    int2magic(62071): '2.5a0',
    int2magic(62081): '2.5a0', # ast-branch
    int2magic(62091): '2.5a0', # with
    int2magic(62092): '2.5a0', # changed WITH_CLEANUP opcode
    int2magic(62101): '2.5b3', # fix wrong code: for x, in ...
    int2magic(62111): '2.5b3', # fix wrong code: x += yield
    int2magic(62121): '2.5c1', # fix wrong lnotab with for loops and
                               #  storing constants that should have been removed
    int2magic(62131): '2.5c2', # fix wrong code: for x, in ... in
                               # listcomp/genexp)
    int2magic(62135): '2.5dropbox', # Dropbox-modified Python 2.5
                                    # used in versions 1.1x and before of Dropbox
    int2magic(62151): '2.6a0',   # peephole optimizations & STORE_MAP
    int2magic(62161): '2.6a1',   # WITH_CLEANUP optimization
    int2magic(62171): '2.7a0',   # optimize list comprehensions/change
                                 # LIST_APPEND
    int2magic(62181): '2.7a0+1', # optimize conditional branches:
                                 #  introduce POP_JUMP_IF_FALSE and
                                 # POP_JUMP_IF_TRUE
    int2magic(62191): '2.7a0+2', # introduce SETUP_WITH
    int2magic(62201): '2.7a0+3', # introduce BUILD_SET
    int2magic(62211): '2.7',     # introduce MAP_ADD and SET_ADD

    int2magic(62215): '2.7dropbox', # Dropbox-modified Python 2.7
                                    # used in versions 1.2-1.6 or so of
                                    # Dropbox

    int2magic(62211+7): '2.7pypy', # PyPy including pypy-2.6.1, pypy-5.0.1
                                   # PyPy adds 7 to the corresponding CPython nmber
    int2magic(3000): '3.000',
    int2magic(3010): '3.000+1',  # removed UNARY_CONVERT
    int2magic(3020): '3.000+2',  # added BUILD_SET
    int2magic(3030): '3.000+3',  # added keyword-only parameters
    int2magic(3040): '3.000+4',  # added signature annotations
    int2magic(3050): '3.000+5',  # print becomes a function
    int2magic(3060): '3.000+6',  # PEP 3115 metaclass syntax
    int2magic(3061): '3.000+7',  # string literals become unicode
    int2magic(3071): '3.000+8',  # PEP 3109 raise changes
    int2magic(3081): '3.000+9',  # PEP 3137 make __file__ and __name__ unicode
    int2magic(3091): '3.000+10', # kill str8 interning
    int2magic(3101): '3.000+11', # merge from 2.6a0, see 62151
    int2magic(3103): '3.000+12', # __file__ points to source file
    int2magic(3111): '3.0a4',  # WITH_CLEANUP optimization
    int2magic(3131): '3.0a5',  # lexical exception stacking, including POP_EXCEPT)
    int2magic(3141): '3.1a0',  # optimize list, set and dict comprehensions
    int2magic(3151): '3.1a0+', # optimize conditional branches
    int2magic(3160): '3.2a0',  # add SETUP_WITH
    int2magic(3170): '3.2a1',  # add DUP_TOP_TWO, remove DUP_TOPX and ROT_FOUR
    int2magic(3180): '3.2a2',  # 3.2a2 (add DELETE_DEREF)
    int2magic(3180+7): '3.2pypy',  # Python 3.2.5 - PyPy 2.3.4
                                   # PyPy adds 7 to the corresponding CPython number
    int2magic(3190): '3.3a0',  # __class__ super closure changed
    int2magic(3200): '3.3a0+', # __qualname__ added
    int2magic(3220): '3.3a1',  # changed PEP 380 implementation
    int2magic(3210): '3.3a2',  # added size modulo 2**32 to the pyc header
                               # NOTE: 3.3a2 is our name, other places call it 3.3
                               # but most 3.3 versions are 3.3a4 which comes next.
                               # FIXME: figure out what the history is and
                               # what the right thing to do if this isn't it.
    int2magic(3230): '3.3a4',  # revert changes to implicit __class__ closure
    int2magic(3250): '3.4a1',  # evaluate positional default arg
                               # keyword-only defaults)
    int2magic(3260): '3.4a1+1', # add LOAD_CLASSDEREF;
                                # allow locals of class to override free vars
    int2magic(3270): '3.4a1+2', # various tweaks to the __class__ closure
    int2magic(3280): '3.4a1+3',   # remove implicit class argument
    int2magic(3290): '3.4a4',     # changes to __qualname__ computation
    int2magic(3300): '3.4a4+',    # more changes to __qualname__ computation
    int2magic(3310): '3.4rc2',    # alter __qualname__ computation
    int2magic(3350): '3.5',       # 3.5.0, 3.5.1, 3.5.2
    int2magic(3351): '3.5.3',     # 3.5.3
    int2magic(3361): '3.6.0a1',   # 3.6.0a1
    int2magic(3370): '3.6.0a1+1', # 3.6.0a?
    int2magic(3370): '3.6.0a1+2', #
    int2magic(3372): '3.6.0a3',   #
    int2magic(3378): '3.6.0b2',   #
    int2magic(3379): '3.6.0rc1',  #

    # Weird ones
    int2magic(48):    '3.2a2', # WTF? Python 3.2.5 - PyPy 2.3.4
                               # This doesn't follow the rule below
    int2magic(112):   '3.5pypy', # pypy3.5-c-jit-latest
}

magics = __by_version(versions)

# From a Python version givin in sys.info, e.g. 3.6.1,
# what is the "canonic" version number, e.g. '3.6.0rc1'
canonic_python_version = {}

def add_canonic_versions(versions, canonic):
    for v in versions.split():
        canonic_python_version[v] = canonic
        magics[v] = magics[canonic]
        pass
    return

add_canonic_versions('1.5.1 1.5.2', '1.5')
add_canonic_versions('2.0.1', '2.0')
add_canonic_versions('2.1.1 2.1.2', '2.1')
add_canonic_versions('2.2.3', '2.2')
add_canonic_versions('2.3 2.3.7', '2.3a0')
add_canonic_versions('2.4 2.4.1 2.4.2 2.4.3 2.4.5 2.4.6', '2.4b1')
add_canonic_versions('2.5 2.5.1 2.5.2 2.5.3 2.5.4 2.5.5 2.5.6', '2.5c2')
add_canonic_versions('2.6 2.6.6 2.6.7 2.6.8 2.6.9', '2.6a1')
add_canonic_versions('2.7.1 2.7.2 2.7.2 2.7.3 2.7.4 2.7.5 2.7.6 2.7.7 '
                     '2.7.8 2.7.9 2.7.10 2.7.11 2.7.12 2.7.13', '2.7')
add_canonic_versions('3.3 3.3.1 3.3.0 3.3.2 3.3.3 3.3.4 3.3.5 3.3.6', '3.3a4')
add_canonic_versions('3.4 3.4.0 3.4.1 3.4.2 3.4.3 3.4.4 3.4.5 3.4.6', '3.4rc2')
add_canonic_versions('3.5.0 3.5.1 3.5.2', '3.5')
add_canonic_versions('3.6 3.6.0 3.6.1 3.6.2', '3.6.0rc1')

# The canonic version for a canonic version is itself
for v in versions.values():
    canonic_python_version[v] = v

# A set of all Python versions we know about
python_versions = set(canonic_python_version.keys())

def __show(text, magic):
    print(text, struct.unpack('BBBB', magic), struct.unpack('HBB', magic))

def test():
    magic_20 = magics['2.0']
    current = imp.get_magic()
    magic_current = by_magic[ current ]
    print(type(magic_20), len(magic_20), repr(magic_20))
    print()
    print('This Python interpreter has version', magic_current)
    print('Magic code: ', PYTHON_MAGIC_INT)
    print(type(magic_20), len(magic_20), repr(magic_20))

if __name__ == '__main__':
    test()
