#do not import with 'require'

import inspect
import pickle
import importlib
import textwrap
from hashing import md5_hash, hash_deps
from typesystem import create_typesystem
from signature_match_args import signature_match_args
from cache import create_cache
from typed import typed
import require

ts = create_typesystem( prefix = "node_" )
version = hash_deps( "typesystem", __name__ )
cache = create_cache( "node_cache", version = version )
tmp_cache = create_cache( "/tmp/node_cache", version = version )
node_base_t = ts.create_type(( ), dict( ), key = "node_base", allow_duplicates = True )
node_generic_base_t = ts.create_type(( ), dict( ), key = "node_generic_base", allow_duplicates = True )
bytecode_t = type(( lambda: None ).__code__ ) #bit hacky

def get_fn_source_hash( fn ):

    code = fn if bytecode_t == type( fn ) else fn.__code__ 
    hash_v = md5_hash( str( code.co_code ))
    
    for c in code.co_consts:
        
        hash_v = md5_hash( hash_v + ( get_fn_source_hash( c ) if bytecode_t == type( c ) else str( c )))
    
    return hash_v

def get_fn_source( fn ):
    
    try:
        return inspect.getsource( fn )

    except:
        return "N/A"

def indent( txt, n_tabs ):
    
    if txt is None:
        
        txt = ""
    
    return txt.replace( "\n", "\n" + "    " * n_tabs )

#TODO: warn if generic_name is already in use
#TODO: detect dependency cycles of nodes
#TODO: dicts with different keyword order are not hashed the same, wasteful
def create_generic_node( generic_declarator_func, generic_name: str ):
    
    generic_sig = inspect.signature( generic_declarator_func )
    node_generic_uuid = md5_hash( generic_name + str( generic_sig ) + get_fn_source_hash( generic_declarator_func ))
    node_generic_t = ts.create_type(( node_generic_base_t, ), dict( ), readonly = False, key = f"generic_node<{ generic_name }, { node_generic_uuid }>", allow_duplicates = True )
    cache_location = None
    
    generic_doc = textwrap.dedent( f"""\

        Node generic type { node_generic_t.__qualname__ } with { len( generic_sig.parameters )} type parameter(s)

        Interface:

            given{ generic_sig }: returns a type specialization
            
        Source:
        
            { indent( get_fn_source( generic_declarator_func ), 3 )}
    """ )
    
    def encode_type_arg_value( value ):
        
        txt = str( value )
        txt = txt.replace( ".", "?" )
        return txt

    def get_cache( ):

        cache_locations = { "local": cache, "/tmp": tmp_cache }
        
        if cache_location in cache_locations:

            return cache_locations[ cache_location ]

        return cache_locations[ "local" ]
    
    def generic_specialize( * args, ** kwargs ):
        
        require._begin_collect_hash( )
        main = typed( generic_declarator_func )( * args, ** kwargs )
        subhashes = require._end_collect_hash( ) # changes if 'require'd modules change
        
        sig = inspect.signature( main )
        
        for ( name, p ) in sig.parameters.items( ):
            
            assert p.annotation is not inspect._empty, f"parameter { name } is not annotated"
            assert issubclass( p.annotation, node_base_t ) , f"{ name } is not a node"
        
        arg_dict = signature_match_args( generic_declarator_func, args, kwargs )
        node_uuid = md5_hash( node_generic_uuid + str( arg_dict ) + subhashes )
        type_args = [ generic_name, * map( encode_type_arg_value, arg_dict.values( )), node_uuid ]
        node_t = ts.create_type(( node_base_t, ), dict( ), readonly = False, key = f"node<{ ', '.join( type_args )}>", allow_duplicates = True )
        
        def get_raw( ):
            
            result_dict = { name: p.annotation.get( ) for ( name, p ) in sig.parameters.items( )}
            result = typed( main )( ** result_dict )
            instance = node_t( )
            instance.v = instance.res = instance.result = result
            return instance
        
        def get( ):
            
            return get_cache( ).get( get_cache_key( ), get_raw )
        
        def clear( ):
        
            return get_cache( ).delete( get_cache_key( ))
        
        def get_cache_key( ):
            
            cache_dict = { name: p.annotation.get_cache_key( ) for ( name, p ) in sig.parameters.items( )}
            hash_v = node_uuid
            hash_v = md5_hash( hash_v + str( cache_dict ))
            hash_v = md5_hash( hash_v + get_fn_source_hash( generic_declarator_func ))
            hash_v = md5_hash( hash_v + get_fn_source_hash( main ))
            return f"{ node_generic_uuid }/{ hash_v }"
            
        node_t.get = get
        node_t.get_result = lambda: get( ).result
        node_t.get_cache_key = get_cache_key
        node_t.clear = clear
        
        type_params = '\n'.join([ f"{ key }: { value }" for ( key, value ) in signature_match_args( generic_declarator_func, args, kwargs ).items( )])
        inputs = '\n'.join([ f"{ name }: { p.annotation.__qualname__ }" for ( name, p ) in sig.parameters.items( )])
        
        tab = "    "
        
        doc = textwrap.dedent( f"""\

            Node type { node_t.__qualname__ } with { len( sig.parameters )} input(s)
            Type specialization of { node_generic_t.__qualname__ }
            
            Type parameters:

                { indent( type_params, 4 )}
            
            Inputs:
            
                { indent( inputs, 4 )}
            
            Static interface:

                get( ): creates an instance of this node type and computes its result
                
            Interface:
            
                v, res, result: the computed result of { main.__name__ }
                
            Result type documentation:
            
                { indent( "N/A" if sig.return_annotation is inspect._empty else sig.return_annotation.__doc__, 4 )}
            
            Generic node type documentation:
            
                { indent( generic_doc, 4 )}
        """ )
        
        node_t.__doc__ = doc
        return node_t
    
    node_generic_t.given = generic_specialize
    node_generic_t.__doc__ = generic_doc

    def generic_clear( ):
        
        return get_cache( ).delete( node_generic_uuid )

    def store_in_tmp( ):

        nonlocal cache_location
        cache_location = "/tmp";
    
    node_generic_t.get = lambda * args, ** kwargs: node_generic_t.given( * args, ** kwargs ).get( )
    node_generic_t.get_result = lambda * args, ** kwargs: node_generic_t.given( * args, ** kwargs ).get_result( )
    node_generic_t.get_cache_key = lambda * args, ** kwargs: node_generic_t.given( * args, ** kwargs ).get_cache_key( )
    node_generic_t.clear = generic_clear
    node_generic_t.store_in_tmp = store_in_tmp
    
    return node_generic_t
    
def cache_key_node( cache_key_func, name = None, key = "" ):
    
    hash_v = md5_hash( str( key ) + get_fn_source_hash( cache_key_func ))
    type_args = [ hash_v ] if name is None else [ name, hash_v ]
    node_t = ts.create_type(( node_base_t, ), dict( ), readonly = False, key = f"cache_key_node<{ ', '.join( type_args )}>", allow_duplicates = True )
    
    def get( ):
        
        instance = node_t( )
        instance.v = instance.res = instance.result = cache_key_func( )
        return instance
    
    node_t.get = get
    node_t.get_cache_key = cache_key_func
    node_t.__doc__ = textwrap.dedent( f"""
        
        Cache key node
        
        Source:
        
            { indent( get_fn_source( cache_key_func ), 1 )}
    """ )
    
    return node_t

# decorator
def generic_node( generic_declarator_func ):
    
    return create_generic_node( generic_declarator_func, generic_declarator_func.__name__ )

def find( module_name, node_name = None ):

    # untracked, since the nodes have their own invalidation mechanism
    mod = require.module( module_name, untracked = True )
    
    def try_attribute( attribute_name ):
        
        if hasattr( mod, attribute_name ):
        
            node = getattr( mod, attribute_name )
            if issubclass( node, node_base_t ) or issubclass( node, node_generic_base_t ):
                
                return node

    if node_name is None:

        node = try_attribute( "node" ) or try_attribute( module_name )

    else:

        node = try_attribute( f"{ node_name }_node" ) or try_attribute( f"node_{ node_name }" )
    
    assert not node is None, f"could not find node '{ node_name }' in module '{ module_name }'"
    return node

# decorate
def store_in_tmp( generic_node ):

    generic_node.store_in_tmp( )
    return generic_node
