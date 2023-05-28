# must be imported normally

import importlib
import sys
from hashing import md5_hash    
from types import SimpleNamespace as namespace
import functools

hash_stack = [ ]
symbol_stack = [ ]
cache = { }

def _begin_collect_hash( ):
    
    hash_stack.append([ ])
    
def _end_collect_hash( ):
    
    return md5_hash( ", ".join( hash_stack.pop( ))) 

# Makefile-style function
#l: locals
def _require_module( name, * args, uncached = False, verbose = False, to = None, untracked = False ):
    
    symbol_stack.append( to )
    
    # cached intermediate results
    spec = None
    source = None
    mod_cached = None
    mod_checked = None
    mod_uncached = None
    subhash = None
    own_hash = None
    local_cache = { }
    indent = namespace( level = 0, tab = "│  " )
    
    def produce_wrapper( f, show_result ):
        
        @functools.wraps( f )
        def wrapper( * args, ** kwargs ):

            if verbose:
                
                print( f"[require] { indent.tab * indent.level }{ f.__name__ }" )
                indent.level += 1
            
            result = f( * args, ** kwargs )

            if verbose:

                indent.level -= 1
                result_str = f"{ result }" if show_result else f"[{ type( result )}]"
                print( f"[require] { indent.tab * indent.level }└─▶ { result_str }" )

            return result

        return wrapper
    
    #decorator
    def log( f ):

        return produce_wrapper( f, False )
    
    #dectorator
    def log_res( f ):

        return produce_wrapper( f, True )
        
    @log
    def calc_spec( ):
        
        return importlib.util.find_spec( name, * args )
    
    @log
    def get_spec( ):
        
        nonlocal spec
        spec = spec or calc_spec( )
        return spec
    
    @log
    def calc_source( ):
        
        return get_spec( ).loader.get_source( get_spec( ).name )
    
    @log
    def get_source( ):
        
        nonlocal source
        source = source or calc_source( )
        return source
    
    @log
    def calc_mod_cached( ):
        
        return importlib.import_module( name, * args )
    
    @log
    def get_mod_cached( ):
        
        nonlocal mod_cached
        mod_cached = mod_uncached or mod_checked or mod_cached or calc_mod_cached( )
        return mod_cached
    
    @log
    def calc_mod_uncached( ):
        
        nonlocal mod_uncached
        nonlocal subhash
        
        if name is sys.modules:

            del sys.modules[ name ]
            
        _begin_collect_hash( ) 
        mod_uncached = get_spec( ).loader.load_module( get_spec( ).name ) # might run further 'require' calls
        subhash = _end_collect_hash( )
        return mod_uncached
    
    @log
    def get_mod_uncached( ):
        
        nonlocal mod_uncached
        mod_uncached = mod_uncached or calc_mod_uncached( )
        return mod_uncached
    
    @log
    def calc_subhash( ):
        
        calc_mod_uncached( )
        return subhash
    
    @log
    def get_subhash( ):
        
        nonlocal subhash
        subhash = subhash or calc_subhash( )            
        return subhash
    
    @log_res
    def is_bottom_level_module( ):

        # TODO: checking by name occurence is janky but good enough for now
        return "require" not in get_source( ) 
    
    @log_res
    def calc_own_hash( ):
        
        hash_v = md5_hash( get_source( )) if is_bottom_level_module( ) else md5_hash( get_subhash( ) + get_source( ))
        local_cache[ name ] = hash_v
        return hash_v
    
    @log_res
    def get_own_hash( ):
        
        nonlocal own_hash
        own_hash = own_hash or calc_own_hash( )
        return own_hash
    
    @log_res
    def test_cache( ):
        
        own_hash_now = get_own_hash( ) # avoid short circuit
        return name in cache and own_hash_now == cache[ name ]
    
    @log
    def calc_mod_checked( ):
        
        return get_mod_cached( ) if test_cache( ) else get_mod_uncached( )
    
    @log
    def get_mod_checked( ):
        
        nonlocal mod_checked
        mod_checked = mod_uncached or mod_checked or calc_mod_checked( )
        return mod_checked
    
    @log
    def get_mod( ):
        
        return get_mod_uncached( ) if uncached else get_mod_checked( )
    
    # we are not the top level require and hash tracking is not disabled
    if len( hash_stack ) > 0 and not untracked:

        hash_stack[ -1 ].append( get_own_hash( ))
        
    mod = get_mod( )
    cache.update( local_cache ) # this must be the last line before return    
    return mod

# keep this in items form, the order is important
def through_symbol_stack( symbol_items ):
    
    if len( symbol_stack ) > 0:
        
        symbols = symbol_stack.pop( )
        
        if symbols:
        
            symbols.update({ name: symbol for ( name, symbol ) in symbol_items })            
        
    values = [ v for ( _, v ) in symbol_items ]
    return values[ 0 ] if len( values ) == 1 else values

def module( name, * args, ** kwargs ):
    
    return through_symbol_stack([( name, _require_module( name, * args, ** kwargs ))])

def single( name, * args, ** kwargs ):
    
    return through_symbol_stack([( name, getattr( _require_module( name, * args, ** kwargs ), name ))])

def symbols( module_name, * symbol_names, ** kwargs ):
    
    mod = _require_module( module_name, ** kwargs )
    return through_symbol_stack([( name, getattr( mod, name )) for name in symbol_names ])

# TODO: make these options stack-based so they can recurse
def make_uncached_interface( ** ikwargs ):
    
    return namespace( 

        module = lambda * args, ** kwargs: module( * args, uncached = True, ** ikwargs, ** kwargs ),
        single = lambda * args, ** kwargs: single( * args, uncached = True, ** ikwargs, ** kwargs ),
        symbols = lambda * args, ** kwargs: symbols( * args, uncached = True, ** ikwargs, ** kwargs )
    )

def make_untracked_interface( ** ikwargs ):

    return namespace( 

        uncached = make_uncached_interface( untracked = True ),
        module = lambda * args, ** kwargs: module( * args, untracked = True, ** ikwargs, ** kwargs ),
        single = lambda * args, ** kwargs: single( * args, untracked = True, ** ikwargs, ** kwargs ),
        symbols = lambda * args, ** kwargs: symbols( * args, untracked = True, ** ikwargs, ** kwargs )
    )

uncached = make_uncached_interface( )
untracked = make_untracked_interface( )