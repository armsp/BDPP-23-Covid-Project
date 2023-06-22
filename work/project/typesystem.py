from types import SimpleNamespace as namespace
from collections.abc import Iterable
import builtins
import importlib
import textwrap
from hashing import md5_hash
from typed import typed, validate_arguments, fullname

def create_typesystem( prefix = "" ):
    
    def indent( txt, n_tabs ):
    
        return txt.replace( "\n", "\n" + "    " * n_tabs )
    
    @typed
    def create_type( bases: tuple, own_type_dict: dict, readonly: bool = True, key = None, allow_duplicates = True ):

        type_dict = { }
        
        # only base classes allowed that are created with this method
        for base in bases:
                
            type_dict.update( base.type_dict )

        type_dict.update( own_type_dict )
        type_constraints_string = build_type_constraints( type_dict )
        
        hash_v = md5_hash( type_constraints_string )
        hash_v = md5_hash( hash_v + ", ".join( map( fullname, bases ))) 
        name = f"type<{ hash_v }>" if key is None else key
        
        # necessary for pickling consistency
        own_module = importlib.import_module( __name__ )
        if name in own_module.__dict__:
        
            return own_module.__dict__[ name ]
        
        t = type( name, bases, { name: None for ( name, _ ) in type_dict.items( )})
        
        # necessary for pickling
        assert t.__module__ == __name__
        assert t.__name__ == name
        own_module.__dict__[ name ] = t
        
        def create( ** kwargs ):
            
            validate_arguments( kwargs, type_dict )
            instance = t( )
            instance.__dict__ = kwargs
            return instance
        
        t.type_dict = type_dict
        t.create = create
        
        def t_setattr( self, key, value ):
    
            if key == "__dict__" or not readonly:

                object.__setattr__( self, key, value )
            else:

                raise Exception( f"{ t.__name__ } is readonly" )

        builtins.setattr( t, "__setattr__", t_setattr )
        delimiter = "\n"
        doc = textwrap.dedent( f"""
        
            Generated { 'readonly' if readonly else 'mutable' } type of typesystem '{ prefix }'

            Data: 

                { indent( build_type_constraints( type_dict, delimiter = delimiter ), 4 )}
        """)
        
        builtins.setattr( t, "__doc__", doc )
        return t

    def type_constraint_to_string( constraint ):

        if type( constraint ) == type:

            return fullname( constraint )

        elif isinstance( constraint, Iterable ):

            return "[ " + ", ".join([ type_constraint_to_string( c ) for c in constraint ]) + " ]"

        return "None"

    def build_type_constraints( type_dict, delimiter = ", " ):

        return delimiter.join([ f"{ name }: { type_constraint_to_string( constraint )}" for ( name, constraint ) in type_dict.items( )])
    
    return namespace( create_type = create_type )
