#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
## @file ostap/core/ostap_types.py
#  core types for ostap 
#  @author Vanya BELYAEV Ivan.Belyaev@itep.ru
#  @date   2011-06-07
# =============================================================================
"""Core types for ostap 
"""
# =============================================================================
__version__ = "$Revision$"
__author__  = "Vanya BELYAEV Ivan.Belyaev@itep.ru"
__date__    = "2011-06-07"
__all__     = (
    ##
    'num_types'       , ## numerical types (real)
    'integer_types'   , ## integer types
    'string_types'    , ## string  types
    'str_types'       , ## string  types (only string!)
    'listlike_types'  , ## list-like types (list, tuple, set, collections.Iterable)
    'list_types'      , ## list types (list, tuple)
    'dict_types'      , ## dict types 
    'dictlike_types'  , ## dict-like types 
    'long_type'       , ## long-type
    'sequence_types'  , ## sequence types
    'iterable_types'  , ## iterable 
    'sized_types'     , ## sized types 
    ##
    'is_integer'      , ## is a value of int-like type?
    'is_number'       , ## is a value of numeric  type?
    'is_good_number'  , ## is a value of numeric  type and not-NaN,no-Inf ?
    ##
    'is_string'       , ## is a value of str-type? 
    'is_string_like'  , ## is a value of string-like type? 
    'is_list'         , ## is a value of list/tuple type?
    'is_list_like'    , ## is a value of list-like type?
    ##
    'all_integers'    , ## all argumets of integer types?
    'all_numerics'    , ## all argumets of numeric types?
    'all_strings'     , ## all argumets of string  types?
    )
# =============================================================================
import math
from   sys import version_info as python_version 
if ( 3 , 0 ) <= python_version :
    long           = int
    string_types   = bytes , str 
    integer_types  = int   ,
    long_type      = int
    import collections.abc as C
else :
    string_types   = str   , unicode
    integer_types  = int   , long
    long_type      = long 
    python_version = 2 
    import collections     as C
# =============================================================================
if   ( 3 , 5 ) <= python_version : from collections.abc import Generator, Collection, Sequence, Iterable, Sized   
elif ( 3 , 3 ) <= python_version :
    from collections.abc import Collection, Sequence, Iterable, Sized   
    from types           import GeneratorType as Generator 
else :
    from collections     import Sequence , Iterable , Sized            
    from collections     import Container     as Collection
    from types           import GeneratorType as Generator
    
# =============================================================================
# logging 
# =============================================================================
from ostap.logger.logger import getLogger 
if '__main__' ==  __name__ : logger = getLogger( 'ostap.core.ostap_types' )
else                       : logger = getLogger( __name__     )
# =============================================================================
logger.debug ( 'Core objects/classes/functions for Ostap')
# =============================================================================

iterable_types  = Iterable,
num_types       = integer_types + ( float , ) 
str_types       = str,

list_types      = list , tuple

import array 
listlike_types  = list_types + ( set , C.Sequence , array.array )
# =============================================================================
try :
    import numpy as np
    listlike_types  = listlike_types + ( np.ndarray , )    
except ImportError :
    pass 
# =============================================================================
dict_types      = dict ,
dictlike_types  = dict ,  C.Mapping  
sequence_types  = listlike_types + ( Sequence , Collection , Iterable , Generator )
sized_types     = Sized ,
# =============================================================================

# =============================================================================
## Is this number of a proper integer?
def is_integer ( v ) :
    """Is this number of a proper integer?"""
    return isinstance ( v , integer_types ) 

# =============================================================================
## Is this number of a proper numeric type
def is_number  ( v ) :
    """Is this number of a proper numeric?"""
    return isinstance ( v , num_types   ) 

# =============================================================================
## good numeric value 
def is_good_number  ( v ) :
    """Is numeric type and good value?"""
    return isinstance ( v , num_types   ) and \
           ( not math.isinf ( v ) ) and ( not math.isnan ( v ) )

# =============================================================================
## is  value of str-type?
def is_string ( v ) :
    """Is  value of str-type?"""
    return isinstance ( v , str_types )

# =============================================================================
## is  value of string-like -type?
def is_string_like ( v ) :
    """Is  value of string-like type?"""
    return isinstance ( v , string_types )

# =============================================================================
## is list type?
def is_list  ( v ) :
    """Is value of list type (list ot tuple)"""
    return isinstance ( v , list_type )

# =============================================================================
## is list-like type?
def is_list_like  ( v ) :
    """Is value of list-like type (list but not a string-like!)"""
    return isinstance ( v , listlike_type ) and not isinstance ( v , string_types )

# =============================================================================
## are all values of integer-line types?
def all_integers ( *args ) :
    """Are all value of integer-line types?
    """
    for a in args :
        if not isinstance ( a , integer_types ) : return False
    return True

# =============================================================================
## are all values of numeric types?
def all_numerics ( *args ) :
    """Are all values of numeric types?
    """
    for a in args :
        if not isinstance ( a , num_types ) : return False
    return True

# =============================================================================
## are all values of string types?
def all_strings ( *args ) :
    """Are all values of string types?
    """
    for a in args :
        if not isinstance ( a , stgring_types ) : return False
    return True

    
# =============================================================================
if '__main__' == __name__ :

    from ostap.utils.docme import docme
    docme ( __name__ , logger = logger )

    
# =============================================================================
if '__main__' == __name__ :

    from ostap.utils.docme import docme
    docme ( __name__ , logger = logger )

    
# =============================================================================
##                                                                      The END 
# =============================================================================
